from __future__ import division
import pandas as pd
import numpy as np
import itertools as it
import pickle
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

hon = pd.read_csv("hon.csv.gz", compression="gzip")
hon = hon.drop(["ignore"], axis=1)

trip = pd.read_csv("trip.csv.gz", compression="gzip")
trip = trip.drop(["ignore"], axis=1)

# Ids
honid = hon["id"]
tripid = trip["id"]

#Definitions
nelements = 10000 # hon.shape[0] #(92111)
folds = 10
equal = False
repetitions = 10

np.random.seed(0)

# Selects nelements
if equal:
    tindex = np.random.choice(trip.shape[0], size=nelements, replace=False)
    hindex = np.random.choice(hon.shape[0], size=nelements, replace=False)
    tnelements, hnelements = nelements, nelements
    print "Same sizes for trip and hon %d" % (nelements)

else:
    tindex = np.arange(trip.shape[0])
    np.random.shuffle(tindex)
    hindex = np.arange(hon.shape[0])
    np.random.shuffle(hindex)
    tnelements, hnelements = trip.shape[0], hon.shape[0]
    print "Different sizes for trip %d and hon %d" % (tnelements, hnelements)

def makeXy(labels):
    #### TRIP = 0, HON = 1
    #t = trip[semantic_labels + umls_labels + chv_labels + pos_labels].ix[tindex]
    t = trip[labels].ix[tindex]
    #h = hon[semantic_labels + umls_labels + chv_labels + pos_labels].ix[hindex]
    h = hon[labels].ix[hindex]
    
    X = t.append(h)
    X = X.values
    y = np.concatenate((np.ones(tnelements), np.zeros(hnelements)))
    return X,y

def goParallel(X,y,repetitions=1):

    etccv = cross_val_score(ExtraTreesClassifier(), X, y, cv=10, n_jobs=-1)
    dmcv = cross_val_score(DummyClassifier(strategy="most_frequent"), X, y, cv=10, n_jobs=-1)

    return etccv.mean(), dmcv.mean(), etccv.mean()/dmcv.mean() - 1.0

def tpr_score(actual, pred, pos_label=0):
    return (pred[actual == pos_label] == pos_label).sum()

def getLabels(group):
    labels = []
    semantic_labels = ["AvgSymptomsPerQuery","AvgCausesPerQuery","AvgRemediesPerQuery","AvgNonSymCauseRemedyTypesPerQuery"]
    umls_labels = ["AvgQueriesUsingMeSH","AvgNumberOfMeSHPerQuery","AvgMeSHDepth","AvgQueriesUsingSources", "AvgNumberOfSourcesPerQuery", "AvgQueriesUsingConcepts", "AvgNumberOfConceptsPerQuery"]
    chv_labels = ["AvgNumberOfCHVDataFound", "AvgNumberOfCHVFound", "AvgNumberOfUMLSFound", "AvgNumberOfCHVMisspelledFound", "AvgNumberOfComboScoreFound"]
    pos_labels = ["PercentageOfAdjectives", "PercentageOfAdverbs","PercentageOfAuxiliars","PercentageOfConjuctions", "PercentageOfDeterminers",\
              "PercentageOfModals", "PercentageOfNouns", "PercentageOfPrepositions", "PercentageOfPronouns", "PercentageOfPunctuations",\
              "PercentageOfShapes", "PercentageOfVerbs"]
    basic_labels = ["AvgCharsPerQuery", "AvgWordsPerQuery"]

    if "sem" in group:
        labels.extend(semantic_labels)
    if "chv" in group:
        labels.extend(chv_labels)
    if "umls" in group:
        labels.extend(umls_labels)
    if "pos" in group:
        labels.extend(pos_labels)
    if "basic" in group:
        labels.extend(basic_labels)
    return np.array(labels)

feature_importances, feature_std = {}, {}
etcr, dmr = {}, {}
for r in range(1,6):
    for group in it.combinations(["sem","chv","umls","pos","basic"], r):
        etcr[group] = {"precision-1":[], "recall-1":[], "f1-1":[], "precision-0":[],"recall-0":[],"f1-0":[], "accuracy":[], "tpr-0":[],"tpr-1":[]}
        dmr[group] = {"precision-1":[], "recall-1":[], "f1-1":[], "precision-0":[],"recall-0":[],"f1-0":[], "accuracy":[], "tpr-0":[], "tpr-1":[]}
#lerrorTrip = []
#lerrorHon = []

#print "TRIP\n", t.mean(), "\nHON\n", h.mean()

for r in range(1,6):
    for group in it.combinations(["sem","chv","umls","pos","basic"], r):
        print "Running group:", group 
        labels = getLabels(group)
        X, y = makeXy(labels)

        feature_importances[group] = np.zeros(X.shape[1])
        feature_std[group] = np.zeros(X.shape[1])

        for i in range(repetitions):
            kf = KFold(n=(tnelements + hnelements), n_folds=folds, shuffle=True)

            for train, test in kf:
                etc = RandomForestClassifier(n_estimators=200, criterion='entropy', n_jobs=-1) #ExtraTreesClassifier()
                X_train, X_test = X[train], X[test]
                y_train, y_test = y[train], y[test]
                predict = etc.fit(X_train, y_train).predict(X_test)
                #predict = np.zeros(X_test.shape[0])
                d0pred = np.zeros(X_test.shape[0])
                d1pred = np.ones(X_test.shape[0])
            
                dmr[group]["f1-1"].append(f1_score(y_test, d1pred, pos_label=1))    
                dmr[group]["f1-0"].append(f1_score(y_test, d0pred, pos_label=0))    
                etcr[group]["f1-1"].append(f1_score(y_test, predict,pos_label=1))
                etcr[group]["f1-0"].append(f1_score(y_test, predict,pos_label=0))
                
                dmr[group]["precision-1"].append(precision_score(y_test, d1pred, pos_label=1))    
                dmr[group]["precision-0"].append(precision_score(y_test, d0pred, pos_label=0))    
                etcr[group]["precision-1"].append(precision_score(y_test, predict,pos_label=1))
                etcr[group]["precision-0"].append(precision_score(y_test, predict,pos_label=0))
                
                dmr[group]["recall-1"].append(recall_score(y_test, d1pred, pos_label=1))    
                dmr[group]["recall-0"].append(recall_score(y_test, d0pred, pos_label=0))    
                etcr[group]["recall-1"].append(recall_score(y_test, predict,pos_label=1))
                etcr[group]["recall-0"].append(recall_score(y_test, predict,pos_label=0))
                
                dmr[group]["accuracy"].append(accuracy_score(y_test, d1pred))    
                etcr[group]["accuracy"].append(accuracy_score(y_test, predict))
                
                dmr[group]["tpr-1"].append(tpr_score(y_test, d1pred, pos_label=1))    
                dmr[group]["tpr-0"].append(tpr_score(y_test, d0pred, pos_label=0))    
                etcr[group]["tpr-1"].append(tpr_score(y_test, predict,pos_label=1))
                etcr[group]["tpr-0"].append(tpr_score(y_test, predict,pos_label=0))
                
                feature_importances[group] += etc.feature_importances_
                feature_std[group] += np.std([tree.feature_importances_ for tree in etc.estimators_], axis=0)
                
                # Predict HON, but it should be TRIP:
                #errorTrip = predict - y_test > 0
                # Predict TRIP, but it should be HON:
                #errorHon = predict - y_test < 0
                #Correct prediction
                #correct = predict - y_test == 0
                
                #lerrorTrip.extend(test[errorTrip])
                #lerrorHon.extend(test[errorHon])
                #print test[correct]
                #print test[error1]
                #print X_test[correct]
            
    #lerrorTrip = np.array(lerrorTrip)
    #lerrorHon = np.array(lerrorHon)

    #d0, d1 = np.array(d0), np.array(d1)
    #etc0, etc1 = np.array(etc0), np.array(etc1)

    # Checking test-t
    #from scipy.stats import ttest_rel
    #print ttest_rel(dresults, results)

    #trip_wrong = trip_semantics.ix[lerrorTrip - nelements]
    #hon_wrong = hon_semantics.ix[lerrorHon]

    #print "TRIP\n", trip_wrong.mean(), "\nHON\n", hon_wrong.mean()
    #trip_wrong.head(50)
    #tripid.ix[trip_wrong.head(5)]

    #tripid[trip_wrong.head(1)]
    #tripid[lerrorTrip - nelements]
    #honid[lerrorHon]

    #return etc0.mean(), d0.mean(), etc0.mean()/d0.mean() - 1.0, etc1.mean(), d1.mean(), etc1.mean()/d1.mean() -1.0

pickle.dump(feature_importances, open("features.pk","w"))
pickle.dump(feature_std, open("features_std.pk","w"))
pd.DataFrame(etcr).to_pickle("rfc.pk")
pd.DataFrame(dmr).to_pickle("dfc.pk")


