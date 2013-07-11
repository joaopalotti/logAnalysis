#Report
from sklearn import cross_validation
from sklearn.metrics import classification_report, f1_score, accuracy_score
#General
from collections import Counter, defaultdict

def makeIncrementalReport(X, y, listOfYs, accBaseline, sf1Baseline, wf1Baseline, mf1Baseline):
    a, f, wf, mf = [], [], [], []
    for i in listOfYs:
        print "Partition ", i
        print len(listOfYs[i])
        #print listOfYs[i]
        acc, sf1, wf1, mf1 = makeReport(X, y, listOfYs[i], accBaseline, sf1Baseline, wf1Baseline, mf1Baseline)
        a, f, wf, mf = a + [acc], f + [sf1], wf + [wf1], mf + [mf1]
    return a, f, wf, mf

def makeReport(X, y, y_pred, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline):
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    
    target_names = ['Layman', 'Specialist']
    
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred, average=None)
    # Simple F1 calculated by the f1 function
    sf1 = f1_score(y, y_pred)
    # Mean F1 ==> (F1(c1) + F1(c2)) / 2 
    mf1 = f1.mean()
    # Weighted F1
    ns = Counter(y)
    wf1 = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    
    print(classification_report(y, y_pred, target_names=target_names))
    
    print "F1 Scores (no average) --> ", (f1)
    
    print "sf1 -> ", sf1
    print "GAIN --> %0.2f%% " % (100.0 * (sf1 - sf1Baseline) / sf1Baseline)
    
    print "mf1 -> ", mf1
    print "GAIN --> %0.2f%% " % (100.0 * (mf1 - mf1Baseline) / mf1Baseline)
    
    print "wf1 -> ", wf1
    print "GAIN --> %0.2f%% " % (100.0 * (wf1 - wf1Baseline) / wf1Baseline)
    
    print "ACC Score --> ", (acc)
    print "GAIN --> %0.2f%% " % (100.0 * (acc - accBaseline) / accBaseline)

    return acc, sf1, wf1, mf1,

def classify(clf, X, y, CV, nJobs, tryToMeasureFeatureImportance=False, featureNames=None):

    print clf
    nSamples, nFeatures = X.shape

    kFold = cross_validation.KFold(n=nSamples, n_folds=CV, indices=True)

    # Run classifier
    lists = [clf.fit(X[train], y[train]).predict(X[test]) for train, test in kFold]
    
    y_pred = []
    for l in lists:
        y_pred += list(l)
    
    scores = cross_validation.cross_val_score(clf, X, y, cv=CV, n_jobs=nJobs) #, scoring="f1") 
    if tryToMeasureFeatureImportance:
        measureFeatureImportance(clf, featureNames)

    print "Done"
    return y_pred

#llq -> listOfListOfQueries
def classifyIncremental(clf, X, listOfLists, y, CV, nJobs, tryToMeasureFeatureImportance=False, featureNames=None):
    
    print clf
    nSamples, nFeatures = X.shape

    for l in listOfLists:
        print "l = ",l.shape
    print "x = ", X.shape
    print "y = ", y.shape

    kFold = cross_validation.KFold(n=nSamples, n_folds=CV, indices=True)

    # Run classifier
    #lists = [clf.fit(X[train], y[train]).predict(X[test]) for train, test in kFold]
    results = defaultdict(list)
    for train, test in kFold:
        for i, l in zip(range(len(listOfLists)), listOfLists):
            results[i] += list(clf.fit(X[train], y[train]).predict(l[test]))

    scores = cross_validation.cross_val_score(clf, X, y, cv=CV, n_jobs=nJobs) #, scoring="f1") 
    if tryToMeasureFeatureImportance:
        measureFeatureImportance(clf, featureNames)

    print "Result size = ", len(results)
    print "Done"
    return results

def measureFeatureImportance(classifier, featureNames):
    
    import numpy as np
    importances = classifier.feature_importances_
    std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print "Feature ranking:"

    for f in xrange(len(indices)):
        if featureNames:
            print "%d. feature %s (%f)" % (f + 1, featureNames[indices[f]], importances[indices[f]])
        else:
            print "%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]])
    
    # Plot the feature importances of the forest
    #import pylab as pl
    #pl.figure()
    #pl.title("Feature importances")
    #pl.bar(xrange(len(indices)), importances[indices],
    #          color="r", yerr=std[indices], align="center")
    #pl.xticks(xrange(len(indices)), indices)
    #pl.xlim([-1, len(indices)])
    #pl.show()
