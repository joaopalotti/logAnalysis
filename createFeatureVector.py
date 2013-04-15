from itertools import groupby
from collections import Counter, defaultdict 
import sys
#My classes
from readCSV import readMyFormat
from auxiliarFunctions import NLWords, preProcessData

removeStopWords=False

class userClass:
    def __init__(self, id, label, nq, ns, mmd, unl):
        self.id = id
        self.label = label
        self.numberOfQueries = nq
        self.numberOfSessions = ns
        self.meanMeshDepth = mmd
        self.usingNL = unl
    
    def toDict(self):
        #return {'numberOfQueries':self.numberOfQueries, 'numberOfSessions':self.numberOfSessions, 'usingNL':self.usingNL}
        return {'numberOfQueries':self.numberOfQueries, 'numberOfSessions':self.numberOfSessions, 'usingNL':self.usingNL, 'meanMeshDepth':self.meanMeshDepth}

'''
    Boolean feature.
'''
def calculateNLPerUser(data):
    mapUserNL = dict()
    
    userIds = sorted( (member.userId, member.keywords) for member in data )
    
    for (userId, keywords) in userIds:
        if userId not in mapUserNL:
            mapUserNL[userId] = False
        mapUserNL[userId] = ( mapUserNL[userId] or hasNLword(keywords) )

    #print "mapUserNL ---> ", mapUserNL
    return mapUserNL

def hasNLword(words):

    #print ( [ w for w in words if w.lower() in NLWords ] )
    return any( [ w for w in words if w.lower() in NLWords ] )
    
def calculateMeanMeshDepthPerUser(data):
    mapUserMeanMeshDepth = dict()
    tempMap = defaultdict(list)

    userIds = sorted( (member.userId, member.mesh) for member in data )
    
    for (userId, mesh) in userIds:
        if mesh is not None:
            tempMap[userId] += mesh 

    for (userId, mesh) in tempMap.iteritems():
        #print sum([len(m.split(".")) for m in mesh ])
        #print len(mesh)
        mapUserMeanMeshDepth[userId] = sum( [ len(m.split(".")) for m in mesh ] ) / len(mesh)

    return mapUserMeanMeshDepth

def calculateNumberOfQueriesPerUser(data):
    userIds = sorted( [member.userId for member in data ] ) 
    usersNumberOfQueries = [ (k , len(list(g))) for k, g in groupby(userIds) ]
    mapUserQueries = dict()
    for u, nq in usersNumberOfQueries:
        mapUserQueries[u] = nq
    
    return mapUserQueries

def calculateNumberOfSessionsPerUser(data):
    userIds = sorted( ( member.userId for member in data if member.previouskeywords is None ) )
    usersNumberOfSessions = [ (k , len(list(g))) for k, g in groupby(userIds) ]
    mapUserSession = dict()
    for u, ns in usersNumberOfSessions:
        mapUserSession[u] = ns
    
    return mapUserSession

def createDictOfUsers(data, label):
    userDict = dict()

    users = set( (member.userId for member in data) )
    countingNumberOfQueriesPerUser = calculateNumberOfQueriesPerUser(data)
    countingNumberOfSessionsPerUser = calculateNumberOfSessionsPerUser(data)
    countingMeanMeshDepthPerUser = calculateMeanMeshDepthPerUser(data)
    countingNLPerUser = calculateNLPerUser(data)
    #print countingNLPerUser

    for user in users:
        if user not in countingNumberOfQueriesPerUser or \
           user not in countingNumberOfSessionsPerUser or \
           user not in countingMeanMeshDepthPerUser or\
           user not in countingNLPerUser:

            print "User is not present. It should be..."
            #sys.exit(0)
            continue
        nq = countingNumberOfQueriesPerUser[user]
        ns = countingNumberOfSessionsPerUser[user]
        mmd = countingMeanMeshDepthPerUser[user]
        unl = countingNLPerUser[user]

        userDict[user] = userClass(user, label, nq=nq, ns=ns, mmd=mmd, unl=unl)

    return userDict

def createFV(filename, label):
    data = readMyFormat(filename) 
    data = preProcessData(data, removeStopWords)
    data = removeUsersWithLessThanXQueries(data, 2)
    
    userDict = createDictOfUsers(data, label)
    
    print len(userDict)
    
    return userDict

def removeUsersWithLessThanXQueries(data, X):
    userIds = sorted( [member.userId for member in data ] ) 
    usersToRemove = [ k for k, g in groupby(userIds) if len(list(g)) < X]
    newData = [member for member in data if member.userId not in usersToRemove]
    return newData

def transformeInDict(userDict):
    listOfDicts = list()
    listOfLabels = list()
    for key, user  in userDict.iteritems():
        listOfDicts.append( user.toDict() )
        listOfLabels.append( user.label )
    return listOfDicts, listOfLabels

def mergeFVs(FVa, FVb, *otherFVs):
    counter = 0
    newDict = dict()

    for user, fv in FVa.iteritems():
        newDict[ user + "_" + str(counter) ] = fv
    
    counter += 1
    for user, fv in FVb.iteritems():
        newDict[ user + "_" + str(counter) ] = fv
    
    for ofv in otherFVs:
        counter += 1
        for user, fv in ofv.iteritems():
            newDict[ user + "_" + str(counter) ] = fv

    return newDict

if __name__ == "__main__":

    goldMinerUserFV = createFV("dataSetsOfficials/goldminer/olds/gold100", 1)
    aolHealthFV = createFV("dataSetsOfficials/aolHealth/olds/aol100", 1)
    honFV = createFV("dataSetsOfficials/hon/olds/hon100", 0)
    tripFV = createFV("dataSetsOfficials/trip/olds/trip100", 1)
    
    regularUserFV = mergeFVs(honFV, aolHealthFV)
    medicalUserFV = mergeFVs(tripFV, goldMinerUserFV)

    ld1, ll1 = transformeInDict(regularUserFV)
    ld2, ll2 = transformeInDict(medicalUserFV)
    
    listOfDicts = ld1 + ld2
    listOfLabels = ll1 + ll2

    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    X = vec.fit_transform(listOfDicts)
    
    import numpy as np
    y = np.array( listOfLabels )
    
    n_samples, n_features = X.shape

    # Shuffle samples
    import random
    p = range(n_samples) 
    random.seed(0)
    random.shuffle(p)
    X, y = X[p], y[p]

    from sklearn import svm
    # Run classifier
    classifier = svm.SVC(kernel='linear', probability=True)
    half = int(n_samples / 2)
    probas_ = classifier.fit(X[:half], y[:half]).predict_proba(X[half:])

    from sklearn.metrics import precision_recall_curve
    from sklearn.metrics import auc
    # Compute Precision-Recall and plot curve
    precision, recall, thresholds = precision_recall_curve(y[half:], probas_[:, 1])
    area = auc(recall, precision)
    print "Area Under Curve: %0.2f" % area
    #print "Precision %0.2f - Recall %0.2f" % (precision, recall)

    import pylab as pl
    pl.clf()
    pl.plot(recall, precision, label='Precision-Recall curve')
    pl.xlabel('Recall')
    pl.ylabel('Precision')
    pl.ylim([0.0, 1.05])
    pl.xlim([0.0, 1.0])
    pl.title('Precision-Recall example: AUC=%0.2f' % area)
    pl.legend(loc="lower left")
    #pl.show()

    # using a naive bayes classifier 
    # http://scikit-learn.org/stable/modules/naive_bayes.html#naive-bayes
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    y_pred = classifier.fit(X[:half], y[:half]).predict(X[half:])
   
    # Classification report
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    from sklearn.metrics import classification_report
    #y_true = [0, 1, 2, 2, 0]
    #y_pred = [0, 0, 2, 2, 0]
    target_names = ['Layman', 'Specialist']
    print(classification_report( y[half:], y_pred, target_names=target_names))


