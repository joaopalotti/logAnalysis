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
formatVersion = "v6"
simpleTest = True
pathToData = "../logAnalysisDataSets/"
honAug = True
aolClean = True
usingAdam = True
toyExample = False

acronymsSet = createAcronymSet(usingAdam)
### HOW TO USE:
#   python createFeatureVector.py minimalNumberOfQueries 

class userClass:
    def __init__(self, id, label, nc, nq, ns, mmd, unl, mwpq, ttps, uab, usy, usc, usrd, usnm, expa, shri, refo, expshr, expref, shrref, expshrref,\
                chv=[], wpu=0, cslq=0, wslq=0, tls=0, nqls=0, modi=0, usem=0, lofs=[], soas=set(),\
                lofc=[], soac=set(), tags=[]):
        self.id = id
        self.label = label
        self.numberOfChars = nc
        self.numberOfQueries = nq
        self.numberOfSessions = ns
        self.meanWordsPerQuery = mwpq
        self.totalTimePerSession = ttps

        self.symptoms = usy
        self.causes = usc
        self.remedies = usrd
        self.notMedical = usnm

        self.expansions = expa
        self.shrinkages = shri
        self.reformulations = refo
        self.expshr = expshr
        self.expref = expref
        self.shrref = shrref
        self.expshrref = expshrref
        self.modifications = modi
        
        self.numberOfWords = wpu
        self.useOfNL = unl
        self.useOfMedAbb = uab
        
        self.charsInLastQuery = cslq
        self.wordsInLastQuery = wslq
        self.timeInLastSession = tls
        self.numberOfQueriesInLastSession = nqls

        self.listMeshDepth = mmd
        self.listNumberOfMeshConcepts = usem

        self.listOfSources = lofs
        self.setOfAllSources = soas
        
        self.listOfConcepts = lofc
        self.setOfAllConcepts = soac
        
        allTags = []
        for tag in tags:
            allTags.extend(tag)
        
        self.countTags = Counter(allTags)

        self.chv = chv
        lenchv = len(self.chv)
        self.chvdata, self.chvf, self.umls, self.chvMisspelled, self.comboScore = 0,0,0,0,0
        for row in self.chv:
            self.chvdata += row[0] 
            self.chvf += row[0] 
            self.umls += row[1]
            self.chvMisspelled += row[2]
            self.comboScore += row[3]
        self.chvdata = self.chvdata / lenchv
        self.chvf = self.chvf / lenchv
        self.umls = self.umls / lenchv
        self.chvMisspelled = self.chvMisspelled / lenchv
        self.comboScore = self.comboScore / lenchv
    
    def toDict(self, groups):
        featuresToUse = {}
        counter = 0

        if "g1" in groups:
            featuresToUse["%02d.AvgCharsPerQuery" % (counter) ] = self.numberOfChars /  self.numberOfQueries
            counter+=1
            featuresToUse["%02d.CharsInLastQuery" % (counter) ] = self.charsInLastQuery
            counter+=1
            featuresToUse["%02d.AvgWordsPerQuery" % (counter) ] = self.numberOfWords / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.WordsInLastQuery" % (counter) ] = self.wordsInLastQuery
            counter+=1
            featuresToUse["%02d.AvgUseOfNL" % (counter) ] = sum(self.useOfNL) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.AnyPastUseOfNL" % (counter) ] = any(self.useOfNL)
            counter+=1
            featuresToUse["%02d.UsedNLLastQuery" % (counter) ] = (self.useOfNL[-1] == 1)
            counter+=1
            featuresToUse["%02d.AvgUseOfMedAbb" % (counter) ] = sum(self.useOfMedAbb) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.AnyPastUseOfMedAbb" % (counter) ] = any(self.useOfMedAbb)
            counter+=1
            featuresToUse["%02d.UsedMedAbbLastQuery" % (counter) ] = (self.useOfMedAbb[-1] == 1)
            counter+=1

        if "g2" in groups:
            featuresToUse["%02d.AvgQueriesPerSession" % (counter) ] =  self.numberOfQueries / self.numberOfSessions
            counter+=1
            featuresToUse["%02d.NumberOfQueriesInLastSession" % (counter) ] = self.numberOfQueriesInLastSession
            counter+=1
            featuresToUse["%02d.AvgTimePerSession" % (counter) ] = self.totalTimePerSession / self.numberOfSessions
            counter+=1
            featuresToUse["%02d.TimeInLastSession" % (counter) ] = self.timeInLastSession
            counter+=1
        
        if "g3" in groups:
            featuresToUse["%02d.AvgNumberOfExpansions" % (counter) ] = self.expansions / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastExpansion" % (counter) ] = (self.expansions > 0)
            counter+=1
            #TODO:
            #featuresToUse["%02d.ExpandedLastQuery" % (counter) ] = 
            #counter+=1
            featuresToUse["%02d.AvgNumberOfReduction" % (counter) ] = self.shrinkages / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastReduction" % (counter) ] = (self.shrinkages > 0)
            counter+=1
            featuresToUse["%02d.AvgNumberOfReformulation" % (counter) ] = self.reformulations / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastRefomulation" % (counter) ] = (self.reformulations > 0)
            counter+=1
            featuresToUse["%02d.AvgNumberOfExpRed" % (counter) ] = self.expshr / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastExpRed" % (counter) ] = (self.expshr > 0)
            counter+=1
            featuresToUse["%02d.AvgNumberOfExpRef" % (counter) ] = self.expref / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastExpRef" % (counter) ] = (self.expref > 0)
            counter+=1
            featuresToUse["%02d.AvgNumberOfRedRef" % (counter) ] = self.shrref / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastRedRef" % (counter) ] = (self.shrref > 0)
            counter+=1
            featuresToUse["%02d.AvgNumberOfExpRedRef" % (counter) ] = self.expshrref / self.modifications 
            counter+=1
            featuresToUse["%02d.AnyPastExpRedRef" % (counter) ] = (self.expshrref > 0)
            counter+=1
        
        if "g4" in groups:
            featuresToUse["%02d.AvgSymptomsPerQuery" % (counter) ] = sum(self.symptoms) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.AnyPastSearchForSymptoms" % (counter) ] = any(self.symptoms) 
            counter+=1
            featuresToUse["%02d.SearchSymptomPreviousQuery" % (counter) ] = (self.symptoms[-1] == 1)
            counter+=1
            featuresToUse["%02d.AvgCausesPerQuery" % (counter) ] = sum(self.causes) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.AnyPastSearchForCauses" % (counter) ] = any(self.causes)
            counter+=1
            featuresToUse["%02d.SearchCausePreviousQuery" % (counter) ] = (self.causes[-1] == 1)
            counter+=1
            featuresToUse["%02d.AvgRemediesPerQuery" % (counter) ] = sum(self.remedies) / self.numberOfQueries 
            counter+=1
            featuresToUse["%02d.AnyPastSearchForRemedies" % (counter) ] = any(self.remedies)
            counter+=1
            featuresToUse["%02d.SearchRemedyPreviousQuery" % (counter) ] = (self.remedies[-1] == 1)
            counter+=1
            featuresToUse["%02d.AvgNonSymCauseRemedyTypesPerQuery" % (counter) ] = sum(self.notMedical) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.AvgTop5NonMedicalSemanticTypesPerQuery" % (counter) ] = any(self.notMedical)
            counter+=1
            featuresToUse["%02d.AvgTop5NonMedicalSemanticTypesPerQuery" % (counter) ] = (self.notMedical[-1] == 1)
            counter+=1
 
        if "g5" in groups:
            ###------------------------- Mesh features --------------------------###
            featuresToUse["%02d.AvgQueriesUsingMeSH" % (counter) ] = len(self.listNumberOfMeshConcepts) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.AvgNumberOfMeSHPerQuery" % (counter) ] = sum(self.listNumberOfMeshConcepts) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.NumberOfMeshInLastQuery" % (counter) ] = 0 if len(self.listNumberOfMeshConcepts) == 0 else self.listNumberOfMeshConcepts[-1]
            counter+=1
            featuresToUse["%02d.AvgMeSHDepth" % (counter) ] =  sum(self.listMeshDepth) / self.numberOfQueries
            counter+=1
            featuresToUse["%02d.MeSHDepthInLastQuery" % (counter) ] = 0 if len(self.listMeshDepth) == 0 else self.listMeshDepth[-1]
            counter+=1
            featuresToUse["%02d.HasUsedMeSHBefore" % (counter) ] = False if len(self.listMeshDepth) == 0 else True   
            counter+=1
            ###------------------------- Souce features --------------------------###
            #Number of different sources in metamap: 169  (http://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html)
            featuresToUse["%02d.AvgQueriesUsingSources" % (counter) ] = len(self.listOfSources) / self.numberOfQueries 
            counter+=1
            featuresToUse["%02d.AvgNumberOfSourcesPerQuery" % (counter) ] = sum(self.listOfSources) / self.numberOfQueries 
            counter+=1
            featuresToUse["%02d.TotalNumberOfDifferentSourcesUsed" % (counter) ] = len(self.setOfAllSources) / 169.0
            counter+=1
            featuresToUse["%02d.NumberOfSourcesInLastQuery" % (counter) ] = 0 if len(self.listOfSources) == 0 else self.listOfSources[-1]
            counter+=1
            ###------------------------- Concepts --------------------------###
            featuresToUse["%02d.AvgQueriesUsingConcepts" % (counter) ] = len(self.listOfConcepts) / self.numberOfQueries 
            counter+=1
            featuresToUse["%02d.AvgNumberOfConceptsPerQuery" % (counter) ] = sum(self.listOfConcepts) / self.numberOfQueries 
            counter+=1
            featuresToUse["%02d.TotalNumberOfDifferentConceptsUsed" % (counter) ] = len(self.setOfAllConcepts) 
            counter+=1
            featuresToUse["%02d.NumberOfConceptsInLastQuery" % (counter) ] = 0 if len(self.listOfConcepts) == 0 else self.listOfConcepts[-1]
            counter+=1

        if "g6" in groups:
            featuresToUse["%02d.AvgNumberOfCHVDataFound" % (counter) ] =  self.chvdata
            counter+=1
            featuresToUse["%02d.NumberOfCHVDataLastQuery" % (counter) ] = self.chv[-1][0] 
            counter+=1
            featuresToUse["%02d.AnyCHVDataInPast" % (counter) ] = (self.chvdata > 0.0) 
            counter+=1
            featuresToUse["%02d.AvgNumberOfCHVFound" % (counter) ] =  self.chvf
            counter+=1
            featuresToUse["%02d.NumberOfCHVLastQuery" % (counter) ] = self.chv[-1][1] 
            counter+=1
            featuresToUse["%02d.AnyCHVInPast" % (counter) ] = self.chvf > 0.0 
            counter+=1
            featuresToUse["%02d.AvgNumberOfUMLSFound" % (counter) ] =  self.umls
            counter+=1
            featuresToUse["%02d.NumberOfUMLSLastQuery" % (counter) ] = self.chv[-1][2] 
            counter+=1
            featuresToUse["%02d.AnyUMLSInPast" % (counter) ] = self.umls > 0.0 
            counter+=1
            featuresToUse["%02d.AvgNumberOfCHVMisspelledFound" % (counter) ] =  self.chvMisspelled
            counter+=1
            featuresToUse["%02d.NumberOfCHVMisspelledLastQuery" % (counter) ] = self.chv[-1][3] 
            counter+=1
            featuresToUse["%02d.AnyCHVMisspelledInPast" % (counter) ] = self.chvMisspelled > 0.0 
            counter+=1
            featuresToUse["%02d.AvgNumberOfComboScoreFound" % (counter) ] =  self.comboScore
            counter+=1
            featuresToUse["%02d.NumberOfComboScoreLastQuery" % (counter) ] = self.chv[-1][4] 
            counter+=1
           
        if "g7" in groups:
            ###------------------------- TAGS --------------------------###
            numberOfTags = sum(self.countTags.values())
            numberOfTags = 1.0 if numberOfTags == 0 else numberOfTags

            featuresToUse["%02d.PercentageOfNouns" % (counter) ] = 0.0 if 'noun' not in self.countTags.keys() else self.countTags['noun'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfAdjectives" % (counter) ] = 0.0 if 'adj' not in self.countTags.keys() else self.countTags['adj'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfConjuctions" % (counter) ] = 0.0 if 'conj' not in self.countTags.keys() else self.countTags['conj'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfVerbs" % (counter) ] = 0.0 if 'verb' not in self.countTags.keys() else self.countTags['verb'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfShapes" % (counter) ] = 0.0 if 'shape' not in self.countTags.keys() else self.countTags['shape'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfPunctuations" % (counter) ] = 0.0 if 'punc' not in self.countTags.keys() else self.countTags['punc'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfAdverbs" % (counter) ] = 0.0 if 'adv' not in self.countTags.keys() else self.countTags['adv'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfDeterminers" % (counter) ] = 0.0 if 'det' not in self.countTags.keys() else self.countTags['det'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfAuxiliars" % (counter) ] = 0.0 if 'aux' not in self.countTags.keys() else self.countTags['aux'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfPrepositions" % (counter) ] = 0.0 if 'prep' not in self.countTags.keys() else self.countTags['prep'] / numberOfTags 
            counter+=1
            featuresToUse["%02d.PercentageOfPronotuns" % (counter) ] = 0.0 if 'pron' not in self.countTags.keys() else self.countTags['pron'] / numberOfTags 
            counter+=1
            ### TODO: more tags and last query tags

        print featuresToUse

        return featuresToUse

        #TODO: remove this after wsdm result is issued
        #if version == "wsdm":
        #    return {'00.queriesPerSession':self.numberOfQueries/self.numberOfSessions, '01.charsPerQueries':self.numberOfChars/self.numberOfQueries,'02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical, '11.didExpansion': self.expansion ,'12.didShrinkage': self.shrinkage ,'13.didReformulation': self.reformulation , '14.didExpShrRef':self.expshrref}

def createDictOfUsers(data, label):
    userDict = dict()

    users = set( (member.userId for member in data) )
    countingNumberOfQueriesPerUser = calculateNumberOfQueriesPerUser(data)
    countingNumberOfCharsPerUser, countingLastCharsPerUser = calculateNumberOfCharsPerUser(data)
    countingMeshDepthPerUser, countingUseMeshPerUser = calculateMeshDepthPerUser(data)
    countingNLPerUser = calculateNLPerUser(data)
    countingWordsPerQuery = calculateMeanWordsPerQuery(data)
    countingTotalTimePerSession, countingNumberOfSessionsPerUser, countingTimeLastSession, countingNumberOfQueriesLastSession = calculateTimePerSession(data)
    countingMedicalAbbreviations = calculateMedicalAbbreviations(data)
    countingSymptoms = calculateUsingSemantic(data, symptomTypes())
    countingCause = calculateUsingSemantic(data, causeTypes())
    countingRemedy = calculateUsingSemantic(data, remedyTypes())
    countingNotMedical = calculateUsingSemantic(data, noMedicalTypes())
    countingUserBehavior, numberOfModifications = calculateUserBehavior(data)
    countingWordsPerUser, countingLastWordsPerUser = calculateWordsPerUser(data)
    countingSources, setOfAllSources = calculateSources(data)
    countingConcetps, setOfAllConcepts = calculateConcepts(data)
    countingTags = calculateTags(data)
    countingCHV = calculateCHV(data)

    for user in users:
        if user not in countingNumberOfQueriesPerUser or \
           user not in countingNumberOfSessionsPerUser or \
           user not in countingNLPerUser or\
           user not in countingWordsPerQuery:
            
            print "User is not present. It should be...User ID = ", user
            print "Number of queries -> ", user in countingNumberOfQueriesPerUser
            print "Number of sessions -> ", user in countingNumberOfSessionsPerUser
            print "NL -> ", user in countingNLPerUser
            print "WordsPerQuery-> ", user in countingWordsPerQuery

            sys.exit(0)
            continue

        nc = countingNumberOfCharsPerUser[user]
        nq = countingNumberOfQueriesPerUser[user]
        ns = countingNumberOfSessionsPerUser[user]
        mwpq = countingWordsPerQuery[user]
        ttps = countingTotalTimePerSession[user]
        uab = countingMedicalAbbreviations[user]
        unl = countingNLPerUser[user]

        usy = countingSymptoms[user]
        usc = countingCause[user]
        usrd = countingRemedy[user]
        usnm = countingNotMedical[user]
        
        expa, shri, refo, expshr, expref, shrref, expshrref = countingUserBehavior[user]
        modi = numberOfModifications
        wpu = countingWordsPerUser[user]
        wslq = countingLastWordsPerUser[user]
        cslq = countingLastCharsPerUser[user]
        tls = countingTimeLastSession[user]
        nqls = countingNumberOfQueriesLastSession[user]

        mmd = [] if user not in countingMeshDepthPerUser else countingMeshDepthPerUser[user]
        usem = countingUseMeshPerUser[user]

        lofs = countingSources[user]
        soas = setOfAllSources[user]
    
        lofc = countingConcetps[user]
        soac = setOfAllConcepts[user]

        tags = countingTags[user]
        
        chv = countingCHV[user]
        
        userDict[user] = userClass(user, label, nc=nc, nq=nq, ns=ns, mmd=mmd, unl=unl, mwpq=mwpq, ttps=ttps, uab=uab, usy=usy, usc=usc, usrd=usrd, usnm=usnm,\
                                   expa=expa, shri=shri, refo=refo, expshr=expshr, expref=expref, shrref=shrref, expshrref=expshrref, chv=chv,\
                                   wpu=wpu, wslq=wslq, tls=tls, nqls=nqls,\
                                  modi=modi, usem=usem, lofs=lofs, soas=soas, lofc=lofc, soac=soac, tags=tags)

    return userDict

#### ========================= METRICS ============================ #####
def calculateTags(data):
    mapUserListOfTags = defaultdict(list)
    
    userIds = sorted( (member.userId, member.postags) for member in data)
    for (userId, tags) in userIds:
        if tags:
            mapUserListOfTags[userId].append( [t for t in tags] )
    
    return mapUserListOfTags
    

def calculateConcepts(data):
    mapUserConcepts = defaultdict(list)
    setOfConcepts = defaultdict(set)
    
    userIds = sorted( (member.userId, member.concepts) for member in data)
    for (userId, concepts) in userIds:
        if concepts:
            mapUserConcepts[userId].append( len(concepts) )
            setOfConcepts[userId].update( {s for s in concepts } )
        
        #print userId, concept
    return mapUserConcepts, setOfConcepts

def calculateSources(data):
    mapUserSource = defaultdict(list)
    setOfSources = defaultdict(set)
    
    userIds = sorted( (member.userId, member.sourceList) for member in data)

    for (userId, sourceList) in userIds:
        if sourceList is not None:
            mapUserSource[userId].append( len(sourceList) )
            setOfSources[userId].update( {s for s in sourceList } )

        #print "ROW --- ", userId, sourceList
        #print "MAP --", mapUserSource 
        #print "SET --", setOfSources
    return mapUserSource, setOfSources

def calculateNLPerUser(data):
    mapUserNL = defaultdict(list)
    
    userIds = sorted( (member.userId, member.keywords) for member in data )
    
    for (userId, keywords) in userIds:
        mapUserNL[userId].append( 1 if hasNLword(keywords) else 0 )

    #print "mapUserNL ---> ", mapUserNL
    return mapUserNL

def hasNLword(words):
    #print ( [ w for w in words if w.lower() in NLWords ] )
    return any( [ w for w in words if w.lower() in NLWords ] )

def calculateMedicalAbbreviations(data):
    mapUserAbb = defaultdict(list)
    
    userIds = sorted( (member.userId, member.keywords) for member in data )
    
    for (userId, keywords) in userIds:
        mapUserAbb[userId].append(1 if hasAbbreviation(keywords) else 0)

    #print "mapUserAbb ---> ", mapUserAbb
    return mapUserAbb

def hasAbbreviation(words):
    return any( [ w for w in words if w.lower() in acronymsSet] )

def calculateMeshDepthPerUser(data):

    mapUserNumberOfMeshConcepts = defaultdict(list)
    mapUserDepthOfMesh = defaultdict(list)

    userIds = sorted( (member.userId, member.mesh) for member in data )
    
    for (userId, mesh) in userIds:
        if mesh is not None:
            mapUserNumberOfMeshConcepts[userId].append(len(mesh))
            mapUserDepthOfMesh[userId].append( sum( [ len(m.split(".")) for m in mesh ] ) / len(mesh) )

            #print mesh, len(mesh),  sum( [ len(m.split(".")) for m in mesh ] ) / len(mesh)
    
    return mapUserNumberOfMeshConcepts, mapUserDepthOfMesh
    #return mapUserTotalMeshDepth, mapUserTimesUsingMesh, mapUserMeshIds, mapUserNumberOfMeshLastQuery, mapUserDepthLastQuery

def calculateNumberOfCharsPerUser(data):
    mapUserChars = defaultdict(int)
    mapUserLastChar = defaultdict(int)

    userWords = [ (member.userId, member.keywords) for member in data ]
    queryInChars = [(userId, sum(len(q) for q in query)) for (userId, query) in userWords]

    for (userId, lenght) in queryInChars:
        mapUserChars[userId] += lenght
        mapUserLastChar[userId] = lenght

    return mapUserChars, mapUserLastChar

def calculateNumberOfQueriesPerUser(data):
    userIds = sorted( [member.userId for member in data ] ) 
    usersNumberOfQueries = [ (k , len(list(g))) for k, g in groupby(userIds) ]
    mapUserQueries = dict()
    for u, nq in usersNumberOfQueries:
        mapUserQueries[u] = nq
    
    return mapUserQueries

def calculateWordsPerUser(data):
    mapUserWords = dict()
    mapUserLastWords = dict()
    userWords = [ (member.userId, len(member.keywords)) for member in data ]
    
    tempMap = defaultdict(list)
    for (userId, lenght) in userWords:
        tempMap[userId].append(lenght)

    for (userId, listOfLenghts) in tempMap.iteritems():
        mapUserWords[userId] = sum(listOfLenghts)
        mapUserLastWords[userId] = listOfLenghts[-1]
    
    return mapUserWords, mapUserLastWords

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

def hasSemanticType(words, semanticSet):
    if words is None:
        return False
    return any( [ w for w in words if w.lower() in semanticSet] )

def calculateUsingSemantic(data, semanticType):
    mapUserSemantic = defaultdict(list)

    userIds = sorted( (member.userId, member.semanticTypes) for member in data )
    for (userId, st) in userIds:
        mapUserSemantic[userId].append(1 if hasSemanticType(st, semanticType) else 0)
    return mapUserSemantic


def calculateTimePerSession(data):
    mapUserTotalTimePerSession = dict()
    mapUserNumberOfSessions = dict()
    mapUserTimeLastSession = dict()
    mapUserQueriesLastSession = dict()

    userDateBool = [ ( member.userId, member.datetime , member.previouskeywords is None, member.keywords) for member in data ] # (user, date, newSession?, keywords)

    tempMap = defaultdict(list)

    for (user, date, newSession, keywords) in userDateBool:
        tempMap[user].append( (date, newSession, keywords) )
        #print user, date, newSession

    for (user, dateNewSession) in tempMap.iteritems():
        
        totalSeconds = 0
        numberOfSessions = 0

        startDate = dateNewSession[0][0]
        endDate = startDate
        #print "User ---> ", user, " Start --> ", startDate
        
        for date, newSession, _ in dateNewSession[1:]:
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
        keywords = dateNewSession[-1][-1]

        mapUserTimeLastSession[user] = seconds
        mapUserTotalTimePerSession[user] = totalSeconds
        mapUserNumberOfSessions[user] = numberOfSessions
        mapUserQueriesLastSession[user] = len(keywords)
        #print "User = ", user, " MeanTime =", mapUserMeanTimePerSession[user]
    
    return mapUserTotalTimePerSession, mapUserNumberOfSessions, mapUserTimeLastSession, mapUserQueriesLastSession

def calculateUserBehavior(data):
    mapUserBehavior = dict()
    sessions = createSessions(data)
    numberOfModifications = 0
    
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
                numberOfModifications += 1
                be, bs, bref, brep = 0 if subQueryE == 0 else 1, 0 if subQueryS == 0 else 1, 0 if subQueryRef == 0 else 1, 0 if subQueryRep == 0 else 1
                indexVal =  int( str(be) + str(bs) + str(bref), 2) 

                #print "INDEX = ", indexVal, " exp : ", be, " shr: ", bs, " ref:", bref
                vOMS[indexVal] += 1
            
        #print "indice 0 => ", vOMS[0]
        mapUserBehavior[user] = (vOMS[4], vOMS[2], vOMS[1], vOMS[6], vOMS[5], vOMS[3], vOMS[7])
        
    return mapUserBehavior, numberOfModifications

def calculateCHV(data):

    mapCHV = defaultdict(list)

    for item in [( member.userId, member.CHVFound, \
                  1 if member.hasCHV == True else 0, 
                  1 if member.hasUMLS == True else 0,\
                  1 if member.hasCHVMisspelled == True else 0,\
                  float(member.comboScore)
                 ) for member in data]:

        mapCHV[item[0]].append([item[1], item[2], item[3], item[4], item[5]])
    
    return mapCHV

##### ========================================================================================== #####

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

def healthNotHealthUsers(minimalNumberOfQueries, maxNumberOfQueries):
    if simpleTest:
        # 1% of the dataset only
        honFV = createFV(pathToData + "/hon/honEnglish." + formatVersion + ".1.dataset..gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        aolHealthFV = createFV(pathToData + "/aolHealth/aolHealth." + formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        goldMinerFV = createFV(pathToData + "/goldminer/goldMiner." + formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        tripFV = createFV(pathToData + "/trip/trip." + formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        notHealth = createFV(pathToData + "/aolNotHealth/aolNotHealthFinal-noDash.v5."+ formatVersion + ".1.dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
   
    else:
        if honAug:
            honFV = createFV(pathToData + "/hon/honAugEnglish." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        else:
            honFV = createFV(pathToData + "/hon/honEnglish." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)

        if aolClean:
            aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthClean." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
            notHealth = createFV(pathToData + "/aolNotHealth/aolNotHealthNoAnimal-noDash." + formatVersion + ".dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
        else:
            aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthCompleteFixed5." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
            notHealth = createFV(pathToData + "/aolNotHealth/aolNotHealthFinal-noDash." + formatVersion + ".dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
        
        goldMinerFV = createFV(pathToData + "/goldminer/goldMiner." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        tripFV = createFV(pathToData + "/trip/trip." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)


    ### Merge Feature sets and transforme them into inputs
    healthUserFV = mergeFVs(honFV, aolHealthFV, goldMinerFV, tripFV)
    notHealthUserFV = notHealth
 
    healthUserOutputFile = "healthUser-%d-%s.pk" % (minimalNumberOfQueries, explanation)
    notHealthUserOutputFile = "notHealthUser-%d-%s.pk" % (minimalNumberOfQueries, explanation)
   
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
    if toyExample:
        honFV, goldMinerFV = {}, {}
        aolHealthFV = createFV("v6", 0, 0, 100)
        tripFV = createFV("v6", 1, 0, 100)
                               
    elif simpleTest:
        # 1 or 10% of the dataset only
        honFV = createFV(pathToData + "/hon/honAugEnglish."+ formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthClean." + formatVersion + ".1.dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        goldMinerFV = createFV(pathToData + "/goldminer/goldMiner." + formatVersion + ".1.dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
        tripFV = createFV(pathToData + "/trip/trip." + formatVersion + ".1.dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
   
    else:
        if honAug:
            honFV = createFV(pathToData + "/hon/honAugEnglish." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        else:
            honFV = createFV(pathToData + "/hon/honEnglish." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)

        if aolClean:
            aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthClean." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        else:
            aolHealthFV = createFV(pathToData + "/aolHealth/aolHealthCompleteFixed5." + formatVersion + ".dataset.gz", 0, minimalNumberOfQueries, maxNumberOfQueries)
        goldMinerFV = createFV(pathToData + "/goldminer/goldMiner." + formatVersion + ".dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
        tripFV = createFV(pathToData + "/trip/trip." + formatVersion + ".dataset.gz", 1, minimalNumberOfQueries, maxNumberOfQueries)
    

    ####
    ### Merge Feature sets and transforme them into inputs
    ##
    # 
    regularUserFV = mergeFVs(honFV, aolHealthFV)
    medicalUserFV = mergeFVs(tripFV, goldMinerFV)
    #regularUserFV = honFV
    #medicalUserFV = goldMinerFV

    regularUserOutputFile = "regularUser-%d-%s.pk" % (minimalNumberOfQueries, explanation)
    medicalUserOutputFile = "medicalUser-%d-%s.pk" % (minimalNumberOfQueries, explanation)

    ####### Save and Load the Features
    import pickle
    with open(regularUserOutputFile, 'wb') as output:
        pickle.dump(regularUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (regularUserOutputFile)
    
    with open(medicalUserOutputFile, 'wb') as output:
        pickle.dump(medicalUserFV, output, pickle.HIGHEST_PROTOCOL)
        print "CREATED FILE: %s" % (medicalUserOutputFile)
    
def testing(minNumberOfQueries, maxNumberOfQueries, explanation):
    testA, testB = {},{}
    for i in range(0,10):
        testA_ = createFV( "in50", 0, minNumberOfQueries, maxNumberOfQueries)
        testB_ = createFV( "in50", 1, minNumberOfQueries, maxNumberOfQueries)
        testA = mergeFVs(testA, testA_)
        testB = mergeFVs(testB, testB_)
    
    with open("regularUser-5-test.pk", 'wb') as output:
        pickle.dump(testA, output, pickle.HIGHEST_PROTOCOL)
    
    with open("medicalUser-5-test.pk", 'wb') as output:
        pickle.dump(testB, output, pickle.HIGHEST_PROTOCOL)


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

