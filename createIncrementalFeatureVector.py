from __future__ import division
from itertools import groupby
from collections import Counter, defaultdict 
import sys

#My classes
from readCSV import readMyFormat
from auxiliarFunctions import NLWords, preProcessData, createAcronymSet, symptomTypes, causeTypes, remedyTypes, whereTypes, noMedicalTypes, compareSets
from statistics import createSessions

removeStopWords=False
acronymsSet = createAcronymSet()
minimalNumberOfQueries = "Invalid number...please enter this parameter!"
maximalNumberOfQueries = 100

### HOW TO USE:
#   python createFeatureVector.py minimalNumberOfQueries 

class userClass:
    def __init__(self, id, label, queryCounter, nq, ns, mmd, unl, mwpq, mtps, uab, usy, usc, usrd, usnm, expa, shri, refo, expshr, expref, shrref, expshrref):
        self.id = id
        self.label = label
        self.queryCounter = queryCounter
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

        self.expansion = expa
        self.shrinkage = shri
        self.reformulation = refo
        self.expshr = expshr
        self.expref = expref
        self.shrref = shrref
        self.expshrref = expshrref

    def toDict(self):
        #return {'00.numberOfQueries':self.numberOfQueries, '01.numberOfSessions':self.numberOfSessions, '02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical}
        return {'-1.queryCounter':self.queryCounter, '00.numberOfQueries':self.numberOfQueries, '01.numberOfSessions':self.numberOfSessions, '02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical, '11.didExpansion': self.expansion ,'12.didShrinkage': self.shrinkage ,'13.didReformulation': self.reformulation , '14.didExpShrRef':self.expshrref}
                
    #'14.didExpShr':self.expshr ,'15.didExpRef': self.expref ,'16.didShrRef': self.shrref ,'17.didExpShrRef': self.expshrref}
    #TODO: should I consider different kinds of abbreviations?
    #TODO: take a look at the mesh and decide if it is possible to separete levels or groups from their data (same for UMLS)

'''
    Boolean feature.
'''
def calculateNLPerUser(data):
    tempMapUserNL = dict()
    mapUserNL = dict()
    
    #Not using datetime, but it is important to keep the order of queries issued by the user
    userIds = sorted( (member.userId, member.datetime, member.keywords) for member in data )
    
    for (userId, _, keywords) in userIds:
        if userId not in tempMapUserNL:
            queryCounter = 1
            tempMapUserNL[userId] = False
        else:
            queryCounter += 1
        
        mapIndex = userId + "_" + str(queryCounter)
        mapUserNL[mapIndex] = ( tempMapUserNL[userId] or hasNLword(keywords) )
        tempMapUserNL[userId] = mapUserNL[mapIndex]

    #    print "User now = ", userId, " counter ---> ", queryCounter, " map ----> ",  mapUserNL[userId + "_" + str(queryCounter) ]

    #print "mapUserNL ---> ", mapUserNL
    return mapUserNL

def hasNLword(words):
    #print ( [ w for w in words if w.lower() in NLWords ] )
    return any( [ w for w in words if w.lower() in NLWords ] )
    
def calculateMeanMeshDepthPerUser(data):
    mapUserMeanMeshDepth = dict()
    processedUser = set()
    tempMap = defaultdict(list)

    #Not using datetime, but it is important to keep the order of queries issued by the user
    userIds = sorted( (member.userId, member.datetime, member.mesh) for member in data )
    
    for (userId, _, mesh) in userIds:
        
        if userId not in processedUser:
            processedUser.add(userId)
            queryCounter = 1
            previousIndex = -1
        else:
            queryCounter += 1
            previousIndex = userId + "_" + str(queryCounter-1)
            
        userIndex = userId + "_" + str(queryCounter)

        if mesh is None and previousIndex == -1: #first query and without mesh
            mapUserMeanMeshDepth[userIndex] = 0
        
        else:
            meanMesh =  sum(len(m.split(".")) for m in mesh)/len(mesh) if mesh is not None else 0

            if previousIndex == -1: #first query
                mapUserMeanMeshDepth[userIndex] = meanMesh
            else:
                #calculate new mean based on previous number
                mapUserMeanMeshDepth[userIndex] = ((mapUserMeanMeshDepth[previousIndex] * (queryCounter - 1) ) + meanMesh) / queryCounter
    
        #print "User id = ", userId, "counter =", queryCounter," mesh = ", mesh, " map => ", mapUserMeanMeshDepth[userIndex]
    return mapUserMeanMeshDepth

def calculateNumberOfQueriesPerUser(data):

    userIds = sorted( [member.userId, member.datetime] for member in data  ) 
    #usersNumberOfQueries = [ (k , len(list(g))) for k, g in groupby(userIds) ]
    processedUser = set()
    mapUserQueries = dict()
    
    for userId, _ in userIds:
        if userId not in processedUser:
            processedUser.add(userId)
            queryCounter = 1
        else:
            queryCounter += 1

        userIndex = userId + "_" + str(queryCounter)
        mapUserQueries[userIndex] = queryCounter

        #print "User id = ", userId, "counter =", queryCounter," map => ", mapUserQueries[userIndex]
    return mapUserQueries

def calculateMeanWordsPerQuery(data):
    mapUserMeanWords = dict()
    userWords = [ (member.userId, member.datetime, len(member.keywords)) for member in data ]
    processedUser = set()

    for (userId, _, nwords) in userWords:
        
        if userId not in processedUser:
            processedUser.add(userId)
            queryCounter = 1
            previousIndex = -1
        else:
            queryCounter += 1
            previousIndex = userId + "_" + str(queryCounter-1)
            
        userIndex = userId + "_" + str(queryCounter)

        if previousIndex == -1: #first query
            mapUserMeanWords[userIndex] = float(nwords)
        else:
            #calculate new mean based on previous number
            mapUserMeanWords[userIndex] = ((mapUserMeanWords[previousIndex] * (queryCounter - 1) ) + nwords) / queryCounter
        
        #print "User id = ", userId, "counter =", queryCounter," nwords = ", nwords, " map => ", mapUserMeanWords[userIndex]
    return mapUserMeanWords

def calculateNumberOfSessionsPerUser(data):
    userIds = sorted( [member.userId, member.datetime, member.previouskeywords is None] for member in data )
    mapUserSession = dict()
    userSessionCounter = dict()

    for userId, _, newSession in userIds:

        if userId not in userSessionCounter:
            userSessionCounter[userId] = 1
            queryCounter = 1
        else:
            queryCounter += 1
            if newSession:
                userSessionCounter[userId] += 1
        
        userIndex = userId + "_" + str(queryCounter)
        mapUserSession[userIndex] = userSessionCounter[userId]

        #print "User id = ", userId, "counter = ", queryCounter," newSession => ", newSession, " map => ", mapUserSession[userIndex]
    
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
    tempMapUserAbb = dict() 
    userIds = sorted( (member.userId, member.datetime, member.keywords) for member in data )
    
    for (userId, _, keywords) in userIds:
        if userId not in tempMapUserAbb:
            tempMapUserAbb[userId] = False
            queryCounter = 1
        else:
            queryCounter += 1

        userIndex = userId + "_" + str(queryCounter)

        mapUserAbb[userIndex] = ( tempMapUserAbb[userId] or hasAbbreviation(keywords) )
        tempMapUserAbb[userId] = mapUserAbb[userIndex]

        #cprint "user =", userId, " counter =", queryCounter, "mapUserAbb ---> ", mapUserAbb[userIndex]
    return mapUserAbb

def hasAbbreviation(words):
    return any( [ w for w in words if w.lower() in acronymsSet] )

def calculateMeanTimePerSession(data):
    
    mapUserMeanTimePerSession = dict()
    userDateBool = sorted( ( member.userId, member.datetime , member.previouskeywords is None) for member in data ) # (user, date, newSession? )
    processedUser = set()
    lastDate = 0

    for (userId, date, newSession) in userDateBool:
        
        if userId not in processedUser:
            processedUser.add(userId)
            queryCounter = 1
            numberOfSessions = 1
            totalSeconds = 0
            firstTimeInSession = date
            newSession = 0
            oldMeanTime, meanTimeSoFar = 0,0

        else:
            queryCounter += 1

        userIndex = userId + "_" + str(queryCounter)

        # new user session...
        if newSession:
            firstTimeInSession = date

            numberOfSessions += 1
            oldMeanTime = meanTimeSoFar
        
        sessionLength = (date - firstTimeInSession).total_seconds()
        meanTimeSoFar = (sessionLength + (numberOfSessions - 1) * oldMeanTime)/ numberOfSessions
        mapUserMeanTimePerSession[userIndex] = meanTimeSoFar

        #print "User id = ", userId, "counter = ", queryCounter," date =>", date, 
        #print "newSession => ", newSession, " sessions: ", numberOfSessions, "secs: ", sessionLength, " map => ", mapUserMeanTimePerSession[userIndex]
    return mapUserMeanTimePerSession

def calculateUserBehavior(data):
    mapUserBehavior = dict()
    sessions = createSessions(data)
    
    for user, session in sessions.iteritems():
        vOMS = [0]*8
        for subSession in session.values():

            modifiedSubSession = False
            previousQuery = subSession[0]
            subQueryE, subQueryS, subQueryRef, subQueryRep = 0, 0, 0, 0
            
            for query in subSession[1:]:
                e, s, ref, _ = compareSets( set(previousQuery[1]), set(query[1]) )
                subQueryE, subQueryS, subQueryRef, = subQueryE + e, subQueryS + s, subQueryRef + ref
                
                #print "Session === ", subSession, "\n"
                #print "Q1  = ", set(previousQuery[1]), " Q2 = ", set(query[1])
                #print " numberOfExpansions = ", numberOfExpansions, " numberOfShrinkage = ", numberOfShrinkage, " numberOfReformulations = ", numberOfReformulations, " numberOfRepetitions = ", numberOfRepetitions
                #print 

                # If a repetition occurs, we do not consider it as a modified session
                if e > 0 or s > 0 or ref > 0:
                    modifiedSubSession = True 
                previousQuery = query
                
            if modifiedSubSession:
                be, bs, bref, brep = 0 if subQueryE == 0 else 1, 0 if subQueryS == 0 else 1, 0 if subQueryRef == 0 else 1, 0 if subQueryRep == 0 else 1
                indexVal =  int( str(be) + str(bs) + str(bref), 2) 

                #print "INDEX = ", indexVal, " exp : ", be, " shr: ", bs, " ref:", bref
                vOMS[indexVal] += 1
            
        #print "indice 0 => ", vOMS[0]
        mapUserBehavior[user] = (vOMS[4] > 0, vOMS[2] > 0, vOMS[1] > 0, vOMS[6] > 0, vOMS[5] > 0, vOMS[3] > 0, vOMS[7]>0)
        
    return mapUserBehavior


def createDictOfUsers(data, label):
    userDict = dict()

    users = set( (member.userId for member in data) )
    countingNumberOfQueriesPerUser = calculateNumberOfQueriesPerUser(data)      # Transformed
    countingNumberOfSessionsPerUser = calculateNumberOfSessionsPerUser(data)    # Transformed
    countingMeanMeshDepthPerUser = calculateMeanMeshDepthPerUser(data)          # Transformed
    countingNLPerUser = calculateNLPerUser(data)                                # Transformed
    countingWordsPerQuery = calculateMeanWordsPerQuery(data)                    # Transformed 
    countingMeanTimePerSession = calculateMeanTimePerSession(data)              # Transformed
    countingUsingAbbreviation = calculateUsingAbbreviation(data)                # Transformed
    #countingUsingSymptons = calculateUsingSemantic(data, symptomTypes())        # TODO
    #countingUsingCause = calculateUsingSemantic(data, causeTypes())             # TODO
    #countingUsingRemedy = calculateUsingSemantic(data, remedyTypes())           # TODO
    #countingUsingNotMedical = calculateUsingSemantic(data, noMedicalTypes())    # TODO
    #countingUserBehavior = calculateUserBehavior(data)                          # TODO

    users = sorted( (member.userId, member.datetime) for member in data )
    previousUser = -1
    
    for u, _ in users:
        if u == previousUser:
            queryCounter += 1
        else:
            previousUser = u
            queryCounter = 1
        user = u + "_" + str(queryCounter)

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
        usy = 0 #countingUsingSymptons[user]
        usc = 0 #countingUsingCause[user]
        usrd = 0 #countingUsingRemedy[user]
        usnm = 0 #countingUsingNotMedical[user]
        expa, shri, refo, expshr, expref, shrref, expshrref = 0,0,0,0,0,0,0 #countingUserBehavior[user]


        userDict[user] = userClass(user, label, queryCounter, nq=nq, ns=ns, mmd=mmd, unl=unl, mwpq=mwpq, mtps=mtps, uab=uab, usy=usy, usc=usc, usrd=usrd, usnm=usnm,\
                                   expa=expa, shri=shri, refo=refo, expshr=expshr, expref=expref, shrref=shrref, expshrref=expshrref)

    return userDict

def createFV(filename, label):
    print "min = ", minimalNumberOfQueries, " max = ", maximalNumberOfQueries
    data = readMyFormat(filename) 
    data = preProcessData(data, removeStopWords)    # Sort the data by user and date
    data = keepUsersInsideLimiteOfQueires(data, minimalNumberOfQueries, maximalNumberOfQueries)
    
    userDict = createDictOfUsers(data, label)
    
    print len(userDict)
    
    return userDict

def keepUsersInsideLimiteOfQueires(data, Xmin, Xmax):
    userIds = sorted( [member.userId for member in data ] ) 
    usersToRemove = set()
    for k, g in groupby(userIds):
        x = len(list(g)) 
        if x > Xmax or x < Xmin:
            usersToRemove.add(k)
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
    
    honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.dataset.gz", 0)
    aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealthCompleteFixed.v4.dataset.gz", 0)
    goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.dataset.gz", 0)
    tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.dataset.gz", 0)

    notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial.v4.dataset.gz", 1)

    # 10% of the dataset only
    #honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.10.gz", 0)
    #aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth.v4.10.gz", 0)
    #goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.10.gz", 0)
    #tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.10.gz", 0)
    
    # 1% of the dataset only
    #notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial.v4.1.gz", 1)

    ### Merge Feature sets and transforme them into inputs
    healthUserFV = mergeFVs(honFV, aolHealthFV, goldMinerFV, tripFV)
    notHealthUserFV = notHealth
 
    healthUserOutputFile = "healthUser-%d.pk" % (minimalNumberOfQueries)
    notHealthUserOutputFile = "notHealthUser-%d.pk" % (minimalNumberOfQueries)
   
    ####### Save and Load the Features
    import pickle
    with open(healthUserOutputFile, 'wb') as output:
        pickle.dump(healthUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (healthUserOutputFile)
    
    with open(notHealthUserOutputFile, 'wb') as output:
        pickle.dump(notHealthUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (notHealthUserOutputFile)

def regularMedicalUsers():
    ####
    ### Load Datasets
    ##
    #
    
    honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.dataset.gz", 0)
    aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealthCompleteFixed.v4.dataset.gz", 0)
    goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.dataset.gz", 1)
    tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.dataset.gz", 1)
    
    # 10% of the dataset only
    #honFV = createFV("dataSetsOfficials/hon/honEnglish.v4.10.gz", 0)
    #aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth.v4.10.gz", 0)
    #goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner.v4.10.gz", 1)
    #tripFV = createFV("dataSetsOfficials/trip/trip_mod.v4.10.gz", 1)

    ####
    ### Merge Feature sets and transforme them into inputs
    ##
    # 
    regularUserFV = mergeFVs(honFV, aolHealthFV)
    medicalUserFV = mergeFVs(tripFV, goldMinerFV)

    regularUserOutputFile = "regularUser-%d.pk" % (minimalNumberOfQueries)
    medicalUserOutputFile = "medicalUser-%d.pk" % (minimalNumberOfQueries)

    ####### Save and Load the Features
    import pickle
    with open(regularUserOutputFile, 'wb') as output:
        pickle.dump(regularUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (regularUserOutputFile)
    
    with open(medicalUserOutputFile, 'wb') as output:
        pickle.dump(medicalUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (medicalUserOutputFile)
    
if __name__ == "__main__":

    minimalNumberOfQueries = int(sys.argv[1])
    regularMedicalUsers()
    #healthNotHealthUsers()
