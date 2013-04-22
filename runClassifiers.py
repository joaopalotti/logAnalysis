import pickle
#My classes
from classifiers import *
from createFeatureVector import userClass

def transformeInDict(userDict):
    listOfDicts = list()
    listOfLabels = list()
    for key, user  in userDict.iteritems():
        listOfDicts.append( user.toDict() )
        listOfLabels.append( user.label )
    return listOfDicts, listOfLabels

if __name__ == "__main__":

    ####
    ### Load Datasets
    ##
    #
    with open('regularUser.pk', 'rb') as input:
        regularUserFV = pickle.load(input)
    
    with open('medicalUser.pk', 'rb') as input:
        medicalUserFV = pickle.load(input)

    ld1, ll1 = transformeInDict(regularUserFV)
    ld2, ll2 = transformeInDict(medicalUserFV)
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2

    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    X = vec.fit_transform(listOfDicts).toarray()
    
    #TODO: normalize the data
    # http://scikit-learn.org/stable/modules/preprocessing.html

    import numpy as np
    y = np.array( listOfLabels )
    
    n_samples, n_features = X.shape

    ####
    ### Shuffer samples  (TODO: Cross-validation)
    ##
    #

    # Shuffle samples
    import random
    p = range(n_samples) 
    random.seed(0)
    random.shuffle(p)
    X, y = X[p], y[p]
    nCV = 10

    ####
    ### Run classifiers
    ##
    #

    parametersSVM = []
    parametersKnn = []
    parametersDT = []

    y_svm = runSVM(X, y, parametersSVM, nCV)
    y_nb  = runNB(X, y, nCV)
    y_knn = runKNN(X, y, parametersKnn, nCV)
    y_dt = runDecisionTree(X, y, parametersDT, nCV)

    ####
    ### Check Results
    ##
    #
    
    print 20 * '=', " SVM Results ", 20 * '='
    makeReport(X, y, y_svm)
    
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

