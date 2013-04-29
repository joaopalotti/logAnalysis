from __future__ import division
from itertools import groupby
from collections import Counter, defaultdict 
import sys

#My classes
from readCSV import readMyFormat
from auxiliarFunctions import NLWords, preProcessData, createAcronymSet, symptomTypes, causeTypes, remedyTypes, whereTypes, noMedicalTypes

removeStopWords=False
acronymsSet = createAcronymSet()
minimalNumberOfQueries = 6
maximalNumberOfQueries = 100

class userClass:
    def __init__(self, id, label, nq, ns, mmd, unl, mwpq, mtps, uab, usy, usc, usrd, usnm):
        self.id = id
        self.label = label
        self.numberOfQueries = nq
        self.numberOfSessions = ns
        self.meanMeshDepth = mmd
        self.usingNL = unl
        self.meanWordsPerQuery = mwpq
        self.meanTimePerSession = mtps
        self.usingAbbreviation = uab
        self.usingSymptons = usy
        self.usingCause = usc
        self.usingRemedy = usrd
        self.usingNotMedical = usnm
    
    def toDict(self):
        return {'00.numberOfQueries':self.numberOfQueries, '01.numberOfSessions':self.numberOfSessions, '02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical}
        #TODO: should I consider different kinds of abbreviations?
        #TODO: take a look at the mesh and decide if it is possible to separete levels or groups from their data (same for UMLS)

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

def calculateMeanWordsPerQuery(data):
    mapUserMeanWords = dict()
    userWords = [ (member.userId, len(member.keywords)) for member in data ]
    #print userWords
    
    tempMap = defaultdict(list)
    for (userId, lenght) in userWords:
        tempMap[userId].append(lenght)

    for (userId, listOfLenghts) in tempMap.iteritems():
        meanSize = sum(listOfLenghts)/len(listOfLenghts)
        #print userId, " ---> ",meanSize
        mapUserMeanWords[userId] = meanSize

    return mapUserMeanWords

def calculateNumberOfSessionsPerUser(data):
    userIds = sorted( ( member.userId for member in data if member.previouskeywords is None ) )
    usersNumberOfSessions = [ (k , len(list(g))) for k, g in groupby(userIds) ]
    mapUserSession = dict()
    for u, ns in usersNumberOfSessions:
        mapUserSession[u] = ns
    
    return mapUserSession

def hasSemanticType(words, semanticSet):
    if words is None:
        return False
    return any( [ w for w in words if w.lower() in semanticSet] )

def calculateUsingSemantic(data, semanticType):
    mapUserSemantic = dict()

    userIds = sorted( (member.userId, member.semanticTypes) for member in data )
    for (userId, st) in userIds:
        if userId not in mapUserSemantic:
            mapUserSemantic[userId] = False
        mapUserSemantic[userId] = ( mapUserSemantic[userId] or hasSemanticType(st, semanticType) )
    return mapUserSemantic

def calculateUsingAbbreviation(data):
    mapUserAbb = dict()
    
    userIds = sorted( (member.userId, member.keywords) for member in data )
    
    for (userId, keywords) in userIds:
        if userId not in mapUserAbb:
            mapUserAbb[userId] = False
        mapUserAbb[userId] = ( mapUserAbb[userId] or hasAbbreviation(keywords) )

    #print "mapUserAbb ---> ", mapUserAbb
    return mapUserAbb

def hasAbbreviation(words):
    return any( [ w for w in words if w.lower() in acronymsSet] )

def calculateMeanTimePerSession(data):
    mapUserMeanTimePerSession = dict()
    
    userDateBool = [ ( member.userId, member.datetime , member.previouskeywords is None) for member in data ] # (user, date, newSession? )

    tempMap = defaultdict(list)

    for (user, date, newSession) in userDateBool:
        tempMap[user].append( (date, newSession) )
        #print user, date, newSession

    for (user, dateNewSession) in tempMap.iteritems():
        
        totalSeconds = 0
        numberOfSessions = 0

        startDate = dateNewSession[0][0]
        endDate = startDate
        #print "User ---> ", user, " Start --> ", startDate
        
        for date, newSession in dateNewSession[1:]:
            #Seeks the next session
            if not newSession:
                endDate = date
                continue
            
            # It is a new session:
            else:
                seconds = (endDate - startDate).total_seconds()
                #print "SECONDS --> ", seconds 
               
                # Reset the date limits
                startDate = date
                endDate = date
                
                totalSeconds += seconds
                numberOfSessions += 1
        
        #the last session
        seconds = (endDate - startDate).total_seconds()
        #print "SECONDS --> ", seconds 
        
        totalSeconds += seconds
        numberOfSessions += 1

        
        mapUserMeanTimePerSession[user] = totalSeconds / numberOfSessions
    return mapUserMeanTimePerSession

def createDictOfUsers(data, label):
    userDict = dict()

    users = set( (member.userId for member in data) )
    countingNumberOfQueriesPerUser = calculateNumberOfQueriesPerUser(data)
    countingNumberOfSessionsPerUser = calculateNumberOfSessionsPerUser(data)
    countingMeanMeshDepthPerUser = calculateMeanMeshDepthPerUser(data)
    countingNLPerUser = calculateNLPerUser(data)
    countingWordsPerQuery = calculateMeanWordsPerQuery(data)
    countingMeanTimePerSession = calculateMeanTimePerSession(data)
    countingUsingAbbreviation = calculateUsingAbbreviation(data)
    countingUsingSymptons = calculateUsingSemantic(data, symptomTypes())
    countingUsingCause = calculateUsingSemantic(data, causeTypes())
    countingUsingRemedy = calculateUsingSemantic(data, remedyTypes())
    countingUsingNotMedical = calculateUsingSemantic(data, noMedicalTypes())

    for user in users:
        if user not in countingNumberOfQueriesPerUser or \
           user not in countingNumberOfSessionsPerUser or \
           user not in countingNLPerUser or\
           user not in countingWordsPerQuery or\
           user not in countingMeanTimePerSession:
           #user not in countingMeanMeshDepthPerUser 
            
            print "User is not present. It should be...User ID = ", user
            print "Number of queries -> ", user in countingNumberOfQueriesPerUser
            print "Number of sessions -> ", user in countingNumberOfSessionsPerUser
            print "Mesh -> ", user in countingMeanMeshDepthPerUser
            print "NL -> ", user in countingNLPerUser
            print "WordsPerQuery-> ", user in countingWordsPerQuery
            print "TimePerSession -> ", user in countingMeanTimePerSession

            #sys.exit(0)
            continue

        nq = countingNumberOfQueriesPerUser[user]
        ns = countingNumberOfSessionsPerUser[user]
        mmd = 0.0 if user not in countingMeanMeshDepthPerUser else countingMeanMeshDepthPerUser[user]
        unl = countingNLPerUser[user]
        mwpq = countingWordsPerQuery[user]
        mtps = countingMeanTimePerSession[user]
        uab = countingUsingAbbreviation[user]
        usy = countingUsingSymptons[user]
        usc = countingUsingCause[user]
        usrd = countingUsingRemedy[user]
        usnm = countingUsingNotMedical[user]

        userDict[user] = userClass(user, label, nq=nq, ns=ns, mmd=mmd, unl=unl, mwpq=mwpq, mtps=mtps, uab=uab, usy=usy, usc=usc, usrd=usrd, usnm=usnm)

    return userDict

def createFV(filename, label):
    data = readMyFormat(filename) 
    data = preProcessData(data, removeStopWords)    # Sort the data by user and date
    data = keepUsersInsideLimiteOfQueires(data, minimalNumberOfQueries, maximalNumberOfQueries)
    
    userDict = createDictOfUsers(data, label)
    
    print len(userDict)
    
    return userDict

def keepUsersInsideLimiteOfQueires(data, Xmin, Xmax):
    userIds = sorted( [member.userId for member in data ] ) 
    usersToRemove = [ k for k, g in groupby(userIds) if len(list(g)) < Xmin or len(list(g)) >= Xmax]
    newData = [member for member in data if member.userId not in usersToRemove]
    return newData

def mergeFVs(*fvs):
    counter = 0
    newDict = dict()

    for ofv in fvs:
        for user, fv in ofv.iteritems():
            newDict[ user + "_" + str(counter) ] = fv
        counter += 1

    return newDict


def healthNotHealthUsers():
    
    # 10% of the dataset only
    honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.10.gz", 0)
    aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth.v4.10.gz", 0)
    goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.10.gz", 0)
    tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.10.gz", 0)
    
    # 1% of the dataset only
    notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial.v4.1.gz", 1)

    ### Merge Feature sets and transforme them into inputs
    healthUserFV = mergeFVs(honFV, aolHealthFV, goldMinerFV, tripFV)
    notHealthUserFV = notHealth
    
    ####### Save and Load the Features
    import pickle
    with open('healthUser.pk', 'wb') as output:
        pickle.dump(healthUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: healthUser.pk"
    
    with open('notHealthUser.pk', 'wb') as output:
        pickle.dump(notHealthUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: notHealthUser.pk"

def regularMedicalUsers():
    ####
    ### Load Datasets
    ##
    #
    
    #honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.dataset.gz", 0)
    #aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth.v4.dataset.gz", 0)
    #goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.dataset.gz", 1)
    #tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.dataset.gz", 1)
    
    # 10% of the dataset only
    honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.10.gz", 0)
    aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth.v4.10.gz", 0)
    goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.10.gz", 1)
    tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.10.gz", 1)

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
    
if __name__ == "__main__":
    #regularMedicalUsers()
    healthNotHealthUsers()
