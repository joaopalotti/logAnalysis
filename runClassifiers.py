import pickle, sys
import random
import numpy as np
#My classes
from classifiers import *
from createFeatureVector import userClass
from sklearn.metrics import f1_score, accuracy_score

### HOW TO USE:
# python runClassifiers.py [normalize|scale|minmax|nothing] [forceBalance|-1] [proportional|-1] [minNumberOfQueries] [nseed]"

nJobs = 2
nCV = 10
CSVM = 10000

parametersSVM = {"nJobs":nJobs, "CV":nCV, "cacheSize":1000, "kernel":"linear", "C":CSVM}
parametersKnn = {"nJobs":nJobs, "CV":nCV, "K":100}
parametersDT = {"nJobs":nJobs, "CV":nCV}
parametersERT = {"nJobs":nJobs, "CV":nCV, "n_estimators":10}
parametersLogReg = {"nJobs":nJobs, "CV":nCV}
parametersNB = {"nJobs":nJobs, "CV":nCV}


def transformeInDict(userDict, n=-1, proportional=-1):
    listOfDicts = list()
    listOfLabels = list()
   
    p = range(len(userDict))
    random.shuffle(p)
    if proportional:
        n = int( int(proportional)/100.0 * len(userDict) )
    
    for v, (key, user) in zip(range(len(p)), userDict.iteritems()):
        if n >= 0 and p[v] >= n:
            continue 
        udict = user.toDict()
        #print user.label, udict
        listOfDicts.append(udict)
        listOfLabels.append(user.label)
    return listOfDicts, listOfLabels


def runClassify(preProcessing, forceBalance, proportional, minNumberOfQueries, nseed):
   
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

    n = -1
    if int(forceBalance) > 0:
        n = int(forceBalance)

    print "Transforming datasets into Dictionaries..."
    ld1, ll1 = transformeInDict(regularUserFV, n, proportional)
    ld2, ll2 = transformeInDict(medicalUserFV, n, proportional)
    print "Transformed"
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2
    y = np.array( listOfLabels )
    
    greatestClass = 0 if len(ll1) > len(ll2) else 1
    y_greatest =  np.array((len(ll1) + len(ll2)) * [greatestClass] )

    print "Using %d regular users -- class %s" % (len(ld1), ll1[0])
    print "Using %d medical users -- class %s" % (len(ld2), ll2[0])
    
    accBaseline = accuracy_score(y, y_greatest)
    print "Acc baseline --> ", (accBaseline)
    print "Avg. accuracy of the greatest dataset => %.3f" % (100.0 * accBaseline)

    f1 = f1_score( y, y_greatest, average=None)
    print "F1 Score --> ", (f1) , " size --> ", len(f1)
    ns = Counter(y)
    wf1Baseline = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    print "Weighted Mean -> ", wf1Baseline
    f1Baseline = f1.mean()
    print "Simple Mean -> %.3f" % (f1Baseline)

    print "Vectorizing dictionaries..."
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    X_noProcess = vec.fit_transform(listOfDicts).toarray()
    print vec.get_feature_names()
    print "Vectorized"
    
    #TODO: normalize the data
    # http://scikit-learn.org/stable/modules/preprocessing.html
    from sklearn import preprocessing
    if preProcessing == "scale":
        X = preprocessing.scale(X_noProcess)
    elif preProcessing == "minmax":
        X = preprocessing.MinMaxScaler().fit_transform(X_noProcess)
    elif preProcessing == "normalize":
        X = preprocessing.normalize(X_noProcess, norm='l2')
    elif preProcessing == "nothing":
        X = X_noProcess

    
    n_samples, n_features = X.shape
    
    ####
    ### Shuffer samples  (TODO: Cross-validation)
    ##
    #
    
    print "Shuffling the data..."
    # Shuffle samples
    p = range(n_samples) 
    random.seed(nseed)
    random.shuffle(p)
    X, y = X[p], y[p]
    nCV = 5
    print "Shuffled"

    ####
    ### Run classifiers
    ##
    #
    print "Running classifiers..."
    #TODO: run a logistic regression to evaluate the features and decide which ones are the best ones

    y_ert = runExtraTreeClassifier(X, y, parametersERT, accBaseline, f1Baseline, wf1Baseline)
    print 20 * '=', " ERF  Results ", 20 * '='
    ertacc, ertf1, ertwf1 = makeReport(X, y, y_ert, accBaseline, f1Baseline, wf1Baseline)
    
    y_nb  = runNB(X, y, parametersNB,  accBaseline, f1Baseline, wf1Baseline)
    print 20 * '=', " NB  Results ", 20 * '='
    nbacc, nbf1, nbwf1 = makeReport(X, y, y_nb, accBaseline, f1Baseline, wf1Baseline)
    
    y_knn = runKNN(X, y, parametersKnn,  accBaseline, f1Baseline, wf1Baseline)
    print 20 * '=', " KNN Results ", 20 * '='
    knnacc, knnf1, knnwf1 = makeReport(X, y, y_knn, accBaseline, f1Baseline, wf1Baseline)
    
    y_dt = runDecisionTree(X, y, parametersDT,  accBaseline, f1Baseline, wf1Baseline)
    print 20 * '=', " DT  Results ", 20 * '='
    dtacc, dtf1, dtwf1 = makeReport(X, y, y_dt, accBaseline, f1Baseline, wf1Baseline)
    
    y_lg =  runLogRegression(X, y, parametersLogReg,  accBaseline, f1Baseline, wf1Baseline)
    print 20 * '=', " LogReg  Results ", 20 * '='
    lgacc, lgf1, lgwf1 = makeReport(X, y, y_lg, accBaseline, f1Baseline, wf1Baseline)
    
    y_svm = runSVM(X, y, parametersSVM,  accBaseline, f1Baseline, wf1Baseline)
    print 20 * '=', " SVM Results ", 20 * '='
    svmacc, svmwf1, svmwf1 = makeReport(X, y, y_svm,  accBaseline, f1Baseline, wf1Baseline)
    
    print "Done"

    return ( accBaseline, f1Baseline, wf1Baseline, ertacc, ertf1, ertwf1, nbacc, nbf1, nbwf1, knnacc, knnf1, knnwf1, dtacc, dtf1, dtwf1,lgacc, lgf1, lgwf1, svmacc, svmwf1, svmwf1)  
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

    print "HOW TO USE: python runClassifiers.py [normalize|scale|minmax|nothing] [forceBalance|-1] [proportional|-1] [minNumberOfQueries] [nseed]"
    preProcessing = sys.argv[1]
    forceBalance = int(sys.argv[2])
    proportional = int(sys.argv[3])
    minNumberOfQueries = int(sys.argv[4])
    nseed = int(sys.argv[5])
    runClassify(preProcessing, forceBalance, proportional, minNumberOfQueries, nseed) 
