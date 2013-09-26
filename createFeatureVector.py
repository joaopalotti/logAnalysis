from __future__ import division
from itertools import groupby
from collections import Counter, defaultdict 
from optparse import OptionParser
import sys, pickle

#My classes
from readCSV import readMyFormat
from auxiliarFunctions import NLWords, preProcessData, createAcronymSet, symptomTypes, causeTypes, remedyTypes, noMedicalTypes, compareSets

removeStopWords=False
formatVersion = "v6"
pathToData = "../logAnalysisDataSets/"
honAug = True
aolClean = True
usingAdam = True

acronymsSet = createAcronymSet(usingAdam)
### HOW TO USE:
#   python createFeatureVector.py minimalNumberOfQueries 

class userClass:
    def __init__(self, id, label, nq, nc, wpu, unl, uab, ns, ttps, expa, shri, modi, keeps, usy, usc, usrd, usnm, lum, mmd, lofs, soas, lofc, soac,\
                chvd, chvf, umls, chvm, chvs, tags):
        #General 
        self.id = id
        self.label = label
        self.numberOfQueries = nq
        
        #Group 1
        self.numberOfChars = nc
        self.numberOfWords = wpu
        self.useOfNL = unl
        self.useOfMedAbb = uab

        #Group 2
        self.startedSessions = ns
        self.timePerSession = ttps

        #Group 3
        self.expansions = expa
        self.reductions = shri
        self.modifications = modi
        self.keeps = keeps
        
        #Group 4
        self.symptoms = usy
        self.causes = usc
        self.remedies = usrd
        self.notMedical = usnm

        #Group 5
        self.listNumberOfMeshConcepts = lum
        self.listMeshDepth = mmd
        self.listOfSources = lofs
        self.accSetOfSources = soas
        self.listOfConcepts = lofc
        self.accSetOfConcepts = soac
        
        #Group 6
        self.chvdata = chvd
        self.chvf = chvf
        self.umls = umls
        self.chvMisspelled = chvm
        self.comboScore = chvs

        #Group 7
        self.accTags = tags

    def toDict(self, idxq, groups):
        # Idxq varies from 0 to (numberOfQueries - 1)

        featuresToUse = {}
        counter = 0
        if idxq >= self.numberOfQueries:
            print "ERROR ---- idxq > numberOfQueries. idxq = %d, numberOfQueries = %d" % (idxq, self.numberOfQueries)
            exit(0)

        if "g1" in groups:
            featuresToUse["%02d.AvgCharsPerQuery" % (counter) ] = sum(self.numberOfChars[0:(idxq+1)])/(idxq+1)
            counter+=1
            featuresToUse["%02d.AvgWordsPerQuery" % (counter) ] = sum(self.numberOfWords[0:(idxq+1)])/(idxq+1)
            counter+=1
            featuresToUse["%02d.AvgUseOfNL" % (counter) ] = sum(self.useOfNL[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastUseOfNL" % (counter) ] = any(self.useOfNL[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.AvgUseOfMedAbb" % (counter) ] = sum(self.useOfMedAbb[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastUseOfMedAbb" % (counter) ] = any(self.useOfMedAbb[0:(idxq+1)])
            counter+=1
            #Features related to the actual query:
            featuresToUse["%02d.CharsInQuery" % (counter) ] = self.numberOfChars[idxq]
            counter+=1
            featuresToUse["%02d.WordsInQuery" % (counter) ] = self.numberOfWords[idxq]
            counter+=1
            featuresToUse["%02d.UsedNLQuery" % (counter) ] = self.useOfNL[idxq] == 1
            counter+=1
            featuresToUse["%02d.UsedMedAbbQuery" % (counter) ] = self.useOfMedAbb[idxq] == 1
            counter+=1

        if "g2" in groups:
            sessionsSoFar = sum(self.startedSessions[0:(idxq+1)])
            featuresToUse["%02d.AvgQueriesPerSession" % (counter) ] = 0 if sessionsSoFar == 0 else (idxq+1) / sessionsSoFar
            counter+=1
            featuresToUse["%02d.AvgTimePerSession" % (counter) ] = 0 if sessionsSoFar == 0 else sum(self.timePerSession[0:(idxq+1)]) / sessionsSoFar
            counter+=1
        
        if "g3" in groups:
            featuresToUse["%02d.AvgNumberOfExpansions" % (counter) ] = sum(self.expansions[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastExpansion" % (counter) ] = any(self.expansions[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.ExpandedQuery" % (counter) ] = self.expansions[idxq]
            counter+=1
            featuresToUse["%02d.AvgNumberOfReductions" % (counter) ] = sum(self.reductions[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastReductions" % (counter) ] = any(self.reductions[0:(idxq)])
            counter+=1
            featuresToUse["%02d.ReductedQuery" % (counter) ] = self.reductions[idxq]
            counter+=1
            featuresToUse["%02d.AvgNumberOfModifications" % (counter) ] = sum(self.modifications[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastModification" % (counter) ] = any(self.modifications[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.ModifiedQuery" % (counter) ] = self.modifications[idxq]
            counter+=1
            featuresToUse["%02d.AvgNumberOfKeeps" % (counter) ] = sum(self.keeps[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastKeep" % (counter) ] = any(self.keeps[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.KeptQuery" % (counter) ] = self.keeps[idxq]
            counter+=1
        
        if "g4" in groups:
            featuresToUse["%02d.AvgSymptomsPerQuery" % (counter) ] = sum(self.symptoms[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastSearchForSymptoms" % (counter) ] = any(self.symptoms[0:(idxq+1)]) 
            counter+=1
            featuresToUse["%02d.AvgCausesPerQuery" % (counter) ] = sum(self.causes[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastSearchForCauses" % (counter) ] = any(self.causes[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.AvgRemediesPerQuery" % (counter) ] = sum(self.remedies[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastSearchForRemedies" % (counter) ] = any(self.remedies[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.AvgNonSymCauseRemedyTypesPerQuery" % (counter) ] = sum(self.notMedical[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyPastSearchForNonSymCauseRemedyTypes" % (counter) ] = any(self.notMedical[0:(idxq+1)])
            counter+=1
            #Features related to the actual query:
            featuresToUse["%02d.SearchedSymptomQuery" % (counter) ] = (self.symptoms[idxq] == 1)
            counter+=1
            featuresToUse["%02d.SearchedCauseQuery" % (counter) ] =   (self.causes[idxq] == 1)
            counter+=1
            featuresToUse["%02d.SearchedRemedyQuery" % (counter) ] =   (self.remedies[idxq] == 1)
            counter+=1
            featuresToUse["%02d.SearchedForNonSymCauseRemedyQuery" % (counter) ] = (self.notMedical[idxq] == 1)
            counter+=1
 
        if "g5" in groups:
            ###------------------------- Mesh features --------------------------###
            featuresToUse["%02d.AvgQueriesUsingMeSH" % (counter) ] = sum([1 for m in self.listNumberOfMeshConcepts[0:(idxq+1)] if m > 0]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AvgNumberOfMeSHPerQuery" % (counter) ] = sum(self.listNumberOfMeshConcepts[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AvgMeSHDepth" % (counter) ] = sum(self.listMeshDepth[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.HasUsedMeSHBefore" % (counter) ] = False if sum(self.listMeshDepth[0:(idxq+1)]) == 0 else True   
            counter+=1
            #Features related to the actual query:
            featuresToUse["%02d.NumberOfMeshInQuery" % (counter) ] = self.listNumberOfMeshConcepts[idxq]
            counter+=1
            featuresToUse["%02d.MeSHDepthInQuery" % (counter) ] = self.listMeshDepth[idxq]
            counter+=1
            ###------------------------- Souce features --------------------------###
            #Number of different sources in metamap: 169  (http://www.nlm.nih.gov/research/umls/sourcereleasedocs/index.html)
            featuresToUse["%02d.AvgQueriesUsingSources" % (counter) ] = sum([1 for s in self.listOfSources[0:(idxq+1)] if s > 0]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AvgNumberOfSourcesPerQuery" % (counter) ] = sum(self.listOfSources[0:(idxq+1)]) / (idxq+1) 
            counter+=1
            featuresToUse["%02d.TotalNumberOfDifferentSourcesUsed" % (counter) ] = len(self.accSetOfSources[idxq]) / 169.0
            counter+=1
            #Features related to the actual query:
            featuresToUse["%02d.NumberOfSourcesInQuery" % (counter) ] = self.listOfSources[idxq]
            counter+=1
            ###------------------------- Concepts --------------------------###
            featuresToUse["%02d.AvgQueriesUsingConcepts" % (counter) ] = sum([1 for c in self.listOfConcepts[0:(idxq+1)] if c > 0]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AvgNumberOfConceptsPerQuery" % (counter) ] = sum(self.listOfConcepts[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.TotalNumberOfDifferentConceptsUsed" % (counter) ] = len(self.accSetOfConcepts[idxq])
            counter+=1
            #Features related to the query:
            featuresToUse["%02d.NumberOfConceptsInQuery" % (counter) ] = self.listOfConcepts[idxq]
            counter+=1

        if "g6" in groups:
            featuresToUse["%02d.AvgNumberOfCHVDataFound" % (counter) ] =  sum(self.chvdata[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyCHVDataInPast" % (counter) ] = any(self.chvdata[0:(idxq+1)]) 
            counter+=1
            featuresToUse["%02d.AvgNumberOfCHVFound" % (counter) ] = sum(self.chvf[0:(idxq+1)]) / (idxq+1)
            counter+=1
            featuresToUse["%02d.AnyCHVInPast" % (counter) ] = any(self.chvf[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.AvgNumberOfUMLSFound" % (counter) ] = sum(self.umls[0:(idxq+1)])/(idxq+1)
            counter+=1
            featuresToUse["%02d.AnyUMLSInPast" % (counter) ] = any(self.umls[0:(idxq+1)])
            counter+=1
            featuresToUse["%02d.AvgNumberOfCHVMisspelledFound" % (counter) ] = sum(self.chvMisspelled[0:(idxq+1)])/(idxq+1)
            counter+=1
            featuresToUse["%02d.AnyCHVMisspelledInPast" % (counter) ] = any(self.chvMisspelled[0:(idxq+1)]) 
            counter+=1
            featuresToUse["%02d.AvgNumberOfComboScoreFound" % (counter) ] =  sum(self.comboScore[0:(idxq+1)]) / (idxq+1)
            counter+=1
            #Features related to the actual query:
            featuresToUse["%02d.NumberOfCHVDataQuery" % (counter) ] = self.chvdata[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfCHVQuery" % (counter) ] = self.chvf[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfUMLSQuery" % (counter) ] = self.umls[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfCHVMisspelledQuery" % (counter) ] = self.chvMisspelled[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfComboScoreQuery" % (counter) ] = self.comboScore[idxq]
            counter+=1

        if "g7" in groups:
            ###------------------------- TAGS --------------------------###
            nTags = sum(self.accTags[idxq].values())
            nTags = 1.0 if nTags == 0 else nTags
            keys = self.accTags[idxq].keys()

            featuresToUse["%02d.PercentageOfNouns" % (counter) ] = 0.0 if 'noun' not in keys else self.accTags[idxq]['noun'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfAdjectives" % (counter) ] = 0.0 if 'adj' not in keys else self.accTags[idxq]['adj'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfConjuctions" % (counter) ] = 0.0 if 'conj' not in keys else self.accTags[idxq]['conj'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfVerbs" % (counter) ] = 0.0 if 'verb' not in keys else self.accTags[idxq]['verb'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfShapes" % (counter) ] = 0.0 if 'shape' not in keys else self.accTags[idxq]['shape'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfPunctuations" % (counter) ] = 0.0 if 'punc' not in keys else self.accTags[idxq]['punc'] / nTags
            counter+=1
            featuresToUse["%02d.PercentageOfAdverbs" % (counter) ] = 0.0 if 'adv' not in keys else self.accTags[idxq]['adv'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfDeterminers" % (counter) ] = 0.0 if 'det' not in keys else self.accTags[idxq]['det'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfAuxiliars" % (counter) ] = 0.0 if 'aux' not in keys else self.accTags[idxq]['aux'] / nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfPrepositions" % (counter) ] = 0.0 if 'prep' not in keys else self.accTags[idxq]['prep']/ nTags 
            counter+=1
            featuresToUse["%02d.PercentageOfPronotuns" % (counter) ] = 0.0 if 'pron' not in keys else self.accTags[idxq]['pron'] / nTags 
            counter+=1
            # Related to actual query
            featuresToUse["%02d.hasNouns" % (counter) ] = False if 'noun' not in keys else self.accTags[idxq]['noun'] > 0
            counter+=1
            featuresToUse["%02d.hasAdjectives" % (counter) ] = False if 'adj' not in keys else self.accTags[idxq]['adj'] > 0 
            counter+=1
            featuresToUse["%02d.hasConjuctions" % (counter) ] = False if 'conj' not in keys else self.accTags[idxq]['conj'] > 0 
            counter+=1
            featuresToUse["%02d.hasVerbs" % (counter) ] = False if 'verb' not in keys else self.accTags[idxq]['verb'] > 0
            counter+=1
            featuresToUse["%02d.hasOfShapes" % (counter) ] = False if 'shape' not in keys else self.accTags[idxq]['shape'] > 0
            counter+=1
            featuresToUse["%02d.hasOfPunctuations" % (counter) ] = False if 'punc' not in keys else self.accTags[idxq]['punc'] > 0
            counter+=1
            featuresToUse["%02d.hasOfAdverbs" % (counter) ] = False if 'adv' not in keys else self.accTags[idxq]['adv'] > 0
            counter+=1
            featuresToUse["%02d.hasOfDeterminers" % (counter) ] = False if 'det' not in keys else self.accTags[idxq]['det'] > 0
            counter+=1
            featuresToUse["%02d.hasOfAuxiliars" % (counter) ] = False if 'aux' not in keys else self.accTags[idxq]['aux'] > 0
            counter+=1
            featuresToUse["%02d.hasOfPrepositions" % (counter) ] = False if 'prep' not in keys else self.accTags[idxq]['prep'] > 0
            counter+=1
            featuresToUse["%02d.hasOfPronotuns" % (counter) ] = False if 'pron' not in keys else self.accTags[idxq]['pron'] > 0
            counter+=1


        if "gn" in groups:
            # Group of features that contains last in the name
            #Group 1:
            featuresToUse["%02d.CharsInQuery" % (counter) ] = self.numberOfChars[idxq]
            counter+=1
            featuresToUse["%02d.WordsInQuery" % (counter) ] = self.numberOfWords[idxq]
            counter+=1
            featuresToUse["%02d.UsedNLQuery" % (counter) ] = self.useOfNL[idxq] == 1
            counter+=1
            featuresToUse["%02d.UsedMedAbbQuery" % (counter) ] = self.useOfMedAbb[idxq] == 1
            counter+=1
            #Group 4:
            featuresToUse["%02d.SearchedSymptomQuery" % (counter) ] = (self.symptoms[idxq] == 1)
            counter+=1
            featuresToUse["%02d.SearchedCauseQuery" % (counter) ] =   (self.causes[idxq] == 1)
            counter+=1
            featuresToUse["%02d.SearchedRemedyQuery" % (counter) ] =   (self.remedies[idxq] == 1)
            counter+=1
            featuresToUse["%02d.SearchedForNonSymCauseRemedyQuery" % (counter) ] = (self.notMedical[idxq] == 1)
            counter+=1
           
            #Group 5:
            featuresToUse["%02d.NumberOfMeshInQuery" % (counter) ] = self.listNumberOfMeshConcepts[idxq]
            counter+=1
            featuresToUse["%02d.MeSHDepthInQuery" % (counter) ] = self.listMeshDepth[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfSourcesInQuery" % (counter) ] = self.listOfSources[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfConceptsInQuery" % (counter) ] = self.listOfConcepts[idxq]
            counter+=1

            #Group 6:
            featuresToUse["%02d.NumberOfCHVDataQuery" % (counter) ] = self.chvdata[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfCHVQuery" % (counter) ] = self.chvf[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfUMLSQuery" % (counter) ] = self.umls[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfCHVMisspelledQuery" % (counter) ] = self.chvMisspelled[idxq]
            counter+=1
            featuresToUse["%02d.NumberOfComboScoreQuery" % (counter) ] = self.comboScore[idxq]
            counter+=1

            #Group 7
            keys = self.accTags[idxq].keys()
            featuresToUse["%02d.hasNouns" % (counter) ] = False if 'noun' not in keys else self.accTags[idxq]['noun'] > 0
            counter+=1
            featuresToUse["%02d.hasAdjectives" % (counter) ] = False if 'adj' not in keys else self.accTags[idxq]['adj'] > 0 
            counter+=1
            featuresToUse["%02d.hasConjuctions" % (counter) ] = False if 'conj' not in keys else self.accTags[idxq]['conj'] > 0 
            counter+=1
            featuresToUse["%02d.hasVerbs" % (counter) ] = False if 'verb' not in keys else self.accTags[idxq]['verb'] > 0
            counter+=1
            featuresToUse["%02d.hasOfShapes" % (counter) ] = False if 'shape' not in keys else self.accTags[idxq]['shape'] > 0
            counter+=1
            featuresToUse["%02d.hasOfPunctuations" % (counter) ] = False if 'punc' not in keys else self.accTags[idxq]['punc'] > 0
            counter+=1
            featuresToUse["%02d.hasOfAdverbs" % (counter) ] = False if 'adv' not in keys else self.accTags[idxq]['adv'] > 0
            counter+=1
            featuresToUse["%02d.hasOfDeterminers" % (counter) ] = False if 'det' not in keys else self.accTags[idxq]['det'] > 0
            counter+=1
            featuresToUse["%02d.hasOfAuxiliars" % (counter) ] = False if 'aux' not in keys else self.accTags[idxq]['aux'] > 0
            counter+=1
            featuresToUse["%02d.hasOfPrepositions" % (counter) ] = False if 'prep' not in keys else self.accTags[idxq]['prep'] > 0
            counter+=1
            featuresToUse["%02d.hasOfPronotuns" % (counter) ] = False if 'pron' not in keys else self.accTags[idxq]['pron'] > 0
            counter+=1


        #TODO: reference to the last query
        #if "gl" in groups:
        #print featuresToUse

        return featuresToUse

        #TODO: remove this after wsdm result is issued
        #if version == "wsdm":
        #    return {'00.queriesPerSession':self.numberOfQueries/self.numberOfSessions, '01.charsPerQueries':self.numberOfChars/self.numberOfQueries,'02.usingNL':self.usingNL, '03.meanMeshDepth':self.meanMeshDepth, '04.meanWordsPerQuery': self.meanWordsPerQuery, '05.meanTimePerSession': self.meanTimePerSession, '06.usingMedicalAbbreviation':self.usingAbbreviation, '07.usingSymptonSemanticType':self.usingSymptons, '08.usingCauseSemanticType':self.usingCause, '09.usingRemedySemanticType':self.usingRemedy, '10.usingNotMedicalSemanticTypes':self.usingNotMedical, '11.didExpansion': self.expansion ,'12.didShrinkage': self.shrinkage ,'13.didReformulation': self.reformulation , '14.didExpShrRef':self.expshrref}

def createDictOfUsers(data, label):
    userDict = dict()
    users = set( (member.userId for member in data) )
    #General
    countingNumberOfQueriesPerUser = calculateNumberOfQueriesPerUser(data)
    #Group 1
    countingNumberOfCharsPerUser = calculateNumberOfCharsPerUser(data)
    countingWordsPerUser = calculateWordsPerUser(data)
    countingNLPerUser = calculateNLPerUser(data)
    countingMedicalAbbreviations = calculateMedicalAbbreviations(data)
    #Group 2
    countingTotalTimePerSession, countingNumberOfSessionsPerUser = calculateTimePerSession(data)
    #Group 3
    countingUserExpa, countingUserShri, countingUserModi, countingUserKeep = calculateUserBehavior(data)
    #Group 4
    countingSymptoms = calculateUsingSemantic(data, symptomTypes())
    countingCause = calculateUsingSemantic(data, causeTypes())
    countingRemedy = calculateUsingSemantic(data, remedyTypes())
    countingNotMedical = calculateUsingSemantic(data, noMedicalTypes())
    #Group 5
    countingListUseMeshPerUser, countingMeshDepthPerUser = calculateMeshDepthPerUser(data)
    countingSources, setOfAllSources = calculateSources(data)
    countingConcetps, setOfAllConcepts = calculateConcepts(data)
    #Group 6
    countingCHVD, countingCHVF, countingUMLS, countingCHVM, countingCHVS = calculateCHV(data)
    #Group 7
    countingTags = calculateTags(data)

    for user in users:
        # General 
        nq = countingNumberOfQueriesPerUser[user]
        # Group 1
        nc = countingNumberOfCharsPerUser[user]
        wpu = countingWordsPerUser[user]
        uab = countingMedicalAbbreviations[user]
        unl = countingNLPerUser[user]
        #Group 2
        ttps = countingTotalTimePerSession[user]
        ns = countingNumberOfSessionsPerUser[user]
        #Group 3
        expa = countingUserExpa[user]
        shri = countingUserShri[user]
        modi = countingUserModi[user]
        keeps = countingUserKeep[user] 
        #Group 4
        usy = countingSymptoms[user]
        usc = countingCause[user]
        usrd = countingRemedy[user]
        usnm = countingNotMedical[user]
        #Group 5
        mmd = [] if user not in countingMeshDepthPerUser else countingMeshDepthPerUser[user]
        lum = countingListUseMeshPerUser[user]
        lofs = countingSources[user]
        soas = setOfAllSources[user]
        lofc = countingConcetps[user]
        soac = setOfAllConcepts[user]
        #Group 6
        chvd = countingCHVD[user]
        chvf = countingCHVF[user]
        umls = countingUMLS[user]
        chvm = countingCHVM[user]
        chvs = countingCHVS[user]
        #Group 7
        tags = countingTags[user]
        
        userDict[user] = userClass(user, label, nq=nq, nc=nc, wpu=wpu, unl=unl, uab=uab, ns=ns, ttps=ttps,\
                                   expa=expa, shri=shri, modi=modi, keeps=keeps,\
                                   usy=usy, usc=usc, usrd=usrd, usnm=usnm, lum=lum, mmd=mmd, lofs=lofs, soas=soas, lofc=lofc, soac=soac,\
                                   chvd=chvd, chvf=chvf, umls=umls, chvm=chvm, chvs=chvs,tags=tags)

    return userDict

#### ========================= METRICS ============================ #####
def calculateTags(data):
    mapUserListOfTags = defaultdict(list)
    userIds = sorted( (member.userId, member.datetime, member.postags) for member in data)

    for (userId, _, tags) in userIds:
        lastQ = Counter([])
        if tags:
            c = Counter( [t for t in tags] )
            
            if userId in mapUserListOfTags:
                lastQ = mapUserListOfTags[userId][-1]
            mapUserListOfTags[userId].append(lastQ + c)
        else:
            mapUserListOfTags[userId].append(lastQ)
    
    return mapUserListOfTags
    
def calculateConcepts(data):
    mapUserConcepts = defaultdict(list)
    accSetOfConcepts = defaultdict(list)
    
    userIds = sorted( (member.userId, member.datetime,  member.concepts) for member in data)
    for (userId, _, concepts) in userIds:
        accSet = set()
        if len(accSetOfConcepts[userId]) > 0:
            accSet = set(accSetOfConcepts[-1])
        
        if concepts:
            mapUserConcepts[userId].append( len(concepts) )
            accSetOfConcepts[userId].append( set(concepts).union(accSet) )
        else:
            mapUserConcepts[userId].append(0)
            accSetOfConcepts[userId].append(accSet)
        
    return mapUserConcepts, accSetOfConcepts

def calculateSources(data):
    mapUserSource = defaultdict(list)
    accSetOfSources = defaultdict(list)
    
    userIds = sorted( (member.userId, member.datetime, member.sourceList) for member in data)

    for (userId, _, sourceList) in userIds:
        accSet = set()
        if len(accSetOfSources[userId]) > 0:
            accSet = set(accSetOfSources[-1])
     
        if sourceList:
            mapUserSource[userId].append( len(sourceList) )
            accSetOfSources[userId].append( set(sourceList).union(accSet) )
        else:
            mapUserSource[userId].append( 0 )
            accSetOfSources[userId].append( accSet )

    #for k, v in mapUserSource.iteritems():
    #    print k, v
    
    #for k, v in accSetOfSources.iteritems():
    #    print k, v

    return mapUserSource, accSetOfSources

def calculateNLPerUser(data):
    mapUserNL = defaultdict(list)
    
    userIds = sorted( (member.userId, member.datetime, member.keywords) for member in data )
    
    for (userId, _, keywords) in userIds:
        mapUserNL[userId].append( 1 if hasNLword(keywords) else 0 )

    #print "mapUserNL ---> ", mapUserNL
    return mapUserNL

def hasNLword(words):
    #print ( [ w for w in words if w.lower() in NLWords ] )
    return any( [ w for w in words if w.lower() in NLWords ] )

def calculateMedicalAbbreviations(data):
    mapUserAbb = defaultdict(list)
    
    userIds = sorted( (member.userId, member.datetime, member.keywords) for member in data )
    
    for (userId, _, keywords) in userIds:
        mapUserAbb[userId].append(1 if hasAbbreviation(keywords) else 0)

    #print "mapUserAbb ---> ", mapUserAbb
    return mapUserAbb

def hasAbbreviation(words):
    return any( [ w for w in words if w.lower() in acronymsSet] )

def calculateMeshDepthPerUser(data):

    mapUserNumberOfMeshConcepts = defaultdict(list)
    mapUserDepthOfMesh = defaultdict(list)

    userIds = sorted( (member.userId, member.datetime, member.mesh) for member in data )
    
    for (userId, _, mesh) in userIds:
        if mesh is not None:
            mapUserNumberOfMeshConcepts[userId].append(len(mesh))
            mapUserDepthOfMesh[userId].append( sum( [ len(m.split(".")) for m in mesh ] ) / len(mesh) )
        else:
            mapUserNumberOfMeshConcepts[userId].append(0)
            mapUserDepthOfMesh[userId].append(0)
        
            #print mesh, len(mesh),  sum( [ len(m.split(".")) for m in mesh ] ) / len(mesh)
    
    return mapUserNumberOfMeshConcepts, mapUserDepthOfMesh
    #return mapUserTotalMeshDepth, mapUserTimesUsingMesh, mapUserMeshIds, mapUserNumberOfMeshLastQuery, mapUserDepthLastQuery

def calculateNumberOfCharsPerUser(data):
    mapUserChars = defaultdict(list)

    userWords = [ (member.userId, member.datetime, member.keywords) for member in data ]
    queryInChars = [(userId, sum(len(q) for q in query)) for (userId, _, query) in userWords]

    for (userId, lenght) in queryInChars:
        mapUserChars[userId].append(lenght)

    #for k,v in mapUserChars.iteritems():
    #    print k, v
    return mapUserChars

def calculateNumberOfQueriesPerUser(data):
    userIds = sorted( [member.userId for member in data ] ) 
    usersNumberOfQueries = [ (k , len(list(g))) for k, g in groupby(userIds) ]
    mapUserQueries = dict()
    for u, nq in usersNumberOfQueries:
        mapUserQueries[u] = nq
    
    return mapUserQueries

def calculateWordsPerUser(data):
    mapUserWords = defaultdict(list)
    userWords = sorted( [(member.userId, member.datetime, len(member.keywords)) for member in data ] )
    
    for (userId, _, lenght) in userWords:
        mapUserWords[userId].append(lenght)
    
    #for k,v in mapUserWords.iteritems():
    #    print k, v
    return mapUserWords

def hasSemanticType(words, semanticSet):
    if words is None:
        return False
    return any( [ w for w in words if w.lower() in semanticSet] )

def calculateUsingSemantic(data, semanticType):
    mapUserSemantic = defaultdict(list)

    userIds = sorted( (member.userId, member.datetime, member.semanticTypes) for member in data )
    for (userId, _, st) in userIds:
        mapUserSemantic[userId].append(1 if hasSemanticType(st, semanticType) else 0)
    return mapUserSemantic


def calculateTimePerSession(data):
    mapUserTotalTimePerSession = defaultdict(list)
    mapUserNumberOfSessions = defaultdict(list)
    #mapUserTimeLastSession = dict()
    #mapUserQueriesLastSession = dict()

    userDateBool =  sorted( (member.userId, member.datetime , member.previouskeywords is None) for member in data ) # (user, date, newSession?)

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
                mapUserNumberOfSessions[user].append(0)
                mapUserTotalTimePerSession[user].append(0)
                continue
            
            # It is a new session:
            else:
                seconds = (endDate - startDate).total_seconds()
                #print "SECONDS --> ", seconds 
               
                # Reset the date limits
                startDate = date
                endDate = date
                
                #totalSeconds += seconds
                #numberOfSessions += 1
                
                mapUserNumberOfSessions[user].append(1)
                mapUserTotalTimePerSession[user].append(seconds)
        
        #the last session
        seconds = (endDate - startDate).total_seconds()
        #print "SECONDS --> ", seconds 
       
        #It is the end of the last session
        #totalSeconds += seconds
        #numberOfSessions += 1
        
        mapUserNumberOfSessions[user].append(1)
        mapUserTotalTimePerSession[user].append(seconds)

        #for k,v in mapUserNumberOfSessions.iteritems():
        #    print k, v
        #for k,v in mapUserTotalTimePerSession.iteritems():
        #    print k, v
        
        #print "User = ", user, " MeanTime =", mapUserMeanTimePerSession[user]
    
    return mapUserTotalTimePerSession, mapUserNumberOfSessions

def calculateUserBehavior(data):
    
    mapUserExpa = defaultdict(list)
    mapUserModi = defaultdict(list)
    mapUserShri = defaultdict(list)
    mapUserKeep = defaultdict(list)
    tmpMap = defaultdict(list)
    
    userBehavior = sorted( (member.userId, member.datetime, member.keywords) for member in data )

    for user, _, keywords in userBehavior:
        tmpMap[user].append(keywords)
        
    for user, keywordsList in tmpMap.iteritems():
        previous = []
        for keywords in keywordsList:
            expa, shri, modi, keep = compareSets(set(previous), set(keywords))
            mapUserExpa[user].append(expa)
            mapUserShri[user].append(shri)
            mapUserModi[user].append(modi)
            mapUserKeep[user].append(keep)
            previous = keywords
    
    return mapUserExpa, mapUserShri, mapUserModi, mapUserKeep

def calculateCHV(data):

    tmpCHV = sorted((member.userId, member.datetime, member.CHVFound, 1 if member.hasCHV == True else 0, 1 if member.hasUMLS == True else 0,\
                     1 if member.hasCHVMisspelled == True else 0, float(member.comboScore)) for member in data)
    mapCHVD = defaultdict(list)
    mapCHVF = defaultdict(list)
    mapUMLS = defaultdict(list)
    mapCHVM = defaultdict(list)
    mapCHVS = defaultdict(list)

    for (user, _, chvfound, hasCHV, hasUMLS, chvMisspelled, comboScore) in tmpCHV:
         mapCHVD[user].append(chvfound)
         mapCHVF[user].append(hasCHV)
         mapUMLS[user].append(hasUMLS)
         mapCHVM[user].append(chvMisspelled)
         mapCHVS[user].append(comboScore)
    
    return mapCHVD, mapCHVF, mapUMLS, mapCHVM, mapCHVS

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

def healthNotHealthUsers(minimalNumberOfQueries, maxNumberOfQueries, smallDataset):
    if smallDataset:
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

def regularMedicalUsers(minimalNumberOfQueries, maxNumberOfQueries, explanation, smallDataset):
    ####
    ### Load Datasets
    ##
    #
    if smallDataset:
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
        testA_ = createFV( "v62", 0, minNumberOfQueries, maxNumberOfQueries)
        testB_ = createFV( "v63", 1, minNumberOfQueries, maxNumberOfQueries)
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
    op.add_option("--1p", "-s", action="store_true", dest="smallDataset", help="Just create the feature vectors based on 1% of the datasets", default=False)

    (opts, args) = op.parse_args()
    if len(args) > 0:
        print "This program does not receive parameters this way: use -h to see the options."
    
    if opts.testingOnly:
        testing(opts.minNumberOfQueries, opts.maxNumberOfQueries, opts.explanation)
        sys.exit(0)

    if opts.healthUsers:
        healthNotHealthUsers(opts.minNumberOfQueries, opts.maxNumberOfQueries, opts.explanation, opts.smallDataset)
    else:
        regularMedicalUsers(opts.minNumberOfQueries, opts.maxNumberOfQueries, opts.explanation, opts.smallDataset)

