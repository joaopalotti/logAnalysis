import pickle, sys
import random
#My classes
from classifiers import *
from createFeatureVector import userClass

nJobs = 2
nCV = 10

parametersSVM = {"nJobs":nJobs, "CV":nCV, "cacheSize":1000, "kernel":"linear", "C":1.0}
parametersKnn = {"nJobs":nJobs, "CV":nCV, "K":100}
parametersDT = {"nJobs":nJobs, "CV":nCV}
parametersERT = {"nJobs":nJobs, "CV":nCV, "n_estimators":10}
parametersLogReg = {"nJobs":nJobs, "CV":nCV}
parametersNB = {"nJobs":nJobs, "CV":nCV}

medicalUserDataSet = "medicalUser.pk"
regularUserDataSet = "regularUser.pk"

healthUserDataSet = "healthUser.pk"
notHealthUserDataSet = "notHealthUser.pk"

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
        listOfDicts.append(user.toDict())
        listOfLabels.append(user.label)
    return listOfDicts, listOfLabels

if __name__ == "__main__":

    preProcessing = sys.argv[1]
    forceBalance = sys.argv[2]
    proportional = sys.argv[3]

    print preProcessing
    if forceBalance and int(forceBalance) > 0:
        print "Forcing only %s examples for each dataset" % (forceBalance)

    if proportional and int(proportional) > 0:
        print "Using proportional representation. %s percente of the base." % (proportional)
    
    if forceBalance and int(forceBalance) > 0 and proportional and int(proportional):
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
   
    print "Using %d regular users" % ( len(ld1) )
    print "Using %d medical users" % ( len(ld2) )
    baseline = 1.0 * max( [len(ld1), len(ld2)] ) / (len(ld1) + len(ld2))
    print "Avg. accuracy of the greatest dataset => %f" % (100.0 * baseline)

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

    import numpy as np
    y = np.array( listOfLabels )
    
    n_samples, n_features = X.shape

    ####
    ### Shuffer samples  (TODO: Cross-validation)
    ##
    #

    print "Shuffling the data..."
    # Shuffle samples
    p = range(n_samples) 
    random.seed(0)
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

    y_ert = runExtraTreeClassifier(X, y, parametersERT, baseline)
    y_nb  = runNB(X, y, parametersNB, baseline)
    y_knn = runKNN(X, y, parametersKnn, baseline)
    y_dt = runDecisionTree(X, y, parametersDT, baseline)
    y_svm = runSVM(X, y, parametersSVM, baseline)
    y_lg =  runLogRegression(X, y, parametersLogReg, baseline)
    print "Done"

    ####
    ### Check Results
    ##
    #
    print 20 * '=', " SVM Results ", 20 * '='
    makeReport(X, y, y_svm, baseline)
    
    print 20 * '=', " NB  Results ", 20 * '='
    makeReport(X, y, y_nb,baseline)
    
    print 20 * '=', " KNN Results ", 20 * '='
    makeReport(X, y, y_knn,baseline)
    
    print 20 * '=', " DT  Results ", 20 * '='
    makeReport(X, y, y_dt,baseline)

    print 20 * '=', " ERF  Results ", 20 * '='
    makeReport(X, y, y_ert,baseline)
    
    print 20 * '=', " LogReg  Results ", 20 * '='
    makeReport(X, y, y_lg,baseline)
    
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

