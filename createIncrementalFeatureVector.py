from __future__ import division
from itertools import groupby
from collections import Counter, defaultdict 
from optparse import OptionParser
import sys, pickle

#My classes
from readCSV import readMyFormat
from auxiliarFunctions import NLWords, preProcessData, createAcronymSet, symptomTypes, causeTypes, remedyTypes, whereTypes, noMedicalTypes, compareSets
from statistics import createSessions

removeStopWords=False
formatVersion = "v6" #"v5" #"v4"
simpleTest = True
pathToData = "../logAnalysisDataSets/"
usingAdam=True

acronymsSet = createAcronymSet(usingAdam)

### HOW TO USE:
#   python createFeatureVector.py minimalNumberOfQueries 

def testing(minNumberOfQueries, maxNumberOfQueries, explanation):
    testA, testB = {},{}
    for i in range(0,1):
        testA_ = createFV("v62", 0, minNumberOfQueries, maxNumberOfQueries)
        testB_ = createFV("v63", 1, minNumberOfQueries, maxNumberOfQueries)
        testA = mergeFVs(testA, testA_)
        testB = mergeFVs(testB, testB_)

    regularUserOutputFile = "regularUser-%d-%s.pk" % (minNumberOfQueries, explanation)
    medicalUserOutputFile = "medicalUser-%d-%s.pk" % (minNumberOfQueries, explanation)
    with open(regularUserOutputFile, 'wb') as output:
        pickle.dump(testA, output, pickle.HIGHEST_PROTOCOL)
    
    with open(medicalUserOutputFile, 'wb') as output:
        pickle.dump(testB, output, pickle.HIGHEST_PROTOCOL)
    print "Created Feature Vectors from test files"

class userClass:
    def __init__(self, id, label, nc, nq, wpu, unl, uab): #mmd, unl, mwpq, mtps, uab, usy, usc, usrd, usnm, expa, shri, refo, expshr, expref, shrref, expshrref,\
                #chvf=0.0, chv=0.0, umls=0.0, chvm=0.0, combo=0.0):
        #General
        self.id = id
        self.label = label
        # Group 1
        self.numberOfChars = nc
        self.numberOfQueries = nq
        self.numberOfWords = wpu
        self.useOfNL = unl
        self.useOfMedAbb = uab

        #self.numberOfQueries = nq
        #self.numberOfSessions = ns
        #self.usingNL = unl
        
        #self.meanWordsPerQuery = mwpq
        #self.meanTimePerSession = mtps
        #self.usingAbbreviation = uab
        #self.usingSymptons = usy
        #self.usingCause = usc
        #self.usingRemedy = usrd
        #self.usingNotMedical = usnm
        
        #self.meanMeshDepth = mmd
        #self.expansion = expa
        #self.shrinkage = shri
        #self.reformulation = refo
        #self.expshr = expshr
        #self.expref = expref
        #self.shrref = shrref
        #self.expshrref = expshrref
        
        #self.chvf = chvf
        #self.chv = chv
        #self.umls = umls
        #self.chvm = chvm
        #self.comboScore = combo

    def toDict(self, idxq, groups):
        featuresToUse = {}
        counter = 0

        if "g1" in groups:
            featuresToUse["%02d.AvgCharsPerQuery" % (counter) ] = sum(self.numberOfChars[0:idxq]) / idxq
            counter+=1
            print idxq, sum(self.numberOfChars[0:idxq]), sum(self.numberOfChars[0:idxq]) / idxq
            #featuresToUse["%02d.AvgWordsPerQuery" % (counter) ] = self.numberOfWords / self.numberOfQueries
            #counter+=1
            #featuresToUse["%02d.AvgUseOfNL" % (counter) ] = sum(self.useOfNL) / self.numberOfQueries
            #counter+=1
            #featuresToUse["%02d.AnyPastUseOfNL" % (counter) ] = any(self.useOfNL)
            #counter+=1
            #featuresToUse["%02d.AvgUseOfMedAbb" % (counter) ] = sum(self.useOfMedAbb) / self.numberOfQueries
            #counter+=1
            #featuresToUse["%02d.AnyPastUseOfMedAbb" % (counter) ] = any(self.useOfMedAbb)
            #counter+=1
            #Features related to the last query:
            #featuresToUse["%02d.CharsInLastQuery" % (counter) ] = self.charsInLastQuery
            #counter+=1
            #featuresToUse["%02d.WordsInLastQuery" % (counter) ] = self.wordsInLastQuery
            #counter+=1
            #featuresToUse["%02d.UsedNLLastQuery" % (counter) ] = (self.useOfNL[-1] == 1)
            #counter+=1
            #featuresToUse["%02d.UsedMedAbbLastQuery" % (counter) ] = (self.useOfMedAbb[-1] == 1)
            #counter+=1
        
        return featuresToUse
        #return {'00.numberOfQueries':self.numberOfQueries, '01.numberOfSessions':self.numberOfSessions,'02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical, '11.didExpansion': self.expansion ,'12.didShrinkage': self.shrinkage ,'13.didReformulation': self.reformulation , '14.didExpShrRef':self.expshrref, '15.CHVFound': self.chvf, '16.CHV':self.chv, '17.UMLS':self.umls, '18.CHVMisspelled':self.chvm, '19.ComboScore':self.comboScore}
                
def createDictOfUsers(data, label):
    userDict = defaultdict(list)

    users = set( (member.userId for member in data) )
    
    #Group 1
    countingNumberOfCharsPerUser = calculateNumberOfCharsPerUser(data)
    countingNumberOfQueriesPerUser = calculateNumberOfQueriesPerUser(data)      
    countingWordsPerUser = calculateWordsPerUser(data)
    countingNLPerUser = calculateNLPerUser(data)
    countingMedicalAbbreviations = calculateMedicalAbbreviations(data)
    
    #countingNumberOfSessionsPerUser = calculateNumberOfSessionsPerUser(data)    
    #countingMeanMeshDepthPerUser = calculateMeanMeshDepthPerUser(data)          
    #countingNLPerUser = calculateNLPerUser(data)                                
    #countingWordsPerQuery = calculateMeanWordsPerQuery(data)                    
    #countingMeanTimePerSession = calculateMeanTimePerSession(data)              
    #countingUsingAbbreviation = calculateUsingAbbreviation(data)                
    #countingUsingSymptons = calculateUsingSemantic(data, symptomTypes())        
    #countingUsingCause = calculateUsingSemantic(data, causeTypes())             
    #countingUsingRemedy = calculateUsingSemantic(data, remedyTypes())           
    #countingUsingNotMedical = calculateUsingSemantic(data, noMedicalTypes())    
    #countingUserBehavior = calculateUserBehavior(data)                          
    #countingUserCHVFound, countingUserCHV, countingUserUMLS, countingUserMisspelled, countingUserComboScore = calculateCHV(data) # TODO

    users = sorted( (member.userId, member.datetime) for member in data )
    previousUser = -1
    
    for u, _ in users:
        #if u == previousUser:
        #    queryCounter += 1
        #else:
        #    previousUser = u
        #    queryCounter = 1

        #user = u + "_" + str(queryCounter).zfill(2)

        nc = countingNumberOfCharsPerUser[u]
        nq = countingNumberOfCharsPerUser[u] #countingNumberOfQueriesPerUser[user]
        wpu = 0 #countingWordsPerUser[user]
        unl = {} #countingNLPerUser[user]
        uab = {} #countingMedicalAbbreviations[user]

        #nq = countingNumberOfQueriesPerUser[user]
        #ns = countingNumberOfSessionsPerUser[user]
        #mmd = 0.0 if user not in countingMeanMeshDepthPerUser else countingMeanMeshDepthPerUser[user]
        #unl = countingNLPerUser[user]
        #mwpq = countingWordsPerQuery[user]
        #mtps = countingMeanTimePerSession[user]
        #uab = countingUsingAbbreviation[user]
        #usy = countingUsingSymptons[user]
        #usc = countingUsingCause[user]
        #usrd = countingUsingRemedy[user]
        #usnm = countingUsingNotMedical[user]
        #expa, shri, refo, expshr, expref, shrref, expshrref = countingUserBehavior[user]

        #CHVFound, CHV    = countingUserCHVFound[user], countingUserCHV[user]
        #UMLS, CHVMisspelled = countingUserUMLS[user], countingUserMisspelled[user]
        #comboScore = countingUserComboScore[user]

        #userDict[u].append(userClass(user, label, nq=nq, ns=ns, mmd=mmd, unl=unl, mwpq=mwpq, mtps=mtps, uab=uab, usy=usy, usc=usc, usrd=usrd, usnm=usnm,\
        #                       expa=expa, shri=shri, refo=refo, expshr=expshr, expref=expref, shrref=shrref, expshrref=expshrref,\
        #                          chvf=CHVFound, chv=CHV, umls=UMLS, chvm=CHVMisspelled, combo=comboScore) )
        #userDict[u].append(userClass(user, label, nc=nc, nq=nq, wpu=wpu, unl=unl, uab=uab))
        userDict[u] = userClass(u, label, nc=nc, nq=nq, wpu=wpu, unl=unl, uab=uab)

    return userDict


#### ------------------------------FEATURES----------------------------------#####

def calculateNumberOfCharsPerUser(data):
    mapUserChars = defaultdict(list)
    
    userWords = [ (member.userId, member.keywords) for member in data ]
    queryInChars = [(userId, sum(len(q) for q in query)) for (userId, query) in userWords]
    
    for (userId, lenght) in queryInChars:
        mapUserChars[userId].extend([lenght])


    for k,v in mapUserChars.items():
        print k, v
    

    return mapUserChars


def calculateNumberOfCharsPerUser2(data):
    mapUserChars = dict()
    processed = set()
    
    userWords = [ (member.userId, member.keywords) for member in data ]
    queryInChars = [(userId, sum(len(q) for q in query)) for (userId, query) in userWords]
    
    for (userId, lenght) in queryInChars:
        if userId not in processed:
            queryCounter = 1
            processed.add(userId)
        else:
            queryCounter += 1
        
        print "row --- ", userId, lenght
        mapIndex = userId + "_" + str(queryCounter).zfill(2)
        mapUserChars[mapIndex] = lenght
    return mapUserChars

def calculateWordsPerUser(data):
    return {}

def calculateMedicalAbbreviations(data):
    return {}

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
        
        mapIndex = userId + "_" + str(queryCounter).zfill(2)
        mapUserNL[mapIndex] = ( tempMapUserNL[userId] or hasNLword(keywords) )
        tempMapUserNL[userId] = mapUserNL[mapIndex]

    #    print "User now = ", userId, " counter ---> ", queryCounter, " map ----> ",  mapUserNL[userId + "_" + str(queryCounter).zfill(2) ]

    #print "mapUserNL ---> ", mapUserNL
    return mapUserNL

def hasNLword(words):
    #print ( [ w for w in words if w.lower() in NLWords ] )
    return any( [ w for w in words if w.lower() in NLWords ] )
   

def calculateCHV(data):

    tempMap = defaultdict(list)
    mapUserCHVFound, mapUserCHV, mapUserUMLS, mapUserMisspelled, mapComboScore = {}, {}, {}, {}, {}

    userIds = sorted( (member.userId, member.datetime, member.CHVFound, member.hasCHV, member.hasUMLS, member.hasCHVMisspelled, member.comboScore) for member in data )
    for (userId, _, CHVFound, hasCHV, UMLS, CHVMisspelled, comboScore) in userIds:
        tempMap[userId].append([CHVFound,1 if hasCHV else 0, 1 if UMLS else 0, 1 if CHVMisspelled else 0, float(comboScore)])

    for userId, queries in tempMap.items():
        queryCounter = 0 
        values = []
        for query in queries:
            queryCounter += 1
            userIndex = userId + "_" + str(queryCounter).zfill(2)
            
            values.append(query)
            size = len(values)
            mapUserCHVFound[userIndex]   = sum([v[0] for v in values])/size
            mapUserCHV[userIndex]        = sum([v[1] for v in values])/size
            mapUserUMLS[userIndex]       = sum([v[2] for v in values])/size
            mapUserMisspelled[userIndex] = sum([v[3] for v in values])/size
            mapComboScore[userIndex]     = sum([v[4] for v in values])/size

    return mapUserCHVFound, mapUserCHV, mapUserUMLS, mapUserMisspelled, mapComboScore
 

def calculateMeanMeshDepthPerUser(data):
    mapUserMeanMeshDepth = dict()
    previousUser = str(-1)
    tempMap = defaultdict(list)

    #Not using datetime, but it is important to keep the order of queries issued by the user
    userIds = sorted( (member.userId, member.datetime, member.mesh) for member in data )
    
    for (userId, _, mesh) in userIds:
        
        if userId != previousUser:
            previousUser = userId
            queryCounter = 1
            previousIndex = -1
        else:
            queryCounter += 1
            previousIndex = userId + "_" + str(queryCounter-1).zfill(2)
            
        userIndex = userId + "_" + str(queryCounter).zfill(2)

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
    previousUser = str("invalid user")
    mapUserQueries = dict()
    
    for userId, _ in userIds:
        if userId != previousUser:
            previousUser = userId
            queryCounter = 1
        else:
            queryCounter += 1

        userIndex = userId + "_" + str(queryCounter).zfill(2)
        mapUserQueries[userIndex] = queryCounter

        #print "User id = ", userId, "counter =", queryCounter," map => ", mapUserQueries[userIndex]
    return mapUserQueries

def calculateMeanWordsPerQuery(data):
    mapUserMeanWords = dict()
    userWords = [ (member.userId, member.datetime, len(member.keywords)) for member in data ]
    previousUser = str("invalid user")

    for (userId, _, nwords) in userWords:
        
        if userId != previousUser:
            previousUser = userId
            queryCounter = 1
            previousIndex = -1
        else:
            queryCounter += 1
            previousIndex = userId + "_" + str(queryCounter-1).zfill(2)
            
        userIndex = userId + "_" + str(queryCounter).zfill(2)

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
        
        userIndex = userId + "_" + str(queryCounter).zfill(2)
        mapUserSession[userIndex] = userSessionCounter[userId]

        #print "User id = ", userId, "counter = ", queryCounter," newSession => ", newSession, " map => ", mapUserSession[userIndex]
    
    return mapUserSession

def hasSemanticType(words, semanticSet):
    if words is None:
        return False
    return any( [ w for w in words if w.lower() in semanticSet] )

def calculateUsingSemantic(data, semanticType):
    mapUserSemantic = dict()
    tempMapUserSemantic = dict() 
    userIds = sorted( (member.userId, member.datetime, member.semanticTypes) for member in data )
    
    for (userId, _, st) in userIds: 
        if userId not in tempMapUserSemantic:
            tempMapUserSemantic[userId] = False
            queryCounter = 1
        else:
            queryCounter += 1
        
        userIndex = userId + "_" + str(queryCounter).zfill(2)

        mapUserSemantic[userIndex] = ( tempMapUserSemantic[userId] or hasSemanticType(st, semanticType) )
        tempMapUserSemantic[userId] = mapUserSemantic[userIndex]
    
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

        userIndex = userId + "_" + str(queryCounter).zfill(2)

        mapUserAbb[userIndex] = ( tempMapUserAbb[userId] or hasAbbreviation(keywords) )
        tempMapUserAbb[userId] = mapUserAbb[userIndex]

        #print "user =", userId, " counter =", queryCounter, "mapUserAbb ---> ", mapUserAbb[userIndex]
    return mapUserAbb

def hasAbbreviation(words):
    return any( [ w for w in words if w.lower() in acronymsSet] )

def calculateMeanTimePerSession(data):
    
    mapUserMeanTimePerSession = dict()
    userDateBool = sorted( ( member.userId, member.datetime , member.previouskeywords is None) for member in data ) # (user, date, newSession? )
    previousUser = str("invalid user")
    lastDate = 0

    for (userId, date, newSession) in userDateBool:
        
        if userId != previousUser:
            previousUser = userId
            queryCounter = 1
            numberOfSessions = 1
            totalSeconds = 0
            firstTimeInSession = date
            newSession = 0
            oldMeanTime, meanTimeSoFar = 0,0

        else:
            queryCounter += 1

        userIndex = userId + "_" + str(queryCounter).zfill(2)

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

def getBehavior(vOMS, subQueryE, subQueryS, subQueryRef, subQueryRep):
    be, bs, bref, brep = 0 if subQueryE == 0 else 1, 0 if subQueryS == 0 else 1, 0 if subQueryRef == 0 else 1, 0 if subQueryRep == 0 else 1
    indexVal =  int( str(be) + str(bs) + str(bref), 2) 
    vOMS[indexVal] += 1
    return (vOMS[4] > 0, vOMS[2] > 0, vOMS[1] > 0, vOMS[6] > 0, vOMS[5] > 0, vOMS[3] > 0, vOMS[7]>0)
            
def calculateUserBehavior(data):
    
    mapUserBehavior = dict()
    tempMapUserBehavior = dict()

    sessions = createSessions(data)
    for user, session in sessions.iteritems():
        vOMS = [0]*8
        queryCounter = 0
        subQueryE, subQueryS, subQueryRef, subQueryRep = 0, 0, 0, 0

        for subSession in session.values():
            
            previousQuery = subSession[0]
            queryCounter += 1
            userIndex = user + "_" + str(queryCounter).zfill(2)
            mapUserBehavior[userIndex] = getBehavior(vOMS, subQueryE, subQueryS, subQueryRef, subQueryRep)  
            
            for query in subSession[1:]:
                queryCounter += 1
                userIndex = user + "_" + str(queryCounter).zfill(2)

                e, s, ref, _ = compareSets( set(previousQuery[1]), set(query[1]) )
                subQueryE, subQueryS, subQueryRef, = subQueryE + e, subQueryS + s, subQueryRef + ref
                mapUserBehavior[userIndex] = getBehavior(vOMS, subQueryE, subQueryS, subQueryRef, subQueryRep)  
                previousQuery = query

    return mapUserBehavior

def createFV(filename, label, minNumberOfQueries, maxNumberOfQueries):
    print "min = ", minNumberOfQueries, " max = ", maxNumberOfQueries
    data = readMyFormat(filename, formatVersion) 
    data = preProcessData(data, removeStopWords)    # Sort the data by user and date
    data = keepUsersInsideLimiteOfQueires(data, minNumberOfQueries, maxNumberOfQueries)
    
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
     
    if not simpleTest:
        honFV = createFV("dataSetsOfficials/hon/honEnglish." + formatVersion + ".dataset.gz", 0)
        aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealthCompleteFixed4." + formatVersion + ".dataset.gz", 0)
        goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner." + formatVersion + ".dataset.gz", 0)
        tripFV = createFV("dataSetsOfficials/trip/trip_mod." + formatVersion + ".dataset.gz", 0)
        notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial." + formatVersion + ".dataset.gz", 1)

    if simpleTest:
        # 1% of the dataset only
        honFV = createFV("dataSetsOfficials/hon/honEnglish." + formatVersion + ".1.dataset..gz", 0)
        aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth." + formatVersion + ".1.dataset.gz", 0)
        goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner." + formatVersion + ".1.dataset.gz", 0)
        tripFV = createFV("dataSetsOfficials/trip/trip_mod." + formatVersion + ".1.dataset.gz", 0)
    
        notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial."+ formatVersion + ".1.gz", 1)

    ### Merge Feature sets and transforme them into inputs
    healthUserFV = mergeFVs(honFV, aolHealthFV, goldMinerFV, tripFV)
    notHealthUserFV = notHealth
 
    healthUserOutputFile = "healthUser-%d.pk" % (minimalNumberOfQueries)
    notHealthUserOutputFile = "notHealthUser-%d.pk" % (minimalNumberOfQueries)
   
    ####### Save and Load the Features
    with open(healthUserOutputFile, 'wb') as output:
        pickle.dump(healthUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (healthUserOutputFile)
    
    with open(notHealthUserOutputFile, 'wb') as output:
        pickle.dump(notHealthUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (notHealthUserOutputFile)

def regularMedicalUsers(minimalNumberOfQueries, maxNumberOfQueries, explanation):
    ####
    ### Load Datasets
    ##
    #
    if simpleTest:
        honFV = createFV(pathToData + "/hon/honAugEnglish."+ formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthClean." + formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        goldMinerFV = createFV(pathToData + "/goldminer/goldMiner." + formatVersion + ".1.dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
        tripFV = createFV(pathToData + "/trip/trip." + formatVersion + ".1.dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
   
    else:
        honFV = createFV(pathToData + "/hon/honAugEnglish." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthClean." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        goldMinerFV = createFV(pathToData + "/goldminer/goldMiner." + formatVersion + ".dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
        tripFV = createFV(pathToData + "/trip/trip." + formatVersion + ".dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
    
    ####
    ### Merge Feature sets and transforme them into inputs
    ##
    # 
    regularUserFV = mergeFVs(honFV, aolHealthFV)
    medicalUserFV = mergeFVs(tripFV, goldMinerFV)

    regularUserOutputFile = "regularUser-%d-%s.pk" % (minimalNumberOfQueries, explanation)
    medicalUserOutputFile = "medicalUser-%d-%s.pk" % (minimalNumberOfQueries, explanation)

    ####### Save and Load the Features
    with open(regularUserOutputFile, 'wb') as output:
        pickle.dump(regularUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (regularUserOutputFile)
    
    with open(medicalUserOutputFile, 'wb') as output:
        pickle.dump(medicalUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (medicalUserOutputFile)
    
if __name__ == "__main__":

    op = OptionParser(version="%prog 1")
    
    op.add_option("--minNumberOfQueries", "-m", action="store", type="int", dest="minNumberOfQueries", help="Define the min. number of queries (X) necessary to use a user for classification.  [default: %default]", metavar="X", default=5)
    op.add_option("--maxNumberOfQueries", "-M", action="store", type="int", dest="maxNumberOfQueries", help="Define the max. number of queries (X) necessary to use\
                  a user for classification.  [default: %default]", metavar="X", default=100)
    op.add_option("--explanation", "-e", action="store", type="string", dest="explanation", help="Prefix to include in the created files", metavar="N", default="")
    op.add_option("--healthUsers", "-u", action="store_true", dest="healthUsers", help="Use if you want to create a health/not health user feature file", default=False)
    op.add_option("--testingOnly", "-t", action="store_true", dest="testingOnly", help="Just to test some new feature", default=False)

    (opts, args) = op.parse_args()
    if len(args) > 0:
        print "This program does not receive parameters this way: use -h to see the options."
    
    if opts.testingOnly:
        testing(opts.minNumberOfQueries, opts.maxNumberOfQueries, opts.explanation)
        sys.exit(0)
    
    if opts.healthUsers:
        healthNotHealthUsers(opts.minNumberOfQueries, opts.maxNumberOfQueries, opts.explanation)
    else:
        regularMedicalUsers(opts.minNumberOfQueries, opts.maxNumberOfQueries, opts.explanation)

