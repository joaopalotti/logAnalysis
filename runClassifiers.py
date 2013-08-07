import pickle, sys
import random
import numpy as np
from optparse import OptionParser
from collections import Counter
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier

#My classes
from classifiers import classify, makeReport, plot_precision_recall
from auxClassifier import *
from createFeatureVector import userClass
from sklearn.metrics import f1_score, accuracy_score

### HOW TO USE:
# python runClassifiers.py -h
# python runClassifiers.pt --preprocessing=[normalize|scale|minmax|nothing] -b [forceBalance|-1] -g [proportional|-1] -m [minNumberOfQueries] -s [nseed]"

nJobs = 2
nCV = 10
CSVM = 10000

classifyParameters = {"KNN-K": 100, "ERT-n_estimators": 10, "SVM-cacheSize": 1000, "SVM-kernel": "linear", "SVM-C": CSVM} 


def transformeInDict(userDict, n=-1, proportional=-1):
    listOfDicts = list()
    listOfLabels = list()

    p = range(len(userDict))
    random.shuffle(p)
    if proportional > 0:
        n = int( int(proportional)/100.0 * len(userDict) )

    for v, (key, user) in zip(p, userDict.iteritems()):
        if n >= 0 and v >= n:
            continue 
        udict = user.toDict()
        listOfDicts.append(udict)
        listOfLabels.append(user.label)
        #print user.label, udict
        #print udict  #### Check how this features are related with the features calculated by the random tree method
    return listOfDicts, listOfLabels


def runClassify(preProcessingMethod, forceBalance, proportional, minNumberOfQueries, nseed):
   
    medicalUserDataSet = "medicalUser-%d.pk" % (minNumberOfQueries)
    regularUserDataSet = "regularUser-%d.pk" % (minNumberOfQueries)
    
    healthUserDataSet = "healthUser-%d.pk"   % (minNumberOfQueries)
    notHealthUserDataSet = "notHealthUser-%d.pk" % (minNumberOfQueries)

    print "using seed -> ", nseed

    print preProcessing
    if forceBalance > 0:
        print "Forcing only %s examples for each dataset" % (forceBalance)

    if proportional > 0:
        print "Using proportional representation. %s percente of the base." % (proportional)
    
    if forceBalance > 0 and proportional > 0:
        print "ERROR! YOU SHOULD CHOOSE OR FORCEBALANCE OR PROPORTIONAL DATA!"

    ####
    ### Load Datasets
    ##
    #
    print "Loading the datasets..."
    with open(regularUserDataSet, 'rb') as input:
    #with open(notHealthUserDataSet, 'rb') as input:
        regularUserFV = pickle.load(input)
    
    with open(medicalUserDataSet, 'rb') as input:
    #with open(healthUserDataSet, 'rb') as input:
        medicalUserFV = pickle.load(input)
    print "Loaded"

    print "Transforming datasets into Dictionaries..."
    ld1, ll1 = transformeInDict(regularUserFV, forceBalance, proportional)
    ld2, ll2 = transformeInDict(medicalUserFV, forceBalance, proportional)
    print "Transformed"
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2
    y = np.array( listOfLabels )
    
    greatestClass = 0 if len(ll1) > len(ll2) else 1
    y_greatest =  np.array((len(ll1) + len(ll2)) * [greatestClass] )

    print "Using %d regular users -- class %s" % (len(ld1), ll1[0])
    print "Using %d medical users -- class %s" % (len(ld2), ll2[0])
     
    accBaseline = accuracy_score(y, y_greatest)
    print "Avg. ACC of the greatest dataset => %.3f" % (100.0 * accBaseline)

    f1 = f1_score(y, y_greatest, average=None)
    print "F1 Score --> ", (f1) , " size --> ", len(f1)
    
    sf1Baseline = f1_score(y, y_greatest) # TODO: maybe? , pos_label=greatestClass)
    print "Simple F1 -> %.3f" % (sf1Baseline)
    
    mf1Baseline = f1.mean()
    print "Mean F1 -> %.3f" % (mf1Baseline)
    
    ns = Counter(y)
    wf1Baseline = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    print "Weighted F1 -> ", wf1Baseline

    print "Vectorizing dictionaries..."
    vec, X_noProcess = vectorizeData(listOfDicts) 
    print vec.get_feature_names()
    print "Vectorized"
   
    print "Preprocessing data"
    preProcessing(X_noProcess, preProcessingMethod)
    
    n_samples, n_features = X.shape
    ####
    ### Shuffer samples  (TODO: Cross-validation)
    ##
    #
    
    print "Shuffling the data..."
    shuffleData(X, y, nseed, n_samples)
    # Shuffle samples
    print "Shuffled"
    
    nCV = 5

    ####
    ### Run classifiers
    ##
    #
    print "Running classifiers..."
    #TODO: run a logistic regression to evaluate the features and decide which ones are the best ones
    
    y_ert,ert_probas = classify(ExtraTreesClassifier(random_state=0, compute_importances=True, n_jobs=nJobs, n_estimators=classifyParameters["ERT-n_estimators"]), \
                     X, y, nCV, nJobs, tryToMeasureFeatureImportance=True, featureNames=vec.get_feature_names())
    print 20 * '=', " ERF  Results ", 20 * '='
    ertacc, ertsf1, ertwf1, ertmf1 = makeReport(X, y, y_ert, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)
    plot_precision_recall(y, ert_probas)
    
    y_nb, nb_probas  = classify(GaussianNB(),\
                     X, y, nCV, nJobs)
    print 20 * '=', " NB  Results ", 20 * '='
    nbacc, nbsf1, nbwf1, nbmf1 = makeReport(X, y, y_nb, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)
    plot_precision_recall(y, nb_probas)
    
    y_knn, knn_probas = classify(KNeighborsClassifier(n_neighbors=classifyParameters["KNN-K"]),\
                     X, y, nCV, nJobs)
    print 20 * '=', " KNN Results ", 20 * '='
    knnacc, knnsf1, knnwf1, knnmf1 = makeReport(X, y, y_knn, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)
    plot_precision_recall(y, knn_probas)
    
    y_dt, dt_probas = classify(DecisionTreeClassifier(random_state=0, compute_importances=True),\
                    X, y, nCV, nJobs)
    print 20 * '=', " DT  Results ", 20 * '='
    dtacc, dtsf1, dtwf1, dtwmf1 = makeReport(X, y, y_dt, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)
    plot_precision_recall(y, dt_probas)
    
    y_lg, lg_probas =  classify(LogisticRegression(),\
                     X, y, nCV, nJobs)
    print 20 * '=', " LogReg  Results ", 20 * '='
    lgacc, lgsf1, lgwf1, lgmf1 = makeReport(X, y, y_lg, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)
    plot_precision_recall(y, lg_probas)
    
    y_svm, svm_probas = classify(SVC(kernel=classifyParameters["SVM-kernel"], cache_size=classifyParameters["SVM-cacheSize"], C=classifyParameters["SVM-C"]),\
                     X, y, nCV, nJobs)
    print 20 * '=', " SVM Results ", 20 * '='
    svmacc, svmsf1, svmwf1, svmmf1 = makeReport(X, y, y_svm, accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)
    plot_precision_recall(y, svm_probas)
    
    print "Done"

    return ( accBaseline, sf1Baseline, mf1Baseline, wf1Baseline, ertacc, ertsf1, ertwf1, nbacc, nbsf1, nbwf1, knnacc, knnsf1, knnwf1, dtacc, dtsf1, dtwf1, lgacc, lgsf1, lgwf1, svmacc, svmsf1, svmwf1)  
    #import pylab as pl
    #pl.clf()
    #pl.plot(recall, precision, label='Precision-Recall curve')
    #pl.xlabel('Recall')
    #pl.ylabel('Precision')
    #pl.ylim([0.0, 1.05])
    #pl.xlim([0.0, 1.0])
    #pl.title('Precision-Recall example: AUC=%0.2f' % area)
    #pl.legend(loc="lower left")
    #pl.show()

if __name__ == "__main__":
    
    op = OptionParser(version="%prog 2")
    op.add_option("--preprocessing", "-p", action="store", type="string", dest="preProcessing", help="Preprocessing option [normalize|scale|minmax|nothing] --  [default: %default]", metavar="OPT", default="normalize")
    op.add_option("--forceBalance", "-b", action="store", type="int", dest="forceBalance", help="Force balance keeping only X instances of each class.", metavar="X", default=-1)
    op.add_option("--proportional", "-g", action="store", type="int", dest="proportional", help="Force proportion of the data to X%.", metavar="X", default=-1)
    op.add_option("--minNumberOfQueries", "-m", action="store", type="int", dest="minNumberOfQueries", help="Define the min. number of queries (X) necessary to use a user for classification.  [default: %default]", metavar="X", default=5)
    op.add_option("--nseed", "-s", action="store", type="int", dest="nseed", help="Seed used for random processing during classification.  [default: %default]", metavar="X", default=29)

    (opts, args) = op.parse_args()
    if len(args) > 0:
        print "This program does not receive parameters this way: use -h to see the options."
    
    print "Using preprocessing: ", opts.preProcessing
    print "Using ", opts.minNumberOfQueries, "as the minimal number of queries"
    print "Forcing Balance = ",opts.forceBalance
    print "Proportional =",opts.proportional

    runClassify(opts.preProcessing, opts.forceBalance, opts.proportional, opts.minNumberOfQueries, opts.nseed)

