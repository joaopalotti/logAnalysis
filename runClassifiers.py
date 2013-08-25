import pickle, sys
import random
import numpy as np
from optparse import OptionParser
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.dummy import DummyClassifier

#My classes
from classifiers import classify, makeReport, plotGraph, getPrecisionRecall, getROC, parallelClassify, getCurves
from auxClassifier import preprocessing, shuffleData, vectorizeData, calculateBaselines
from createFeatureVector import userClass

### HOW TO USE:
# python runClassifiers.py -h
# python runClassifiers.pt --preprocessing=[normalize|scale|minmax|nothing] -b [forceBalance|-1] -g [proportional|-1] -m [minNumberOfQueries] -s [nseed]"

nCV = 10
CSVM = 10000
SVMMaxIter=10000

classifyParameters = {"KNN-K": 100, "ERT-n_estimators": 10, "SVM-cacheSize": 1000, "SVM-kernel": "linear", "SVM-C": CSVM, "SVM-maxIter":SVMMaxIter} 

gridETC = [{'criterion': ['gini','entropy'], 'max_features': ["auto", None, "log2"]}]
gridKNN = [{'n_neighbors': [1,2,3,4,5,10,15,20,50,100], 'algorithm': ["auto", "kd_tree"]}]
gridSVM = [{'C': [1,100000,10000000], 'kernel': ["linear", "rbf","poly"]},\
           {'C': [1,100000,10000000], 'kernel': ["poly"], 'degree':[3,5,10]},\
           {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 1000, 1000000]}]
gridLR = [{'C': [1,1000,10000,10000000], 'penalty': ["l1", "l2"]}]
gridDT = [{'criterion': ["gini","entropy"], 'max_features': ["auto", None, "log2"]}]


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

def runClassify(preProcessingMethod, forceBalance, proportional, minNumberOfQueries, nseed, explanation, healthUsers, gridSearch, generatePickle, hasPlotLibs, paralled, nJobs):
   
    if healthUsers:
        positiveOutputFile = "healthUser-%d-%s.pk" % (minNumberOfQueries, explanation)
        negativeOutputFile = "notHealthUser-%d-%s.pk" % (minNumberOfQueries, explanation)
    else:
        negativeOutputFile = "regularUser-%d-%s.pk" % (minNumberOfQueries, explanation)
        positiveOutputFile = "medicalUser-%d-%s.pk" % (minNumberOfQueries, explanation)
    
    
    print "using seed -> ", nseed
    print "loading: ", positiveOutputFile, "and", negativeOutputFile

    print preProcessingMethod
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
    with open(negativeOutputFile, 'rb') as input:
        negativeUserFV = pickle.load(input)
    
    with open(positiveOutputFile, 'rb') as input:
        positiveUserFV = pickle.load(input)
    print "Loaded"

    print "Transforming datasets into Dictionaries..."
    ld1, ll1 = transformeInDict(negativeUserFV, forceBalance, proportional)
    ld2, ll2 = transformeInDict(positiveUserFV, forceBalance, proportional)
    print "Transformed"
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2
    y = np.array( listOfLabels )
    
    greatestClass = 0 if len(ll1) > len(ll2) else 1
    y_greatest =  np.array((len(ll1) + len(ll2)) * [greatestClass] )

    print "Using %d regular users -- class %s" % (len(ld1), ll1[0])
    print "Using %d medical users -- class %s" % (len(ld2), ll2[0])
    
    baselines = calculateBaselines(y, y_greatest)
    
    print "Vectorizing dictionaries..."
    vec, X_noProcess = vectorizeData(listOfDicts) 
    print vec.get_feature_names()
    print "Vectorized"
   
    print "Preprocessing data"
    X = preprocessing(X_noProcess, preProcessingMethod)
    
    n_samples, n_features = X.shape
    ####
    ### Shuffer samples  (TODO: Cross-validation)
    ##
    #
    
    print "Shuffling the data..."
    X, y = shuffleData(X, y, nseed, n_samples)
    # Shuffle samples
    print "Shuffled"
    
    ####
    ### Run classifiers
    ##
    #
    precRecall, roc = {}, {}
    clfrs = []

    print "Running classifiers..."
    
    dmfc = DummyClassifier(strategy='most_frequent')
    clfrs.append( (dmfc, "DummyMostFrequent", X, y, nCV, nJobs, baselines) )
    # ================================================================
    dsc = DummyClassifier(strategy='stratified')
    clfrs.append( (dsc, "DummyStratified", X, y, nCV, nJobs, baselines) )
    # ================================================================
    duc = DummyClassifier(strategy='uniform')
    clfrs.append( (duc, "DummyUniform", X, y, nCV, nJobs, baselines) )
    # ================================================================
    nbc = GaussianNB()
    clfrs.append( (nbc, "Naive Bayes", X, y, nCV, nJobs, baselines) )
    # ================================================================
    knnc = KNeighborsClassifier(n_neighbors=classifyParameters["KNN-K"])
    clfrs.append( (knnc, "KNN", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridKNN}) )
    # ================================================================
    lrc = LogisticRegression()
    clfrs.append( (lrc, "Logistic Regression", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridLR}) )
    # ================================================================
    dtc = DecisionTreeClassifier()
    clfrs.append( (dtc, "Decision Tree", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridDT}) )
    # ================================================================
    svmc = SVC(kernel=classifyParameters["SVM-kernel"], cache_size=classifyParameters["SVM-cacheSize"], C=classifyParameters["SVM-C"], max_iter=classifyParameters["SVM-maxIter"], probability=True)
    clfrs.append( (svmc, "SVM", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridSVM}) )
    # ================================================================
    etc = ExtraTreesClassifier(random_state=0, n_jobs=nJobs, n_estimators=classifyParameters["ERT-n_estimators"])
    clfrs.append( (etc, "Random Forest", X, y, nCV, nJobs, baselines, {"tryToMeasureFeatureImportance":True, "featureNames":vec.get_feature_names(), "useGridSearch":gridSearch, "gridParameters":gridETC}) )
    
    results = []
    if paralled:
        from scoop import futures
        results = futures.map(parallelClassify,clfrs)
    else:
        results.append(classify(dmfc, "DummyMostFrequent", X, y, nCV, nJobs, baselines))
        results.append(classify(dsc, "DummyStratified", X, y, nCV, nJobs, baselines))
        results.append(classify(duc, "DummyUniform", X, y, nCV, nJobs, baselines))
        results.append(classify(nbc, "Naive Bayes", X, y, nCV, nJobs, baselines))
        results.append(classify(knnc, "KNN", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridKNN}))
        results.append(classify(lrc, "Logistic Regression", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridLR}))
        results.append(classify(dtc, "Decision Tree", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridDT}))
        results.append(classify(svmc, "SVM", X, y, nCV, nJobs, baselines, {"useGridSearch":gridSearch, "gridParameters":gridSVM}))
        results.append(classify(etc, "Random Forest", X, y, nCV, nJobs, baselines, {"tryToMeasureFeatureImportance":True, "featureNames":vec.get_feature_names(), "useGridSearch":gridSearch, "gridParameters":gridETC}))


    precRecall, roc = getCurves(results)
    roc["Random Classifier"] = ([0,1],[0,1])

    plotGraph(precRecall, fileName="precisionAndRecall", xlabel="Recall", ylabel="Precision", generatePickle=generatePickle, hasPlotLibs=hasPlotLibs)
    plotGraph(roc, fileName="ROC", xlabel="False Positive Rate", ylabel="True Positive Rate", generatePickle=generatePickle, hasPlotLibs=hasPlotLibs)
    
    for r in results:
        label = r[0]
        resultMetrics = r[1]
        print "%s, %.3f, %.3f, %.3f, %.3f" % (label, 100.0*resultMetrics.acc, 100.0*resultMetrics.sf1, 100.0*resultMetrics.mf1, 100.0*resultMetrics.wf1)

    print "Done"

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
    op.add_option("--ignorePickle", "-i", action="store_true", dest="ignorePickle", help="Don't Generate Pickle of plots", default=False)
    op.add_option("--useScoop", "-s", action="store_true", dest="useScoop", help="Use Scoop to run classifier in parallel", default=False)
    op.add_option("--njobs", "-j", action="store", type="int", dest="njobs", help="Number of parallel jobs to run.", metavar="X", default=2)

    (opts, args) = op.parse_args()
    if len(args) > 0:
        print "This program does not receive parameters this way: use -h to see the options."
    
    print "Using preprocessing: ", opts.preProcessing
    print "Using ", opts.minNumberOfQueries, "as the minimal number of queries"
    print "Forcing Balance = ",opts.forceBalance
    print "Proportional =",opts.proportional
    print "using grid search =", opts.gridSearch
    print "Has plot libs = ", opts.hasPlotLibs
    print "Generating Pickle = ", not opts.ignorePickle
    print "Running in parallel =", opts.useScoop
    print "Njobs = ", opts.njobs

    runClassify(opts.preProcessing, opts.forceBalance, opts.proportional, opts.minNumberOfQueries, opts.nseed, opts.explanation, opts.healthUsers, opts.gridSearch, not opts.ignorePickle, opts.hasPlotLibs, opts.useScoop, opts.njobs)

