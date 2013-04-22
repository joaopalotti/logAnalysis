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

    ####
    ### Load Datasets
    ##
    #
    
    #honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.dataset.gz", 0)
    #aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth.v4.dataset.gz", 0)
    #goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.dataset.gz", 1)
    #tripFV = createFV("dataSetsOfficials/trip/trip.v4.dataset.gz", 1)

    honFV = createFV("dataSetsOfficials/hon/olds/hon300", 0)                    #   16 users
    aolHealthFV = createFV("dataSetsOfficials/aolHealth/olds/aol100", 0)        # + 22 users  = 38 laymen
    
    goldMinerFV = createFV("dataSetsOfficials/goldminer/olds/gold100", 1)   #   15 users
    tripFV = createFV("dataSetsOfficials/trip/olds/trip200", 1)                 # + 19 users  = 34 Specialist
    
    ####
    ### Merge Feature sets and transforme them into inputs
    ##
    # 
    regularUserFV = mergeFVs(honFV, aolHealthFV)
    medicalUserFV = mergeFVs(tripFV, goldMinerFV)

    ####### Save and Load the Features
    import pickle
    with open('regularUser.pk', 'wb') as output:
        pickle.dump(regularUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: regularUser.pk"
    
    with open('medicalUser.pk', 'wb') as output:
        pickle.dump(medicalUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: medicalUser.pk"
    
