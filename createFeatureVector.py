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
formatVersion = "v5"
simpleTest = True

### HOW TO USE:
#   python createFeatureVector.py minimalNumberOfQueries 

class userClass:
    def __init__(self, id, label, nq, ns, mmd, unl, mwpq, mtps, uab, usy, usc, usrd, usnm, expa, shri, refo, expshr, expref, shrref, expshrref,\
                chvf=0.0, chv=0.0, umls=0.0, chvm=0.0, combo=0.0):
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

        self.expansion = expa
        self.shrinkage = shri
        self.reformulation = refo
        self.expshr = expshr
        self.expref = expref
        self.shrref = shrref
        self.expshrref = expshrref
        
        self.chvf = chvf
        self.chv = chv
        self.umls = umls
        self.chvm = chvm
        self.comboScore = combo

    def toDict(self):
        return {'00.numberOfQueries':self.numberOfQueries, '01.numberOfSessions':self.numberOfSessions, '02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical, '11.didExpansion': self.expansion ,'12.didShrinkage': self.shrinkage ,'13.didReformulation': self.reformulation , '14.didExpShrRef':self.expshrref, '15.CHVFound': self.chvf, '16.CHV':self.chv, '17.UMLS':self.umls, '18.CHVMisspelled':self.chvm, '19.ComboScore':self.comboScore}
        #return {'00.numberOfQueries':self.numberOfQueries, '01.numberOfSessions':self.numberOfSessions, '02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical}
                
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
        #print "User = ", user, " MeanTime =", mapUserMeanTimePerSession[user]
    
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

def calculateCHV(data):

    tempMap = defaultdict(list)
    mapUserCHVFound, mapUserCHV, mapUserUMLS, mapUserMisspelled, mapComboScore = {}, {}, {}, {}, {}

    for item in [( member.userId, member.CHVFound, \
                  1 if member.hasCHV == True else 0, 
                  1 if member.hasUMLS == True else 0,\
                  1 if member.hasCHVMisspelled == True else 0,\
                  float(member.comboScore)
                 ) for member in data]:

        tempMap[item[0]].append([item[1], item[2], item[3], item[4], item[5]])
    
    for user, values in tempMap.iteritems():
        #print user, values
        size = len(values)
        mapUserCHVFound[user]   = sum([v[0] for v in values])/size
        mapUserCHV[user]        = sum([v[1] for v in values])/size
        mapUserUMLS[user]       = sum([v[2] for v in values])/size
        mapUserMisspelled[user] = sum([v[3] for v in values])/size
        mapComboScore[user]     = sum([v[4] for v in values])/size

    return mapUserCHVFound, mapUserCHV, mapUserUMLS, mapUserMisspelled    
    
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
    countingUserBehavior = calculateUserBehavior(data)

    if formatVersion == "v5":
        countingUserCHVFound, countingUserCHV, countingUserUMLS, countingUserMisspelled = calculateCHV(data)

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
        expa, shri, refo, expshr, expref, shrref, expshrref = countingUserBehavior[user]
        
        if formatVersion == "v5":
            CHVFound, CHV    = countingUserCHVFound[user], countingUserCHV[user]
            UMLS, CHVMisspelled = countingUserUMLS[user], countingUserMisspelled[user]
            userDict[user] = userClass(user, label, nq=nq, ns=ns, mmd=mmd, unl=unl, mwpq=mwpq, mtps=mtps, uab=uab, usy=usy, usc=usc, usrd=usrd, usnm=usnm,\
                                   expa=expa, shri=shri, refo=refo, expshr=expshr, expref=expref, shrref=shrref, expshrref=expshrref,\
                                      chvf=CHVFound, chv=CHV, umls=UMLS, chvm=CHVMisspelled)
        else:
            userDict[user] = userClass(user, label, nq=nq, ns=ns, mmd=mmd, unl=unl, mwpq=mwpq, mtps=mtps, uab=uab, usy=usy, usc=usc, usrd=usrd, usnm=usnm,\
                                   expa=expa, shri=shri, refo=refo, expshr=expshr, expref=expref, shrref=shrref, expshrref=expshrref)

    return userDict

def createFV(filename, label):
    print "min = ", minimalNumberOfQueries, " max = ", maximalNumberOfQueries
    data = readMyFormat(filename, formatVersion) 
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
    
    if not simpleTest:
        honFV = createFV("dataSetsOfficials/hon/honEnglish." + formatVersion + ".dataset.gz", 0)
        aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealthCompleteFixed." + formatVersion + ".dataset.gz", 0)
        goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner." + formatVersion + ".dataset.gz", 0)
        tripFV = createFV("dataSetsOfficials/trip/trip_mod." + formatVersion + ".dataset.gz", 0)
        notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial." + formatVersion + ".dataset.gz", 1)

    if simpleTest:
        # 10% of the dataset only
        honFV = createFV("dataSetsOfficials/hon/honEnglish." + formatVersion + ".10.dataset..gz", 0)
        aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealth." + formatVersion + ".10.dataset.gz", 0)
        goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner." + formatVersion + ".10.dataset.gz", 0)
        tripFV = createFV("dataSetsOfficials/trip/trip_mod." + formatVersion + ".10.dataset.gz", 0)
    
        # 1% of the dataset only
        notHealth = createFV("dataSetsOfficials/aolNotHealth/aolNotHealthPartial."+ formatVersion + ".1.gz", 1)

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
    
    if not simpleTest:
        honFV = createFV("dataSetsOfficials/hon/honEnglish." + formatVersion + ".dataset.gz", 0)
        aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealthCompleteFixed4." + formatVersion + ".dataset.gz", 0)
        goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner." + formatVersion + ".dataset.gz", 1)
        tripFV = createFV("dataSetsOfficials/trip/trip_mod." + formatVersion + ".dataset.gz", 1)
    
    if simpleTest:
        # 1 or 10% of the dataset only
        honFV = createFV("dataSetsOfficials/hon/honEnglish."+ formatVersion + ".1.dataset.gz", 0)
        aolHealthFV = createFV("dataSetsOfficials/aolHealth/aolHealthCompleteFixed4." + formatVersion + ".1.dataset.gz", 0)
        goldMinerFV = createFV("dataSetsOfficials/goldminer/goldMiner." + formatVersion + ".1.dataset.gz", 1)
        tripFV = createFV("dataSetsOfficials/trip/trip_mod." + formatVersion + ".1.dataset.gz", 1)

    ####
    ### Merge Feature sets and transforme them into inputs
    ##
    # 
    #regularUserFV = mergeFVs(honFV, aolHealthFV)
    #medicalUserFV = mergeFVs(tripFV, goldMinerFV)
    regularUserFV = honFV
    medicalUserFV = goldMinerFV

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
