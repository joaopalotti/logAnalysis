from __future__ import division

import pickle, sys
import random
import numpy as np
from optparse import OptionParser
from collections import defaultdict
import logging

#classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.dummy import DummyClassifier

#My classes
from classifiers import classify, plotGraph, parallelClassify, getCurves
from auxClassifier import preprocessing, shuffleData, vectorizeData, calculateBaselines #, getSubLists
from createFeatureVector import userClass

### HOW TO USE:
# python runClassifiers.py -h
# python runClassifiers.pt --preprocessing=[normalize|scale|minmax|nothing] -b [forceBalance|-1] -g [proportional|-1] -m [minNumberOfQueries] -s [nseed]"

#TODO: create a parameter for this flag
useIntegral = True

nCV = 10
CSVM = 10000
SVMMaxIter=10000

classifyParameters = {"KNN-K": 20, "ETC-n_estimators": 120, "SVM-cacheSize": 2000, "SVM-kernel": "rbf", "SVM-C": CSVM, "SVM-maxIter":SVMMaxIter, "SVM-gamma":0.0001, "LR-C":1000, "ETC-criterion": "entropy", "ETC-max_features":None, "DT-criterion": "entropy", "DT-max_features":None} 

gridETC = [{'criterion': ['entropy'], 'max_features': [None], "n_estimators":[10,100,1000,10000]}]
gridKNN = [{'n_neighbors': [1,5,10,15,20,50,100], 'algorithm': ["auto"]}]
gridLR = [{'C': [1,1000,10000,10000000], 'penalty': ["l1", "l2"]}]
gridDT = [{'criterion': ["gini","entropy"], 'max_features': ["auto", None, "log2"]}]
gridSVM = [{'kernel': ['rbf'], 'gamma': [100, 10, 1, 0, 1e-3, 1e-4, 1e-6], 'C': [1000000]}]

percentageIntervals = [0,10,20,30,40,50,60,70,80,90,100]

def transformeInDict(userDict, n=-1, proportional=-1, groupsToUse=None):
    listOfDicts = list()
    listOfLabels = list()

    p = range(len(userDict))
    random.shuffle(p)
    if proportional > 0:
        n = int( int(proportional)/100.0 * len(userDict) )

    for v, (_, user) in zip(p, userDict.iteritems()):
        if n >= 0 and v >= n:
            continue 
        udict = user.toDict(user.numberOfQueries - 1, groupsToUse)
        listOfDicts.append(udict)
        listOfLabels.append(user.label)
        #print user.label, udict
        #print udict  #### Check how this features are related with the features calculated by the random tree method
    return listOfDicts, listOfLabels

def transformeInIncrementalDict(userDict, n=-1, proportional=-1, groupsToUse=None, method="percentage", values=[10,20,50,100]):
    listOfLastQueries = list() # the last query has the "accumlated value for a user"
    listOfLabels = list()
    
    mapOfDicts = defaultdict(list)
    allUserIds = sorted([u for u in userDict])

    p = range(len(allUserIds))
    random.shuffle(p)
    if proportional > 0:
        n = int( int(proportional)/100.0 * len(allUserIds) )

    #for v, (key, userId) in zip(p, userDict.iteritems()):
    for v, userId in zip(p, allUserIds):
        if n >= 0 and v >= n:
            continue 

        #print v, userId
        userc = userDict[userId]

        nq = userc.numberOfQueries - 1
        #print userId, nq

        for i, v in zip(range(len(values)), values):
            idxq = int(nq * (v/100.0))
            #idxq = 1 if idxq == 0 else idxq
            #print v, idxq

            intermediateList = userc.toDict(idxq, groupsToUse)
            mapOfDicts[i].append(intermediateList)

            #if method == "percentage":
            #result[i].append(subList[int((len(subList) - 1) * (v/100.0))].toDict(groupsToUse))
            #print len(subList), v, int(len(subList) * (v/100.0) )

        listOfLastQueries.append(userc.toDict(nq, groupsToUse))
        listOfLabels.append(userc.label)

    #Returning a list of list of queries of a single user and list of labels
    return listOfLastQueries, mapOfDicts, listOfLabels


def runClassify(preProcessingMethod, forceBalance, proportional, minNumberOfQueries, nseed, explanation, healthUsers, gridSearch, generatePickle, hasPlotLibs, paralled, nJobs, listOfClassifiers, groupsToUse, usingIncremental):
   
    if healthUsers:
        positiveOutputFile = "healthUser-%d-%s.pk" % (minNumberOfQueries, explanation)
        negativeOutputFile = "notHealthUser-%d-%s.pk" % (minNumberOfQueries, explanation)
    else:
        negativeOutputFile = "regularUser-%d-%s.pk" % (minNumberOfQueries, explanation)
        positiveOutputFile = "medicalUser-%d-%s.pk" % (minNumberOfQueries, explanation)
    
    logging.info("Using seed: %d", nseed)
    logging.info("Loading: %s and %s", positiveOutputFile, negativeOutputFile)
    logging.info("Processing method used: %s", preProcessingMethod)

    if forceBalance > 0:
        logging.warning("Forcing only %s examples for each dataset",forceBalance)

    if proportional > 0:
        logging.warning("Using proportional representation. %s percente of the base.",proportional)
    
    if forceBalance > 0 and proportional > 0:
        logging.error("ERROR! YOU SHOULD CHOOSE OR FORCEBALANCE OR PROPORTIONAL DATA!")
        print "ERROR! YOU SHOULD CHOOSE OR FORCEBALANCE OR PROPORTIONAL DATA!"
        exit(0)

    ####
    ### Load Datasets
    ##
    #
    logging.info("Loading the datasets...")
    with open(negativeOutputFile, 'rb') as input:
        negativeUserFV = pickle.load(input)
    
    with open(positiveOutputFile, 'rb') as input:
        positiveUserFV = pickle.load(input)
    logging.info("Loaded")

    logging.info("Transforming datasets into Dictionaries...")
    if usingIncremental:
        ld1, mapOfListOfQueries1, ll1 = transformeInIncrementalDict(negativeUserFV, forceBalance, proportional, groupsToUse, "percentage", percentageIntervals)
        ld2, mapOfListOfQueries2, ll2 = transformeInIncrementalDict(positiveUserFV, forceBalance, proportional, groupsToUse, "percentage", percentageIntervals)
       
        lm1 = len(mapOfListOfQueries1)
        if lm1 != len(mapOfListOfQueries2):
            logging.error("ERROR MAP SIZES ARE NOT EQUAL!")
            print "ERROR MAP SIZES ARE NOT EQUAL!"
            exit(0)

        mergedLists = defaultdict(list)
        for i in range(lm1):
            mergedLists[i] = mapOfListOfQueries1[i] + mapOfListOfQueries2[i]

            #print "1 ------------------> ", len(mapOfListOfQueries1[i])
            #print "2 ------------------> ", len(mapOfListOfQueries2[i])
            #print "merged ------------------> ", len(mergedLists[i])

        #listOfListsOfQueries = np.array(listOfListOfQueries1 + listOfListOfQueries2)
        #listOfListsOfQueries = listOfListOfQueries1 + listOfListOfQueries2
        #print "LLQ -> ", listOfListsOfQueries
        #print "ld -> ", ld1 + ld2

    else:
        ld1, ll1 = transformeInDict(negativeUserFV, forceBalance, proportional, groupsToUse)
        ld2, ll2 = transformeInDict(positiveUserFV, forceBalance, proportional, groupsToUse)
    logging.info("Transformed")
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2
    y = np.array( listOfLabels )
    
    greatestClass = 0 if len(ll1) > len(ll2) else 1
    y_greatest =  np.array((len(ll1) + len(ll2)) * [greatestClass] )

    logging.info("Using %d regular users -- class %s" % (len(ld1), ll1[0]))
    logging.info("Using %d medical users -- class %s" % (len(ld2), ll2[0]))
    
    baselines = calculateBaselines(y, y_greatest)
    
    logging.info("Vectorizing dictionaries...")
    vec, X_noProcess = vectorizeData(listOfDicts) 
    logging.info("Feature Names: %s", vec.get_feature_names())
    logging.info("Vectorized")
   
    logging.info("Preprocessing data")
    X = preprocessing(X_noProcess, preProcessingMethod)
    #print "X_noProcess ----> ", X_noProcess
    #print "X ---> ", X
    logging.info("Data preprocessed")

    if usingIncremental:
    #    if useIntegral:
    #        incrementalFV = getSubLists(listOfListsOfQueries, "integral", range(0,5), vec, preProcessingMethod, groupsToUse)
    #    else:
        #incrementalFV = getSubLists(listOfListsOfQueries, "percentage", percentageIntervals, vec, preProcessingMethod, groupsToUse)
        incrementalFV = [preprocessing(vec.fit_transform(l).toarray(), preProcessingMethod) for k, l in mergedLists.iteritems()]
        #print "incrementalFV ---> ", incrementalFV
    else:
        incrementalFV = None

    n_samples, n_features = X.shape
    ####
    ### Shuffer samples  (TODO: Cross-validation)
    ##
    #
    
    logging.info("Shuffling the data...")
    X, y = shuffleData(X, y, nseed, n_samples)
    # Shuffle samples
    logging.info("Shuffled")
    
    ####
    ### Run classifiers
    ##
    #
    precRecall, roc = {}, {}
    clfrs = []

    logging.info("Running classifiers...")
    
    if "dmfc" in listOfClassifiers:
        dmfc = DummyClassifier(strategy='most_frequent')
        clfrs.append( (dmfc, "DummyMostFrequent", X, y, nCV, nJobs, baselines) )
    # ================================================================
    if "dsc" in listOfClassifiers:
        dsc = DummyClassifier(strategy='stratified')
        clfrs.append( (dsc, "DummyStratified", X, y, nCV, nJobs, baselines) )
    # ================================================================
    if "duc" in listOfClassifiers:
        duc = DummyClassifier(strategy='uniform')
        clfrs.append( (duc, "DummyUniform", X, y, nCV, nJobs, baselines) )
    # ================================================================
    if "nbc" in listOfClassifiers:
        nbc = GaussianNB()
        clfrs.append( (nbc, "Naive Bayes", X, y, nCV, nJobs, baselines) )
    # ================================================================
    if "knnc" in listOfClassifiers:
        knnc = KNeighborsClassifier(n_neighbors=classifyParameters["KNN-K"])
        clfrs.append( (knnc, "KNN", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridKNN}) )
    # ================================================================
    if "lrc" in listOfClassifiers:
        lrc = LogisticRegression(C=classifyParameters["LR-C"])
        clfrs.append( (lrc, "Logistic Regression", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridLR}) )
    # ================================================================
    if "dtc" in listOfClassifiers:
        dtc = DecisionTreeClassifier( criterion=classifyParameters["DT-criterion"], max_features=classifyParameters["DT-max_features"] )
        clfrs.append( (dtc, "Decision Tree", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridDT}) )
    # ================================================================
    if "svmc" in listOfClassifiers:
        svmc = SVC(kernel=classifyParameters["SVM-kernel"], cache_size=classifyParameters["SVM-cacheSize"], C=classifyParameters["SVM-C"], max_iter=classifyParameters["SVM-maxIter"], probability=True, gamma=classifyParameters["SVM-gamma"])
        clfrs.append( (svmc, "SVM", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridSVM}) )
    # ================================================================
    if "etc" in listOfClassifiers:
        etc = ExtraTreesClassifier(random_state=0, n_jobs=nJobs, n_estimators=classifyParameters["ETC-n_estimators"], criterion=classifyParameters["ETC-criterion"], max_features=classifyParameters["ETC-max_features"])
        clfrs.append( (etc, "Random Forest", X, y, nCV, nJobs, baselines, {"tryToMeasureFeatureImportance":True, "featureNames":vec.get_feature_names(), "useGridSearch":gridSearch, "gridParameters":gridETC}) )
    
    results = []
    if paralled:
        from scoop import futures
        results = futures.map(parallelClassify,clfrs)
    else:
        if "dmfc" in listOfClassifiers:
            results.append(classify(dmfc, "DummyMostFrequent", X, y, nCV, nJobs, baselines, incremental=incrementalFV))
        if "dsc" in listOfClassifiers:
            results.append(classify(dsc, "DummyStratified", X, y, nCV, nJobs, baselines, incremental=incrementalFV))
        if "duc" in listOfClassifiers:
            results.append(classify(duc, "DummyUniform", X, y, nCV, nJobs, baselines, incremental=incrementalFV))
        if "nbc" in listOfClassifiers:
            results.append(classify(nbc, "Naive Bayes", X, y, nCV, nJobs, baselines, incremental=incrementalFV))
        if "knnc" in listOfClassifiers:
            results.append(classify(knnc, "KNN", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridKNN}, incremental=incrementalFV))
        if "lrc" in listOfClassifiers:
            results.append(classify(lrc, "Logistic Regression", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridLR}, incremental=incrementalFV))
        if "dtc" in listOfClassifiers:
            results.append(classify(dtc, "Decision Tree", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridDT}, incremental=incrementalFV))
        if "svmc" in listOfClassifiers:
            results.append(classify(svmc, "SVM", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridSVM}, incremental=incrementalFV))
        if "etc" in listOfClassifiers:
            results.append(classify(etc, "Random Forest", X, y, nCV, nJobs, baselines, {"tryToMeasureFeatureImportance":True, "featureNames":vec.get_feature_names(), "useGridSearch":gridSearch, "gridParameters":gridETC}, incremental=incrementalFV))

    precRecall, roc = getCurves(results)
    roc["Random Classifier"] = ([0,1],[0,1])

    plotGraph(precRecall, fileName="officialPR-DT", xlabel="Recall", ylabel="Precision", generatePickle=generatePickle, hasPlotLibs=hasPlotLibs)
    plotGraph(roc, fileName="officialROC-DT", xlabel="False Positive Rate", ylabel="True Positive Rate", generatePickle=generatePickle, hasPlotLibs=hasPlotLibs)
    
    for r in results:
        label = r[0]
        resultMetrics = r[1]
        if usingIncremental:
            for i in range(len(resultMetrics.acc)):
                print "Partition %d, %s, %.3f, %.3f, %.3f, %.3f" % (i, label, 100.0*(resultMetrics.acc[i]), 100.0*resultMetrics.sf1[i], 100.0*resultMetrics.mf1[i], 100.0*resultMetrics.wf1[i])
            
            print "Means ----- %s, %.3f, %.3f, %.3f, %.3f" % (label, 100.0*(np.mean(resultMetrics.acc)), 100.0*np.mean(resultMetrics.sf1), 100.0*np.mean(resultMetrics.mf1), 100.0*np.mean(resultMetrics.wf1))
        else:
            print "%s, %.3f, %.3f, %.3f, %.3f" % (label, 100.0*resultMetrics.acc, 100.0*resultMetrics.sf1, 100.0*resultMetrics.mf1, 100.0*resultMetrics.wf1)

    logging.info("Done")

if __name__ == "__main__":
    
    op = OptionParser(version="%prog 2")
    op.add_option("--preprocessing", "-p", action="store", type="string", dest="preProcessing", help="Preprocessing option [normalize|scale|minmax|nothing] --  [default: %default]", metavar="OPT", default="normalize")
    op.add_option("--forceBalance", "-b", action="store", type="int", dest="forceBalance", help="Force balance keeping only X instances of each class.", metavar="X", default=-1)
    op.add_option("--proportional", "-q", action="store", type="int", dest="proportional", help="Force proportion of the data to X%.", metavar="X", default=-1)
    op.add_option("--minNumberOfQueries", "-m", action="store", type="int", dest="minNumberOfQueries", help="Define the min. number of queries (X) necessary to use a user for classification.  [default: %default]", metavar="X", default=5)
    op.add_option("--nseed", "-n", action="store", type="int", dest="nseed", help="Seed used for random processing during classification.  [default: %default]", metavar="X", default=29)
    op.add_option("--explanation", "-e", action="store", type="string", dest="explanation", help="Prefix to include in the created files", metavar="TEXT", default="")
    op.add_option("--healthUsers", "-u", action="store_true", dest="healthUsers", help="Use if you want to create a health/not health user feature file", default=False)
    op.add_option("--gridSearch", "-g", action="store_true", dest="gridSearch", help="Use if you want to use grid search to find the best hyperparameters", default=False)
    op.add_option("--hasPlotLibs", "-c", action="store_true", dest="hasPlotLibs", help="Use if you want to plot Precision Vs Recall and ROC curves", default=False)
    op.add_option("--ignorePickle", "-k", action="store_true", dest="ignorePickle", help="Don't Generate Pickle of plots", default=False)
    op.add_option("--useScoop", "-s", action="store_true", dest="useScoop", help="Use Scoop to run classifier in parallel", default=False)
    op.add_option("--njobs", "-j", action="store", type="int", dest="njobs", help="Number of parallel jobs to run.", metavar="X", default=2)
    op.add_option("--classifiers", "-z", action="store", type="string", dest="classifiers", help="Classifiers to run. Options are dmfc|dsc|duc|nbc|knnc|lrc|dtc|svmc|etc", metavar="cl1|cl2|..", default="dmfc|dsc|duc|nbc|knnc|lrc|dtc|svmc|etc")
    op.add_option("--groupsToUse", "-d", action="store", type="string", dest="groupsToUse", help="Options are: g1 | g2 | ... | g7", metavar="G")
    op.add_option("--usingIncremental", "-i", action="store_true", dest="usingIncremental", help="Use incremental feature vector")
    op.add_option("--loglevel", "-l", action="store", type="string", dest="loglevel", help="Log level to use (INFO, WARNING, DEBUG, CRITICAL, ERROR", default="INFO")

    (opts, args) = op.parse_args()
    if len(args) > 0:
        print "This program does not receive parameters this way: use -h to see the options."
   

    logger = logging.getLogger('runClassify.py')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s --- %(message)s', level=opts.loglevel.upper())

    logging.info("Using Preprocessing: %s", opts.preProcessing)
    logging.info("Minimal number of queries: %d", opts.minNumberOfQueries)
    logging.info("Forcing Balance: %d", opts.forceBalance)
    logging.info("Proportional: %d", opts.proportional)
    logging.info("Using Grid Search: %d", opts.gridSearch)
    logging.info("Has plot libs: %d", opts.hasPlotLibs)
    logging.info("Generating Pickle = %d", not opts.ignorePickle)
    logging.info("Running in parallel = %d", opts.useScoop)
    logging.info("Njobs = %d", opts.njobs)
    logging.info("Classifiers = %s", opts.classifiers)
    listOfClassifiers = opts.classifiers.split("|")
    
    if not opts.groupsToUse:
        print " -------- Please, use a feature set: (Ex. g1, g2...g7)"
        op.print_help()
        sys.exit(0)
    listOfGroupsToUse = opts.groupsToUse.split("|")
    
    runClassify(opts.preProcessing, opts.forceBalance, opts.proportional, opts.minNumberOfQueries, opts.nseed, opts.explanation, opts.healthUsers, opts.gridSearch, not opts.ignorePickle, opts.hasPlotLibs, opts.useScoop, opts.njobs, listOfClassifiers, listOfGroupsToUse, opts.usingIncremental)

