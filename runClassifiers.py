import pickle, sys
import random
#My classes
from classifiers import *
from createFeatureVector import userClass

medicalUserDataSet = "medicalUser.pk"
regularUserDataSet = "regularUser.pk"

def transformeInDict(userDict, n=-1):
    listOfDicts = list()
    listOfLabels = list()
    
    p = range(len(userDict))
    random.shuffle(p)
    
    for v, (key, user) in zip(range(len(p)), userDict.iteritems()):
        if n >= 0 and p[v] >= n:
            continue 
        listOfDicts.append(user.toDict())
        listOfLabels.append(user.label)
    return listOfDicts, listOfLabels

if __name__ == "__main__":

    preProcessing = sys.argv[1]
    forceBalance = sys.argv[2]
    print preProcessing
    if forceBalance:
        print "Forcing only %s examples for each dataset" % (forceBalance)

    ####
    ### Load Datasets
    ##
    #
    print "Loading the datasets..."
    with open(regularUserDataSet, 'rb') as input:
        regularUserFV = pickle.load(input)
    
    with open(medicalUserDataSet, 'rb') as input:
        medicalUserFV = pickle.load(input)
    print "Loaded"

    n = -1
    if int(forceBalance) > 0:
        n = int(forceBalance)

    print "Transforming datasets into Dictionaries..."
    ld1, ll1 = transformeInDict(regularUserFV,n)
    ld2, ll2 = transformeInDict(medicalUserFV,n)
    print "Transformed"
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2
   
    print "Using %d regular users" % ( len(ld1) )
    print "Using %d medical users" % ( len(ld2) )
    avgAcc = 100 * max( [len(ld1), len(ld2)] ) / (len(ld1) + len(ld2))
    print "Avg. accuracy of the greatest dataset => %f" % (avgAcc)

    print "Vectorizing dictionaries..."
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    X_noProcess = vec.fit_transform(listOfDicts).toarray()
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
    else:
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

    parametersSVM = []
    parametersKnn = []
    parametersDT = []

    print "Running classifiers..."
    #TODO: run a logistic regression to evaluate the features and decide which ones are the best ones

    y_nb  = runNB(X, y, nCV)
    y_knn = runKNN(X, y, parametersKnn, nCV)
    y_dt = runDecisionTree(X, y, parametersDT, nCV)
    #y_svm = runSVM(X, y, parametersSVM, nCV)
    print "Done"

    ####
    ### Check Results
    ##
    #
    
    #print 20 * '=', " SVM Results ", 20 * '='
    #makeReport(X, y, y_svm)
    
    print 20 * '=', " NB  Results ", 20 * '='
    makeReport(X, y, y_nb)
    
    print 20 * '=', " KNN Results ", 20 * '='
    makeReport(X, y, y_knn)
    
    print 20 * '=', " DT  Results ", 20 * '='
    makeReport(X, y, y_dt)

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

