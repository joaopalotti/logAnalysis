from __future__ import division
from collections import defaultdict, Counter
import operator
from datetime import datetime

from metrics import generateStatsVector
from myPlot import plotter
from latexTools import latexPrinter
from auxiliarFunctions import *
from plotFunctions import *

"""
SOME IMPORTANT NOTES:
    -> Keeping the stop words.
    -> Considering that more than 100 queries in one unique session is way too much. So, the session is removed.
"""

# GLOBAL VARIABLES:
numberOfQueriesInASessionThreshold = 100
removeOutliers=True

def calculateMetrics(dataList, removeStopWords=False, printValuesToFile=True):
    """
        Expected a list of list of DataSet (TripData or AolData) objects
    """
    countingAcronymsList = []
    countingTimePerSessionList = []
    countingTokensList = []
    countingQueriesList = []
    countingQueriesPerSessionList = []
    countingMeshList = []
    countingDiseaseList = []
    countingMeshDepthList = []
    countingQueriesPerUserList = []
    countingQueryRankingList = []
    
    tableGeneralHeader = [["Dtst", "#Days", "#Users", "#Qrs", "mnWrdsPQry", "stdmnWrdsPQry", "medianWrdsPQry", "mnQrsPDay", "Sssions", "mnQrsPrSsion", "stdQrsPrSssion", "medianQrsPrSssion", "mTimePrSsion", "stdTimePrSssion", "medianTimePrSssion", "Users #NL", "Users %NL", "QueriesNL", "%QueriesNL", "%UsersReAccess", "%SssnsReAccess", "QueriesAcronym", "%QAcronym", "UsersAcronym", "%UsersAcronym", "UsersSemantics", "%UserSemantics"]]

    tableGeneralMeshHeader = [["Dtst", "QrsWithMesh", "% QrsWithMesh", "MeshIds", "MeshIds/#Qrs", "DiseIds", "DiseIds/#Qrs","#UsersUsingMesh","#UsersUsingMesh/#Users", "MeanUserMeshDepth"]]
    tableMeshHeader = [ ["Dtst(%)","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
    tableDiseasesHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]

    tableSemanticFocusHeader = [ ["Dtst", "Nothing", "Symptom", "Cause", "Remedy", "SymptomCause", "SymptomRemedy", "CauseRemedy", "SymptomCauseRemedy"] ]
    tableCicleSequenceHeader = [["Dtst", "Gross", "Perc", "SCS", "SRS", "CSC", "CRC", "RSR", "RCR"]] 
    
    tableModifiedSessionHeader = [["Dtst","Nothing","Expansion","Shrinkage","Reformulation","ExpansionShrinkage","ExpansionReformulation","ShrinkageReformulation","ExpansionShrinkageReformulation"]] 
    tableGeneralModifiedHeader = [["Dtst", "Exp", "Exp(%)", "Shr", "Shr(%)", "Ref", "Ref(%)", "Rep", "Rep(%)" ]]
    tableMeshDepthHeader = [["Dtst(%)", "Depth 1", "Depth 2", "Depth 3", "Depth 4", "Depth 5", "Depth 6", "Depth 7", "Depth 8", "Depth 9", "Depth 10","Depth 11", "Depth 12"]]
    tableSemanticByUserHeader = [["Dtst", "Symptom", "Symptom (%)", "Cause", "Cause (%)", "Remedy", "Remedy (%)", "Where", "Where (%)", "noMedical", "noMedical (%)"]] 
    tableSemanticByUserWeightedHeader = [["Dtst", "Symptom", "Symptom (%)", "Cause", "Cause (%)", "Remedy", "Remedy (%)", "Where", "Where (%)", "noMedical", "noMedical (%)"]] 
    tableMeshByUserHeader = [ ["Dtst","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
    tableDiseaseByUserHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]
    tableMeshByUserWeightedHeader = [ ["Dtst","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
    tableDiseaseByUserWeightedHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]
    tableBooleanUseHeader = [["Dtst", "# of ands", "% of ands", "# of ors", "% of ors",  "# of nots", "% of nots", "at least one", "% of booleans" ]]

    generalTableRow = []
    generalMeshRow = []
    meshTableRow = []
    diseaseTableRow = []
    semanticFocusRow = []
    cicleSequenceRow = []
    generalModifiedRow = []
    modifiedSessionRow = []
    meshDepthRow = []
    semanticByUserRow = []
    semanticByUserWeightedRow = []
    meshByUserRow = []
    diseaseByUserRow = []
    meshByUserWeightedRow = []
    diseaseByUserWeightedRow = []
    booleanUseRow = []

    for dataPair in dataList:
        data, dataName = dataPair[0], dataPair[1]
        print "Processing information for data: ", dataName

        data = preProcessData(data, removeStopWords)
        
        '''
        It is important to run the session analyse first because it is going to eliminate users considered as robots (more than X queries in one unique session)
        X -> numberOfQueriesInASessionThreshold, but you may want to check it later
        '''
        
        if removeOutliers:
            outliersToRemove = removeOutliers( createSessions(data) )
            newData = [member for member in data if member.userId not in outliersToRemove]
            data = newData

        
        numberOfSessions, countingQueriesPerSession, npNumQueriesInSession, countingTimePerSession, npTime,\
            numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions,\
            countingSemantics, countingPureSemanticTypes, vectorOfActionSequence,\
            countingReAccess, idMaxQueriesInSession, vectorOfCicleSequence, countingFullSemanticTypes,\
                userSemanticType = calculateQueriesPerSession(data)
        
        semanticTypesCountedByUser, semanticTypesCountedByUserWeighted, setOfUsersWithSemantic = calculateSemanticTypesPercentages(userSemanticType)

       
        hasAcronym, countingAcronyms, usersUsingAcronyms = calculateAcronyms(data)

        numberOfUsers = calculateUsers(data)
        npTerms, booleanTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, greatestQuery, countingQueries, tenMostCommonTermsNoStopWord = calculateTerms(data)
               
        firstDay, lastDay, countingSessionsPerDay, countingQueriesPerDay, meanSessionsPerDay, meanQueriesPerDay = calculateDates(data)
        countingNL = calculateNLuse(data)
        countingQueriesPerUser = calculateQueriesPerUser(data)
        countingQueryRanking = calculateQueryRanking(data)

        usersMetrics = calculateMetricsForUsers(data)

        numberOfQueries = sum(countingQueries.values())
        percentageAcronymInQueries = 100.0 * len(hasAcronym) / numberOfQueries

        hasMeshValues = 0
        countingMesh, countingDisease, hasMeshValues, countingMeshDepth, usersUsingMesh, mapUserMeanMeshDepth, \
                countingMeshByUser, countingDiseaseByUser, countingMeshWeightedByUser, countingDiseaseWeightedByUser  = calculateMesh(data)

        # Print statistics
        with open(dataName + ".result", "w") as f:
            print "Writing file ", dataName + ".result..."
            f.write("Metrics calculated:\n")
            printGeneralMetrics(f, numberOfUsers, numberOfQueries, numberOfSessions, firstDay, lastDay)
            printMetricsForTerms(f, npTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, percentageAcronymInQueries, countingAcronyms, countingNL, numberOfUsers, tenMostCommonTermsNoStopWord, numberOfQueries)
            printMetricsForQueries(f, greatestQuery, countingQueries, countingQueriesPerDay, meanQueriesPerDay)
            printMetricsForSessions(f, numberOfSessions, numberOfQueries, npNumQueriesInSession, npTime,\
                                    numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions,\
                                   countingSessionsPerDay, meanSessionsPerDay, countingReAccess, numberOfUsers, idMaxQueriesInSession)
            printMeshClassificationMetrics(f, countingMesh, countingDisease, numberOfQueries, hasMeshValues, countingMeshDepth)
            printSemantic(f, vectorOfActionSequence, vectorOfCicleSequence, countingFullSemanticTypes, numberOfQueries)
            printOutliers(f, outliersToRemove)

        countingAcronymsList.append([dataName, countingAcronyms])
        countingTimePerSessionList.append( [ dataName , countingTimePerSession ])
        countingTokensList.append( [dataName, countingTokens] )
        countingQueriesList.append([dataName, countingQueries] )
        countingQueriesPerSessionList.append([dataName, countingQueriesPerSession])
        countingMeshList.append([dataName, countingMesh])
        countingDiseaseList.append([dataName, countingDisease])
        countingMeshDepthList.append([dataName, countingMeshDepth])
        countingQueriesPerUserList.append( [dataName, countingQueriesPerUser] )
        countingQueryRankingList.append( [dataName, countingQueryRanking] )

        #Data for tables
        numberOfMeshTerms = sum(countingMesh.values())
        numberOfMeshDiseases = sum(countingDisease.values())

        generalTableRow.append( [ dataName, (lastDay - firstDay).days, numberOfUsers, numberOfQueries, npTerms.mean, npTerms.std, npTerms.median, meanQueriesPerDay, numberOfSessions, npNumQueriesInSession.mean, npNumQueriesInSession.std, npNumQueriesInSession.median, npTime.mean, npTime.std, npTime.median, len(countingNL), 100*len(countingNL)/numberOfUsers, sum(countingNL.values()), 100 * sum(countingNL.values())/numberOfQueries, 100*len(countingReAccess)/numberOfUsers, 100*sum(countingReAccess.values())/numberOfSessions, len(hasAcronym), percentageAcronymInQueries, len(usersUsingAcronyms), 100.0 * len(usersUsingAcronyms) / numberOfUsers, len(setOfUsersWithSemantic), 100.0 * len(setOfUsersWithSemantic) / numberOfUsers  ] )
        generalModifiedRow.append( [dataName, numberOfExpansions, 100.0 * numberOfExpansions/ numberOfQueries , numberOfShrinkage, 100 * numberOfShrinkage/ numberOfQueries, numberOfReformulations, 100 * numberOfReformulations/numberOfQueries, numberOfRepetitions, 100 * numberOfRepetitions/numberOfQueries] )
        generalMeshRow.append( [dataName,  hasMeshValues, 100.0 * hasMeshValues/numberOfQueries, numberOfMeshTerms, numberOfMeshTerms/numberOfQueries, numberOfMeshDiseases, numberOfMeshDiseases/numberOfQueries, len(usersUsingMesh), 100.0*len(usersUsingMesh)/numberOfUsers, sum(mapUserMeanMeshDepth.values())/len(mapUserMeanMeshDepth.items()) ] ) 

        #To avoid division by zero
        numberOfMeshTerms = numberOfMeshTerms if numberOfMeshTerms != 0 else 1
        numberOfMeshDiseases = numberOfMeshDiseases if numberOfMeshDiseases != 0 else 1
        
        meshTableRow.append( [ dataName, 100 * countingMesh["A"]/ numberOfMeshTerms, 100 * countingMesh["B"]/ numberOfMeshTerms, 100 * countingMesh["C"]/ numberOfMeshTerms, 100 * countingMesh["D"]/ numberOfMeshTerms, 100 * countingMesh["E"]/ numberOfMeshTerms, 100 * countingMesh["F"]/ numberOfMeshTerms, 100 * countingMesh["G"]/ numberOfMeshTerms, 100 * countingMesh["H"]/ numberOfMeshTerms, 100 * countingMesh["I"]/ numberOfMeshTerms, 100 * countingMesh["J"]/ numberOfMeshTerms, 100 * countingMesh["K"]/ numberOfMeshTerms, 100 * countingMesh["L"]/ numberOfMeshTerms, 100 * countingMesh["M"]/ numberOfMeshTerms, 100 * countingMesh["N"]/ numberOfMeshTerms, 100 * countingMesh["V"]/ numberOfMeshTerms, 100 * countingMesh["Z"]/ numberOfMeshTerms  ] )
        diseaseTableRow.append( [ dataName,  100 * countingDisease["C01"]/ numberOfMeshDiseases, 100 * countingDisease["C02"]/ numberOfMeshDiseases, 100 * countingDisease["C03"]/ numberOfMeshDiseases, 100 * countingDisease["C04"]/ numberOfMeshDiseases, 100 * countingDisease["C05"]/ numberOfMeshDiseases, 100 * countingDisease["C06"]/ numberOfMeshDiseases, 100 * countingDisease["C07"]/ numberOfMeshDiseases, 100 * countingDisease["C08"]/ numberOfMeshDiseases, 100 * countingDisease["C09"]/ numberOfMeshDiseases, 100 * countingDisease["C10"]/ numberOfMeshDiseases, 100 * countingDisease["C11"]/ numberOfMeshDiseases, 100 * countingDisease["C12"]/ numberOfMeshDiseases, 100 * countingDisease["C13"]/ numberOfMeshDiseases, 100 * countingDisease["C14"]/ numberOfMeshDiseases, 100 * countingDisease["C15"]/ numberOfMeshDiseases, 100 * countingDisease["C16"]/ numberOfMeshDiseases, 100 * countingDisease["C17"]/ numberOfMeshDiseases, 100 * countingDisease["C18"]/ numberOfMeshDiseases, 100 * countingDisease["C19"]/ numberOfMeshDiseases, 100 * countingDisease["C20"]/ numberOfMeshDiseases, 100 * countingDisease["C21"]/ numberOfMeshDiseases, 100 * countingDisease["C22"]/ numberOfMeshDiseases, 100 * countingDisease["C23"]/ numberOfMeshDiseases, 100 * countingDisease["C24"]/ numberOfMeshDiseases, 100 * countingDisease["C25"]/ numberOfMeshDiseases, 100 * countingDisease["C26"]/ numberOfMeshDiseases ] )
        meshByUserRow.append( [ dataName, 100 * countingMeshByUser["A"]/ numberOfUsers, 100 * countingMeshByUser["B"]/ numberOfUsers, 100 * countingMeshByUser["C"]/ numberOfUsers, 100 * countingMeshByUser["D"]/ numberOfUsers, 100 * countingMeshByUser["E"]/ numberOfUsers, 100 * countingMeshByUser["F"]/ numberOfUsers, 100 * countingMeshByUser["G"]/ numberOfUsers, 100 * countingMeshByUser["H"]/ numberOfUsers, 100 * countingMeshByUser["I"]/ numberOfUsers, 100 * countingMeshByUser["J"]/ numberOfUsers, 100 * countingMeshByUser["K"]/ numberOfUsers, 100 * countingMeshByUser["L"]/ numberOfUsers, 100 * countingMeshByUser["M"]/ numberOfUsers, 100 * countingMeshByUser["N"]/ numberOfUsers, 100 * countingMeshByUser["V"]/ numberOfUsers, 100 * countingMeshByUser["Z"]/ numberOfUsers  ] )
        diseaseByUserRow.append( [ dataName,  100 * countingDiseaseByUser["C01"]/ numberOfUsers, 100 * countingDiseaseByUser["C02"]/ numberOfUsers, 100 * countingDiseaseByUser["C03"]/ numberOfUsers, 100 * countingDiseaseByUser["C04"]/ numberOfUsers, 100 * countingDiseaseByUser["C05"]/ numberOfUsers, 100 * countingDiseaseByUser["C06"]/ numberOfUsers, 100 * countingDiseaseByUser["C07"]/ numberOfUsers, 100 * countingDiseaseByUser["C08"]/ numberOfUsers, 100 * countingDiseaseByUser["C09"]/ numberOfUsers, 100 * countingDiseaseByUser["C10"]/ numberOfUsers, 100 * countingDiseaseByUser["C11"]/ numberOfUsers, 100 * countingDiseaseByUser["C12"]/ numberOfUsers, 100 * countingDiseaseByUser["C13"]/ numberOfUsers, 100 * countingDiseaseByUser["C14"]/ numberOfUsers, 100 * countingDiseaseByUser["C15"]/ numberOfUsers, 100 * countingDiseaseByUser["C16"]/ numberOfUsers, 100 * countingDiseaseByUser["C17"]/ numberOfUsers, 100 * countingDiseaseByUser["C18"]/ numberOfUsers, 100 * countingDiseaseByUser["C19"]/ numberOfUsers, 100 * countingDiseaseByUser["C20"]/ numberOfUsers, 100 * countingDiseaseByUser["C21"]/ numberOfUsers, 100 * countingDiseaseByUser["C22"]/ numberOfUsers, 100 * countingDiseaseByUser["C23"]/ numberOfUsers, 100 * countingDiseaseByUser["C24"]/ numberOfUsers, 100 * countingDiseaseByUser["C25"]/ numberOfUsers, 100 * countingDiseaseByUser["C26"]/ numberOfUsers ] )
        meshByUserWeightedRow.append( [ dataName, 100 * countingMeshWeightedByUser["A"]/ numberOfUsers, 100 * countingMeshWeightedByUser["B"]/ numberOfUsers, 100 * countingMeshWeightedByUser["C"]/ numberOfUsers, 100 * countingMeshWeightedByUser["D"]/ numberOfUsers, 100 * countingMeshWeightedByUser["E"]/ numberOfUsers, 100 * countingMeshWeightedByUser["F"]/ numberOfUsers, 100 * countingMeshWeightedByUser["G"]/ numberOfUsers, 100 * countingMeshWeightedByUser["H"]/ numberOfUsers, 100 * countingMeshWeightedByUser["I"]/ numberOfUsers, 100 * countingMeshWeightedByUser["J"]/ numberOfUsers, 100 * countingMeshWeightedByUser["K"]/ numberOfUsers, 100 * countingMeshWeightedByUser["L"]/ numberOfUsers, 100 * countingMeshWeightedByUser["M"]/ numberOfUsers, 100 * countingMeshWeightedByUser["N"]/ numberOfUsers, 100 * countingMeshWeightedByUser["V"]/ numberOfUsers, 100 * countingMeshWeightedByUser["Z"]/ numberOfUsers  ] )
        diseaseByUserWeightedRow.append( [ dataName,  100 * countingDiseaseWeightedByUser["C01"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C02"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C03"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C04"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C05"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C06"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C07"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C08"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C09"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C10"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C11"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C12"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C13"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C14"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C15"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C16"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C17"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C18"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C19"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C20"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C21"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C22"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C23"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C24"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C25"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C26"]/ numberOfUsers ] )
        # ["Dtst", "Nothing", "Symptom", "Cause", "Remedy", "SymptomCause", "SymptomRemedy", "CauseRemedy", "SymptomCauseRemedy"]
        totalActions = sum(vectorOfActionSequence)
        totalActions = 1/100 if totalActions == 0 else totalActions

        semanticFocusRow.append( [ dataName, 100 * vectorOfActionSequence[0]/totalActions, 100 * vectorOfActionSequence[1]/totalActions, 100 * vectorOfActionSequence[2]/totalActions, 100 * vectorOfActionSequence[4]/totalActions, 100 * vectorOfActionSequence[3]/totalActions, 100 * vectorOfActionSequence[5]/totalActions, 100 * vectorOfActionSequence[6]/totalActions, 100 * vectorOfActionSequence[7]/totalActions ] )

        #["Dtst","Nothing","Expansion","Shrinkage","Reformulation","ExpansionShrinkage","ExpansionReformulation","ShrinkageReformulation","ExpansionShrinkageReformulation"]
        totalOfModifiedSessions = sum(vectorOfModifiedSessions)
        totalOfModifiedSessions = 1/100 if totalOfModifiedSessions == 0 else totalOfModifiedSessions

        modifiedSessionRow.append( [dataName, 100 * vectorOfModifiedSessions[0]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[4]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[2]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[1]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[6]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[5]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[3]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[7]/totalOfModifiedSessions ] )
        
        totalCicleSequence = sum(vectorOfCicleSequence)
        totalCicleSequence = 1/100 if totalCicleSequence == 0 else totalCicleSequence
        cicleSequenceRow.append( [dataName, totalCicleSequence, 100.0 * totalCicleSequence/numberOfSessions, 100 * vectorOfCicleSequence[0]/totalCicleSequence, 100 * vectorOfCicleSequence[1]/totalCicleSequence, 100 * vectorOfCicleSequence[2]/totalCicleSequence, 100 * vectorOfCicleSequence[3]/totalCicleSequence, 100 * vectorOfCicleSequence[4]/totalCicleSequence, 100 * vectorOfCicleSequence[5]/totalCicleSequence] )
    
        totalMeshDepth = sum(countingMeshDepth.values())
        totalMeshDepth = 1/100 if totalMeshDepth == 0 else totalMeshDepth
        meshDepthRow.append( [dataName, 100/totalMeshDepth * countingMeshDepth[1], 100/totalMeshDepth * countingMeshDepth[2], 100/totalMeshDepth * countingMeshDepth[3], 100/totalMeshDepth * countingMeshDepth[4], 100/totalMeshDepth * countingMeshDepth[5], 100/totalMeshDepth * countingMeshDepth[6], 100/totalMeshDepth * countingMeshDepth[7],100/totalMeshDepth * countingMeshDepth[8], 100/totalMeshDepth * countingMeshDepth[9], 100/totalMeshDepth * countingMeshDepth[10], 100/totalMeshDepth * countingMeshDepth[11], 100/totalMeshDepth * countingMeshDepth[12]  ])
        
        semanticByUserRow.append( [dataName, semanticTypesCountedByUser["symptom"], 100.0 * semanticTypesCountedByUser["symptom"]/numberOfUsers, semanticTypesCountedByUser["cause"], 100.0 * semanticTypesCountedByUser["cause"]/ numberOfUsers, semanticTypesCountedByUser["remedy"], 100.0 * semanticTypesCountedByUser["remedy"]/numberOfUsers, semanticTypesCountedByUser["where"], 100.0 * semanticTypesCountedByUser["where"]/numberOfUsers, semanticTypesCountedByUser["noMedical"], 100.0 * semanticTypesCountedByUser["noMedical"]/numberOfUsers ])
        semanticByUserWeightedRow.append( [dataName, semanticTypesCountedByUserWeighted["symptom"], 100.0 * semanticTypesCountedByUserWeighted["symptom"]/numberOfUsers, semanticTypesCountedByUserWeighted["cause"], 100.0 * semanticTypesCountedByUserWeighted["cause"]/ numberOfUsers, semanticTypesCountedByUserWeighted["remedy"], 100.0 * semanticTypesCountedByUserWeighted["remedy"]/numberOfUsers, semanticTypesCountedByUserWeighted["where"], 100.0 * semanticTypesCountedByUserWeighted["where"]/numberOfUsers, semanticTypesCountedByUserWeighted["noMedical"], 100.0 * semanticTypesCountedByUserWeighted["noMedical"]/numberOfUsers ])
        booleanUseRow.append( [dataName, booleanTerms['and'], 100.0 * booleanTerms['and']/numberOfQueries, booleanTerms['or'], 100.0 * booleanTerms['or']/numberOfQueries,booleanTerms['not'], 100.0 * booleanTerms['not'] / numberOfQueries, booleanTerms['any'], 100.0 * booleanTerms['any'] / numberOfQueries ] )

    # Plot graphics
    myPlotter = plotter() 
    plotQueriesPerSession(myPlotter, countingQueriesPerSessionList, printValuesToFile)
    plotFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile)
    plotLogLogFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile)
    plotFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile)
    plotLogLogFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile)
    plotTimePerSession(myPlotter, countingTimePerSessionList, printValuesToFile)
    plotAcronymFrequency(myPlotter, countingAcronymsList, printValuesToFile)
    plotSizeOfWords(myPlotter, dataList, printValuesToFile)
    plotSizeOfQueries(myPlotter, dataList, printValuesToFile)
    plotMeshDepth(myPlotter, countingMeshDepthList, printValuesToFile)
    plotUsersByNumberOfQueries(myPlotter, countingQueriesPerUserList, printValuesToFile)
    plotQueryRanking(myPlotter, countingQueryRankingList, printValuesToFile)

    #Print latex tables:
    latexWriter = latexPrinter() 
    for l in generalTableRow: 
        tableGeneralHeader.append( l )
    for l in generalMeshRow:
        tableGeneralMeshHeader.append(l)
    for l in meshTableRow:
        tableMeshHeader.append( l )
    for l in diseaseTableRow:
        tableDiseasesHeader.append( l )
    for l in semanticFocusRow:
        tableSemanticFocusHeader.append(l)
    for l in modifiedSessionRow:
        tableModifiedSessionHeader.append(l)
    for l in generalModifiedRow:
        tableGeneralModifiedHeader.append(l)
    for l in cicleSequenceRow:
        tableCicleSequenceHeader.append(l)
    for l in meshDepthRow:
        tableMeshDepthHeader.append(l)
    for l in semanticByUserRow:
        tableSemanticByUserHeader.append(l)
    for l in semanticByUserWeightedRow:
        tableSemanticByUserWeightedHeader.append(l)
    for l in meshByUserRow:
        tableMeshByUserHeader.append(l)
    for l in diseaseByUserRow:
        tableDiseaseByUserHeader.append(l)
    for l in meshByUserWeightedRow:
        tableMeshByUserWeightedHeader.append(l)
    for l in diseaseByUserWeightedRow:
        tableDiseaseByUserWeightedHeader.append(l)
    for l in booleanUseRow:
        tableBooleanUseHeader.append(l)

    latexWriter.addTable(tableGeneralHeader, caption="General Numbers", transpose=True)
    latexWriter.addTable(tableModifiedSessionHeader, caption="Modifications in a session", transpose=True)
    latexWriter.addTable(tableGeneralModifiedHeader, caption="General Modified Statistics (Divided by the \#Queries)", transpose=True)
    latexWriter.addTable(tableGeneralMeshHeader, caption="General Mesh Statistics", transpose=True)
    latexWriter.addTable(tableMeshHeader, caption="Mesh Table", transpose=True)
    latexWriter.addTable(tableDiseasesHeader, caption="Diseases Table", transpose=True)
    latexWriter.addTable(tableMeshDepthHeader, caption="Mesh Depth", transpose=True)
    latexWriter.addTable(tableSemanticFocusHeader, caption="Semantic Focus", transpose=True)
    latexWriter.addTable(tableCicleSequenceHeader, caption="Cicle Sequence", transpose=True)
    latexWriter.addTable(tableSemanticByUserHeader, caption="Semantic counts by user", transpose=True)
    latexWriter.addTable(tableSemanticByUserWeightedHeader, caption="Semantic counts by user (WEIGHTED) - some to the number of users using some semantic", transpose=True)
    latexWriter.addTable(tableMeshByUserHeader, caption="Mesh By User (\%)", transpose=True)
    latexWriter.addTable(tableDiseaseByUserHeader, caption="Disease By User (\%)", transpose=True)
    latexWriter.addTable(tableMeshByUserWeightedHeader, caption="Mesh By User (\%) (WEIGHTED)", transpose=True)
    latexWriter.addTable(tableDiseaseByUserWeightedHeader, caption="Disease By User (\%) (WEIGHTED)", transpose=True)
    latexWriter.addTable(tableBooleanUseHeader, caption="Boolean usage", transpose=True)

    print sum(countingMeshByUser.values()), sum(countingMeshWeightedByUser.values())

def calculateSemanticTypesPercentages(userSemanticType):
    
    symptom, cause, remedy, where, noMedical = 0,0,0,0,0
    symptomSet, causeSet, remedySet, whereSet, noMedicalSet = 0,0,0,0,0
    usersWithoutSemantic, usersWithSemantic = set(), set()

    userSet = dict()
    for (user, semanticTypes) in userSemanticType.iteritems():
        userSet[user] = set(semanticTypes)

    for (user, semanticSet) in userSet.iteritems():
        if semanticSet == set():
            usersWithoutSemantic.add(user)
        if "symptom" in semanticSet:
            symptomSet += 1
        if "cause" in semanticSet:
            causeSet += 1
        if "remedy" in semanticSet:
            remedySet += 1
        if "where" in semanticSet:
            whereSet += 1
        if "noMedical" in semanticSet:
            noMedicalSet += 1
    
    for (user, semanticList) in userSemanticType.iteritems():
        if user not in usersWithoutSemantic:
            usersWithSemantic.add(user)

        for s in semanticList:
            if s == "symptom":
                symptom += ( 1 / len(semanticList) )
            if s == "cause":
                cause +=  (1 / len(semanticList) )
            if s == "remedy":
                remedy += (1 / len(semanticList) )
            if s == "where":
                where += (1 / len(semanticList) )
            if s == "noMedical":
                noMedical += ( 1 / len(semanticList) )

    return {"symptom":symptomSet, "cause":causeSet, "remedy":remedySet, "where":whereSet, "noMedical":noMedicalSet}, {"symptom":symptom, "cause":cause, "remedy":remedy, "where":where, "noMedical":noMedical}, usersWithSemantic

def calculateMetricsForUsers(data):
    pass
    #userIds = set( (member.userId) for member in data )
    #print userIds


def hasNLword(words):
    #TODO: find a better list:
    # possibility: use Noun + Verb Phrase or other structures like that
    return len( [ w for w in words if w.lower() in NLWords ] ) > 0

def calculateNLuse(data):

    #TODO: to finish it!
    countingNL = defaultdict(int)
    userKeywords = ( (member.userId, member.keywords) for member in data )

    for u, k in userKeywords:
        #print u, k
        if hasNLword(k):
            #print "FOUND Word here", k 
            countingNL[u] += 1 

    #print countingNL
    return countingNL

def calculateMesh(data):
   
    #We take only the first letter here
    meshUserValues = [ (member.userId, member.mesh) for member in data if member.mesh ]
    meshValues = [ v for (userId, values) in meshUserValues for v in values if v != '' ]

    tmpUserMesh = defaultdict(list)
    userMesh = defaultdict(list)
    for (user, mesh) in meshUserValues:
        tmpUserMesh[user].append(mesh)
    for (user, meshList) in tmpUserMesh.iteritems():
        userMesh[user] = set([m for mesh in meshList for m in mesh])
    tmpUserMesh = {} # clear memory?

    countingMeshByUser, countingDiseaseByUser, usersUsingMesh, meanMeshDepthByUser, countingMeshWeightedByUser, countingDiseaseWeightedByUser = calculateMeshMetricsByUser(userMesh)
    
    meshDepth = [ len(d.split('.')) for d in meshValues]
    countingMeshDepth = Counter(meshDepth)

    hasMeshValues =  sum( 1 for member in data if member.mesh )
    # Isolate the diseases
    meshDiseases = (values.split(".")[0] for values in meshValues if values.startswith('C'))

    # Using only the first letter in the mesh values ( C19.523.232 --> C, D2.312 -> D)
    meshValues = (values[0] for values in meshValues)
    countingDisease = Counter(meshDiseases)
    countingMesh = Counter(meshValues)
   
    return countingMesh, countingDisease, hasMeshValues, countingMeshDepth, usersUsingMesh, meanMeshDepthByUser, countingMeshByUser, countingDiseaseByUser, countingMeshWeightedByUser, countingDiseaseWeightedByUser

def calculateMeshMetricsByUser(userMesh):
    ## Structure: userMesh['1'] = set( ['A01.x.y.z','B01.a.b.c','C2.a.n.y.t.h.i.n.g'] )
    
    userMeshValue = dict()
    userDiseaseValue = dict()
    meanMeshDepthByUser = dict()
    usersUsingMesh = set()
    
    # Calculate by each user, a mesh letter value
    for (user, meshSet) in userMesh.iteritems():
        userMeshValue[user] =  set( ( m[0] for m in meshSet ) )
        userDiseaseValue[user] = set( (m.split(".")[0] for m in meshSet if m.startswith("C")) )
        meanMeshDepthByUser[user] = sum( [ len(m.split(".")) for m in meshSet ] ) / len(meshSet)
        usersUsingMesh.add(user)

    countingMeshByUser = defaultdict(int)
    countingDiseaseByUser = defaultdict(int)
    countingMeshWeightedByUser = defaultdict(int)
    countingDiseaseWeightedByUser = defaultdict(int)

    for meshValuesSet in userMeshValue.values():
        for m in meshValuesSet:
            countingMeshByUser[m] += 1
            countingMeshWeightedByUser[m] += (1 / len(meshValuesSet))

    for diseaseValuesSet in userDiseaseValue.values():
        for d in diseaseValuesSet:
            countingDiseaseByUser[d] += 1
            countingDiseaseWeightedByUser[d] += (1/len(diseaseValuesSet))
    
    return countingMeshByUser, countingDiseaseByUser, usersUsingMesh, meanMeshDepthByUser, countingMeshWeightedByUser, countingDiseaseWeightedByUser

def calculateUsers(data):
    return len(set((member.userId for member in data)))

def calculateDates(data):

    firstDay = datetime.now() 
    lastDay =  datetime.strptime("14/01/1987 12:10", "%d/%m/%Y %H:%M")
    countingSessionsPerDay = defaultdict(dict)
    countingQueriesPerDay = defaultdict(int)

    for member in data:
        firstDay = member.datetime if member.datetime < firstDay else firstDay
        lastDay = member.datetime if member.datetime > lastDay else lastDay
        
        dayMonthYear = member.datetime.strftime("%d-%m-%Y")
        countingQueriesPerDay[dayMonthYear] += 1
        if member.userId not in countingSessionsPerDay[dayMonthYear]:
            countingSessionsPerDay[dayMonthYear][member.userId] = 0
        
        countingSessionsPerDay[dayMonthYear][member.userId] += 1
 
    sessionsPerDay = [ len(countingSessionsPerDay[day]) for day in countingSessionsPerDay.keys() ]

    meanQueriesPerDay = 0 if len(countingQueriesPerDay) == 0 else sum(countingQueriesPerDay.values()) / len(countingQueriesPerDay)
    meanSessionsPerDay = 0 if len(sessionsPerDay) == 0 else sum(sessionsPerDay) / len(sessionsPerDay)

    #print firstDay, lastDay, countingSessionsPerDay, countingQueriesPerDay, meanSessionsPerDay,  meanQueriesPerDay
    return firstDay, lastDay, countingSessionsPerDay, countingQueriesPerDay, meanSessionsPerDay, meanQueriesPerDay 

def calculateAcronyms(data):
    
    acronymsSet = createAcronymSet()

    # Get the number of queries that have acronyms
    hasAcronym = [ member.keywords for member in data for word in member.keywords if word in acronymsSet]
    # Get the most common ccronyms
    acronymList = [ word for member in data for word in member.keywords if word in acronymsSet]
    countingAcronyms = Counter(acronymList)

    #Get the set of users using acronyms
    usersUsingAcronyms = set([member.userId for member in data for word in member.keywords if word in acronymsSet])

    return hasAcronym, countingAcronyms, usersUsingAcronyms

def calculateExpansionShrinkageReformulations(sessions, ignoreRepetition=True):
    
    numberOfExpansions = 0
    numberOfShrinkage = 0
    numberOfReformulations = 0
    numberOfRepetitions = 0
    
    # TODO: if I remove the ''keep dimmension'', the number of dimmensions would be only 3 -> 2**3 -> 8
    vectorOfModifiedSessions = [0]*8 if ignoreRepetition else [0]*16

    for session in sessions.values():
        for subSession in session.values():
            
            modifiedSubSession = False
            previousQuery = subSession[0]
            subQueryE, subQueryS, subQueryRef, subQueryRep = 0, 0, 0, 0
            
            for query in subSession[1:]:
                e, s, ref, rep = compareSets( set(previousQuery[1]), set(query[1]) )
                numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions =\
                        e + numberOfExpansions, s + numberOfShrinkage, ref + numberOfReformulations, rep + numberOfRepetitions
                subQueryE, subQueryS, subQueryRef, subQueryRep = subQueryE + e, subQueryS + s, subQueryRef + ref, subQueryRep + rep
                
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
                indexVal =  int( str(be) + str(bs) + str(bref), 2) if ignoreRepetition else int( str(be) + str(bs) + str(bref) + str(brep), 2)

                #print "INDEX = ", indexVal, " exp : ", be, " shr: ", bs, " ref:", bref
                vectorOfModifiedSessions[indexVal] += 1
                
    return numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions


"""
    If the number of queries in a single session is greater that the numberOfQueriesInASessionThreshold, 
    the user is considered illegal (robot?) and removed from the sessions.
"""
def removeOutliers(sessions):
    usersToRemove = set()

    for userId, session in sessions.iteritems():
        #print userId, session.values()
        m = max( len(subSession) for subSession in session.values() )
        if m > numberOfQueriesInASessionThreshold:
            print "ROBOT FOUND ----> ", userId, " Session Length: ", m
            usersToRemove.add(userId)
    
    for user in usersToRemove:
        print "DELETING USER ----> ", user
        del sessions[user]
    
    return usersToRemove
    

def createSessions(data):
    sessions = defaultdict(dict)

    for member in data:

        # There are no previous keywords and no sessions of this id -> create the first one sessions[id][1] = list
        if member.previouskeywords is None and not sessions[member.userId]:
            sessions[member.userId][1] = [[member.datetime, member.keywords, member.semanticTypes]]

        # There are no previous keywords and there is at least one sessions of this id -> another session
        elif member.previouskeywords is None and sessions[member.userId]:
            sessions[member.userId][ len(sessions[member.userId]) + 1 ] = [[member.datetime, member.keywords, member.semanticTypes]]
        
        elif member.previouskeywords is not None and not sessions[member.userId]:
            # This situation should not happen, but it does (some error in the logs). It means that a session was not created but there were previous keywords.
            #print "ERROR!"
            #print member.userId, member.datetime, member.keywords, "previous ---> ", member.previouskeywords
            sessions[member.userId][1] = [[member.datetime, member.keywords, member.semanticTypes]]

        # There are previous keywords!
        else:
            sessions[member.userId][ len(sessions[member.userId]) ] += [[member.datetime,member.keywords, member.semanticTypes]]

    #for session, date in sessions.iteritems():
    #    print session, date
    return sessions

def calculateQueriesPerSession(data):
    '''
        I am considering all sessions here. An alternative option would be to consider only the sessions with more that X queries. (e.g. X > 3)
    '''
    sessions = createSessions(data)

    numberOfSessions = sum( len(s) for s in sessions.values() )
    queriesPerSession = [ len(q) for session in sessions.values() for q in session.values() ]
    sessionsWithMoreThanOneQuery = len([ 1 for session in sessions.values() for q in session.values() if len(q) > 1 ])
    
    maxId, maxValue = -1, -1
    for userId, session in sessions.iteritems():
        #print userId, session.values()
        m = max( len(subSession) for subSession in session.values() )
        #print " m ----> ", m
        if m > maxValue:
            maxId, maxValue = userId, m
    
    #print "MAXs =",  maxId, maxValue
    idMaxQueriesInSession = maxId

    countingQueriesPerSession = Counter(queriesPerSession)

    allSessions = [ span for session in sessions.values() for span in session.values() ]
    timeSpansInSeconds = [ (max(span[-1][0],span[0][0]) - min(span[-1][0],span[0][0])).total_seconds() for span in allSessions]
    countingTimePerSession = Counter(timeSpansInSeconds)

    # Basic statistics for queries inside sessions
    npNumQueriesInSession = generateStatsVector(queriesPerSession)
    
    # Basic statistics for the time spend in each session (metric used is seconds) 
    npTime = generateStatsVector(timeSpansInSeconds)
   
    #calculate extra metrics for sessions
    numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions,\
            vectorOfModifiedSessions = calculateExpansionShrinkageReformulations(sessions)
    modifiedQueries = numberOfExpansions + numberOfShrinkage + numberOfReformulations + numberOfRepetitions 
   
    # calculate all semantic stuff
    countingSemantics, countingPureSemanticTypes, vectorOfActionSequence, vectorOfCicleSequence, userSemanticType = calculateSemanticTypes(sessions)
    smt = [ s for member in data if member.semanticTypes is not None for s in member.semanticTypes if member.semanticTypes]
    countingFullSemanticTypes = Counter(smt)
    #print countingFullSemanticTypes

    #Calculate the number of re-access to some information in different sessions!i
    countingReAccess = calculateReAccessInDifferentSessions(sessions)
    
    # The number of sessions with more that 2 queries HAVE to be the same that the number of modified session
    #print "SUM = ", sum(vectorOfModifiedSessions), " More than one = ", sessionsWithMoreThanOneQuery, " rep =", numberOfRepetitions
    #print vectorOfModifiedSessions
    ###TODO CHECK code :
    #assert sum(vectorOfModifiedSessions) == sessionsWithMoreThanOneQuery
    
    #print numberOfSessions, npNumQueriesInSession, npTime
    return numberOfSessions, countingQueriesPerSession, npNumQueriesInSession,\
            countingTimePerSession, npTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions,\
            vectorOfModifiedSessions, countingSemantics, countingPureSemanticTypes, vectorOfActionSequence, countingReAccess, idMaxQueriesInSession,\
            vectorOfCicleSequence, countingFullSemanticTypes, userSemanticType


def calculateQueryRanking(data):
    rankings = [member.rank for member in data if member.rank]
    #print rankings
    return Counter(rankings)

def calculateReAccessInDifferentSessions(sessions):
    countingReAccess = defaultdict(int) # { usedId: numberOfReAcess } 
    '''
    Number of users who had a re-access: len(countingReAccess)
    Total number of re-access: sum(countingReAccess.values())
    '''
    
    for userId, session in sessions.iteritems():
        
        uniqueQueries = {}
        pastQueries = set()

        for subSession in session.values():
            queries = set()
            reAccessThisSession = False

            for query in subSession:
                queries.add( tuple(set(query[1])) ) #using set to ignore order
                #print "usedId =>", userId, "Query => ", query[1]

                if reAccessThisSession:
                    continue

                if tuple(set(query[1])) in pastQueries:
                    #print "FOUND RE ACCESS HERE ---> ", query[1]
                    # We want to count the re-access only once per session
                    countingReAccess[userId] += 1
                    reAccessThisSession = True

                #print "set(queries) =  ", queries

            pastQueries.update(queries)
            #print "Qs ---> ", queries
            #print "PastQueries ----> ", pastQueries
    #print "countingReAccess ->> ", countingReAccess
    #print len(countingReAccess)
    #print sum(countingReAccess.values())
    return countingReAccess

def analyzeSequencyOfActions(sequence):
    cause, symptom, remedy = 0,0,0
    hasCause, hasSymptom, hasRemedy = 0,0,0

    for action in sequence:
        if action is "cause":
            cause += 1
            hasCause = 1
        elif action is "symptom":
            symptom += 1
            hasSymptom = 1
        elif action is "remedy":
            remedy += 1
            hasRemedy = 1
    
    index = int( str(hasRemedy) + str(hasCause) + str(hasSymptom), 2) #binary transformation here
    #print "index = ", index, "remedy =", hasRemedy, "cause", hasCause,"symptom", hasSymptom
    return index

def contains(subSequence, sequence):
    startIndex = 0
    found = False

    for j in range(0, len(subSequence)):
        e = subSequence[j]
        for i in range(startIndex, len(sequence)):
            if e == sequence[i]:
                startIndex = i + 1
                found = True
                break
        if not found:
            break
        else:
            found = False

    #Else is executed only and if only the break inside the for is not activeted
    else:
        return True

    return False


def cicleAnalyze(sequence):
    scs = ["symptom", "cause", "symptom"]
    srs = ["symptom", "remedy", "symptom"]
    csc = ["cause", "symptom", "cause"]
    crc = ["cause", "remedy", "cause"]
    rsr = ["remedy", "symptom", "remedy"]
    rcr = ["remedy", "cause", "remedy"]
    
    vectorOfCicleSequence = [0] * 6 # {scs, srs, csc, crc, rsr, rcr}
    
    if contains(scs, sequence):
        vectorOfCicleSequence[0] += 1
    if contains(srs, sequence):
        vectorOfCicleSequence[1] += 1
    if contains(csc, sequence):
        vectorOfCicleSequence[2] += 1
    if contains(crc, sequence):
        vectorOfCicleSequence[3] += 1
    if contains(rsr, sequence):
        vectorOfCicleSequence[4] += 1
    if contains(rcr , sequence):
        vectorOfCicleSequence[5] += 1

    #print "VECTOR ==== ", vectorOfCicleSequence
    return vectorOfCicleSequence

"""
    Input:
        sessions ---> { id: { sessionCounter: [ [Query1], [Q2], [Q3] ], sessionCounter2: [[Q1], [Q2], [Q3]]  }  }
        id -> user identification
        QueryX -> [ datetime, keywords, semanticTypes]
        sessionCounter -> counter starting from 1

    Some important semantic types (list: http://metamap.nlm.nih.gov/SemanticTypeMappings_2011AA.txt)
        -> Symptom   -> sosy (Sign or Symptom)
        
        -> Cause     -> bact (Bacterium), virs (Virus), dsyn (Disease or Syndrome), orgm (? Organism ?)
        
        -> Remedy    -> drdd (Drug Delivery Device), clnd (Clinical Drug), amas (Amino Acid Sequence ?), antb (Antibiotic), aapp(Amino Acid, Peptide, or Protein?), phsu (Pharmacologic Substance), imft (Immunologic Factor - vaccine, e.g.), vita (Vitamin)

        -> where     -> bpoc (Body Part, Organ, or Organ Component), bsoj (Body Space or Junction), tisu (tissue), bdsy (Body System), blor (Body Location or Region)

        ->>> Important and missing classification: inpo (Injury or Poisoning),  diap (Diagnostic Procedure), irda (Indicator, Reagent, or Diagnostic Aid), fndg (Finding), ftcn (Functional Concept), gngm (Gene or Genome), hcro (Health Care Related Organization), hlca (Health Care Activity), horm|Hormone, inch|Inorganic Chemical, lbpr|Laboratory Procedure, mobd|Mental or Behavioral Dysfunction

"""
def calculateSemanticTypes(sessions):

    countingSemantics = { "symptom":0, "cause": 0, "remedy": 0, "where": 0 }
    countingPureSemanticTypes = defaultdict(int)
    vectorOfActionSequence = [0] * 8 # [ 2^{remedy,cause,symptom} in this order ] 
    vectorOfCicleSequence = [0] * 6 # {scs, srs, csc, crc, rsr, rcr}
    userSemantic = {}
    
    for (user, session) in sessions.iteritems():
        semanticByUser = list()

        for subSession in session.values():
            #print subSession
            
            actionSequence = []
            for query in subSession:
                if query[2] is not None:
                    #print "Semantic Type => ", query[2]
                    
                    for st in query[2]:
                        countingPureSemanticTypes[st] += 1
                        
                        if st in symptomTypes():
                            actionSequence.append("symptom")
                            countingSemantics["symptom"] += 1
                            semanticByUser.append("symptom")
                        
                        elif st in causeTypes():
                            actionSequence.append("cause")
                            countingSemantics["cause"] += 1
                            semanticByUser.append("cause")
                        
                        elif st in remedyTypes():
                            actionSequence.append("remedy")
                            countingSemantics["remedy"] += 1
                            semanticByUser.append("remedy")
                        
                        elif st in whereTypes():
                            actionSequence.append("where")
                            countingSemantics["where"] += 1
                            semanticByUser.append("where")

                        elif st in noMedicalTypes():
                            semanticByUser.append("noMedical")
            
            #analyse the sequence of symptom followed by causes, etc.
            index = analyzeSequencyOfActions(actionSequence)
            cicleVector = cicleAnalyze(actionSequence)

            vectorOfCicleSequence = [ al + bl for al, bl in zip(cicleVector,vectorOfCicleSequence) ]

            #print "INDEX = ", index
            vectorOfActionSequence[index] += 1
        
        userSemantic[user] = semanticByUser

    #print countingSemantics
    #print countingPureSemanticTypes
    #print "Vector of Action Sequence ", vectorOfActionSequence
    #print userSemantic
    return countingSemantics, countingPureSemanticTypes, vectorOfActionSequence, vectorOfCicleSequence, userSemantic

def countBooleanTerms(listOfQueries):

    booleanTerms = {'or':0, 'and':0, 'not':0, 'any':0}
    operators = ['or', 'and', 'not']
    
    for query in listOfQueries:
        anybool = False
        for op in operators:
            if op in query:
                booleanTerms[op] += 1
                anybool = True
        if anybool:
            booleanTerms['any'] += 1
    return booleanTerms            
        
def calculateTerms(data, coOccurrenceThreshold=0.6):
    """
        Calculate Max, Min, Mean, Median of terms along all the queries
        Also count the occurrences of each term and the co-occurrence of terms.
        The coOccurrenceThreshold is a parameter that indicates the minimal number of times that 
        term X has to appears together with term Y among all the apparences of term X or Y.
    """
   
    # I had to transforme the list into a tuple to use the counter
    countingQueries = Counter( [ tuple(sorted(member.keywords)) for member in data ] )

    # separate the information about the queries from the rest of the data
    listOfQueries = [ member.keywords for member in data ]
    
    # Count the number of keywords used in each single query
    queryInNumbers = [ len( query ) for query in listOfQueries]

    indexGreatestQuery, _ = max(enumerate(queryInNumbers), key=operator.itemgetter(1))
    greatestQuery = listOfQueries[indexGreatestQuery]

    #print queryInNumbers
    #print greatestQuery, len(greatestQuery)
    booleanTerms = countBooleanTerms(listOfQueries)

    # Transform the query into a list of simple tokens and count them
    tokens = [ t.lower() for sublist in listOfQueries for t in sublist]
    countingTokens = Counter(tokens)
    
    tenMostCommonTermsNoStopWord = simpleFilterStopWords(countingTokens) 

    # Calculate the Co-occurrence matrix
    matrix = {}
    for queryComplete in listOfQueries:
        #print "Q = ", query
        ## Remove duplicates from a query
        query = list(set(queryComplete))

        for i in range(len(query) - 1):
            first = query[i].lower()
            
            for j in range(i + 1, len(query)):
                second = query[j].lower()
                #print "first ==> ", first, "second ==> ", second
                d1, d2 = min(first,second), max(first,second)

                if d1 not in matrix:
                    matrix[d1] = defaultdict(int)
                if d2 not in matrix[d1]:
                    matrix[d1][d2] = 0

                matrix[d1][d2] += 1
                #print "matrix[",d1,"][",d2,"] = ", matrix[d1][d2]

    # Filter the results using the parameter coOccurrenceThreshold and generate the coOccurrenceList
    numberOfQueries = len(listOfQueries)
    coOccurrenceList = []
    simpleCoOccurrenceList = []

    for d1 in matrix:
        for d2 in matrix[d1]:
            #print d1, d2, matrix[d1][d2], countingTokens[d1], countingTokens[d2]
            if matrix[d1][d2] / countingTokens[d1] >= coOccurrenceThreshold or\
               matrix[d1][d2] / countingTokens[d2] >= coOccurrenceThreshold:
                #print d1, d2, matrix[d1][d2]
                coOccurrenceList.append( [d1, d2, matrix[d1][d2], matrix[d1][d2]/numberOfQueries, matrix[d1][d2]/countingTokens[d1], matrix[d1][d2]/countingTokens[d2]] )
            simpleCoOccurrenceList.append( [d1, d2, matrix[d1][d2], matrix[d1][d2]/numberOfQueries, matrix[d1][d2]/countingTokens[d1], matrix[d1][d2]/countingTokens[d2]] )

    # Calculate basic metrics
    npTerms = generateStatsVector(queryInNumbers)
    
    return npTerms, booleanTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, greatestQuery, countingQueries, tenMostCommonTermsNoStopWord


def calculateQueriesPerUser(data):
    
    #from datetime import datetime
    from itertools import groupby
    #print "START!"
    #start = datetime.now()

    userIds = sorted( [member.userId for member in data] )
    countingQueriesPerUser = Counter([len(list(g)) for k, g in groupby(userIds)])
    
    #end = datetime.now()
    #print "Total Seconds to calculate queries per user: ", (end-start).total_seconds()

    #print countingQueriesPerUser
    return countingQueriesPerUser

def printGeneralMetrics(writer, numberOfUsers, numberOfQueries, numberOfSessions, firstDay, lastDay):
    writer.write("-" * 80 + "\n")
    writer.write("-" * 45 + "\n")
    writer.write("General Information:\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Unique Users", str(numberOfUsers)))
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Queries", str(numberOfQueries)))
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Sessions", str(numberOfSessions)))
    writer.write('{0:45} ==> {1:30}\n'.format("First date in logs", str(firstDay)))
    writer.write('{0:45} ==> {1:30}\n'.format("Last date in logs", str(lastDay)))
    writer.write('{0:45} ==> {1:30}\n'.format("How may days? ", str((lastDay - firstDay).days)))
    writer.write("-" * 45 + "\n")
 
def printMetricsForTerms(writer, npTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, percentageAcronymInQueries, countingAcronyms, countingNL, numberOfUsers, tenMostCommonTermsNoStopWord, numberOfQueries):
    
    writer.write("For TERMS:\n")
    writer.write("-" * 45 + "\n")
   
    writer.write('{0:45} ==> {1:30}\n'.format("Number Of Unique Terms (Types) ", str(len(countingTokens))))
    writer.write('{0:45} ==> {1:30}\n'.format("Number Total Of Terms", str( sum(countingTokens.values()))))
    
    writer.write('{0:45} ==> {1:.3f}\n'.format('Relation Type/Terms', ( sum(countingTokens.values()) / len(countingTokens))))

    writer.write('{0:45} ==> {1:.3f}\n'.format('Max. number of Terms in a query', (npTerms.max)))
    writer.write('{0:45} ==> {1:.3f}\n'.format('Min. number of Terms in a query', (npTerms.min)))
    writer.write('{0:45} ==> {1:.3f}\n'.format('Mean number of Terms in a query', (npTerms.mean)))
    writer.write('{0:45} ==> {1:.3f}\n'.format('Median number of Terms in a query', (npTerms.median)))
    writer.write('{0:45} ==> {1:.3f}\n'.format('Std Deviation of Terms in a query', (npTerms.std)))
    
    writer.write('{0:45} ==> {1:.3f}\n'.format('Percentage of Acronyms in queries', (percentageAcronymInQueries)))
    
    writer.write("-" * 45 + "\n")
    writer.write("15 Most Common Terms:\n")
    
    totalTokens = sum(countingTokens.values())
    writer.write("-" * 45 + "\n")
    writer.write('Token ==> Freq --- Freq/numTokens ------- Freq/numQueries\n')
    for pair in countingTokens.most_common(15):
        writer.write('{0:45} ==> {1:d} --- {2:.3f} ------- {3:.3f}\n'.format(pair[0], pair[1], 100.0*pair[1]/totalTokens, 100.0*pair[1]/numberOfQueries))
    writer.write("-" * 45 + "\n")
     
    writer.write("15 Most Common Terms: (not stop words)\n")
    writer.write('Token ==> Freq --- Freq/numTokens ------- Freq/numQueries\n')
    for (word, freq) in tenMostCommonTermsNoStopWord:
        writer.write('{0:45} ==> {1:d} --- {2:.3f} ------- {3:.3f}\n'.format(word, int(freq), 100.0 * freq / totalTokens, 100.0*freq/numberOfQueries))
    writer.write("-" * 45 + "\n")

    writer.write("50 Most Common Acronyms:\n")
    writer.write('Token ==> Freq --- Freq/numAcronyms ------- Freq/numQueries\n')
    writer.write("-" * 45 + "\n")
    for pair in countingAcronyms.most_common(50): 
        writer.write('{0:45} ==> {1:30} --- {2:.3f} ------- {3:.3f}\n'.format(pair[0], str(pair[1]), 100.0 * pair[1] / numberOfAcronyms, 100.0 * pair[1]/numberOfQueries ))
    writer.write( "-" * 45 + "\n")

    writer.write("Co-ocorrence pairs: \n")
    writer.write('{0:30} | {1:30} | {2:4} | {3:4} | {4:7} | {5:7}\n'.format("Word1","Word2","Freq","%Freq.","W1W2","W2W1"))
    #writer.write("Word1\tWord2\t\t\tTimes together\tSupport W1W2\tConfidence W1->W2\t Confidence W2->W1" + "\n")
    coOccurrenceList = sorted(coOccurrenceList, key=operator.itemgetter(3),reverse=True)
    for nestedList in coOccurrenceList[:50]:
        writer.write('{0:30} | {1:30} | {2:4d} | {3:.4f} | {4:.5f} | {5:.5f}\n'.format(nestedList[0],nestedList[1],nestedList[2],nestedList[3],nestedList[4],nestedList[5]))
        #writer.write( nestedList[0], '\t',  nestedList[1], '\t\t\t' , nestedList[2], '\t', nestedList[3], '\t', nestedList[4], '\t', nestedList[5]

    writer.write("-" * 45 + "\n")
    writer.write("-" * 45 + "\n")
    writer.write("Simple Co-ocorrence pairs: \n")
    writer.write('{0:30} | {1:30} | {2:4} | {3:4} | {4:7} | {5:7}\n'.format("Word1","Word2","Freq","%Freq.","W1W2","W2W1"))
    simpleCoOccurrenceList = sorted(simpleCoOccurrenceList, key=operator.itemgetter(3),reverse=True)
    for nestedList in simpleCoOccurrenceList[:50]:
        writer.write('{0:30} | {1:30} | {2:4d} | {3:.4f} | {4:.5f} | {5:.5f}\n'.format(nestedList[0],nestedList[1],nestedList[2],nestedList[3],nestedList[4],nestedList[5]))

    writer.write("-" * 45 + "\n")
    writer.write("-" * 45 + "\n")
    writer.write('{0:45} ==> {1:d}, {2:.2f}(%)\n'.format("Number of users using NL:", len(countingNL), 100*len(countingNL)/numberOfUsers))
    writer.write('{0:45} ==> {1:d}, {2:.2f}(%)\n'.format("Total number of NL in queries:", sum(countingNL.values()), 100 * sum(countingNL.values()) / numberOfQueries))    
    writer.write("-" * 45 + "\n")
    writer.write("-" * 80 + "\n")


def printMetricsForQueries(writer, greatestQuery, countingQueries, countingQueriesPerDay, meanQueriesPerDay):

    writer.write("-" * 80 + "\n")
    writer.write("-" * 45 + "\n")
    writer.write("For QUERIES:\n")
    writer.write("-" * 45 + "\n")

    uniqueQueries = len(countingQueries)
    allQueries = sum(countingQueries.values())
    writer.write('{0:45} ==> {1:d}\n'.format('Total Number of Unique Queries', uniqueQueries))
    writer.write('{0:45} ==> {1:d}\n'.format('Total Number of Queries', allQueries))
    writer.write('{0:45} ==> {1:.3f} %\n'.format('Percentage Of Repeated queries ', 100 * (allQueries - uniqueQueries)/allQueries ))
    writer.write('{0:45} ==> {1:30}\n'.format('Greatest Query', ' '.join(greatestQuery)))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Mean number of Queries per day", meanQueriesPerDay))
    
    writer.write("-" * 45 + "\n")
    writer.write("15 Most Common Queries:\n")
    writer.write("-" * 45 + "\n")
    for pair in countingQueries.most_common(15):
        writer.write('{0:45} ==> {1:d}\n'.format(pair[0], pair[1]))
    
    writer.write("-" * 45 + "\n")   
    writer.write("Queries by size:\n")
    writer.write("-" * 45 + "\n")
    querySizes = Counter( ( len(q) for q in countingQueries.elements()) )
    writer.write('Size ==> Qt ==> %\n')
    for q,c in querySizes.iteritems():
        writer.write('{0:d} ==> {1:d} ==> {2:.3f}\n'.format(q,c,100.0*c/allQueries))
    writer.write("-" * 45 + "\n")   
    writer.write("-" * 80 + "\n")
    

def printMetricsForSessions(writer, numberOfSessions, numberOfQueries, npNumQueriesInSession, npTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions, countingSessionsPerDay, meanSessionsPerDay, countingReAccess, numberOfUsers, idMaxQueriesInSession):

    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("For SESSIONS:\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Sessions", str(numberOfSessions)))
    writer.write("-" * 40 + "\n")
    writer.write("Session Length in Queries\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:.3f} (id = {2:s})\n'.format("Maximum number of Queries in a session", (npNumQueriesInSession.max), idMaxQueriesInSession))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Minimum number of Queries in a session", (npNumQueriesInSession.min)))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Mean number of Queries in a session", (npNumQueriesInSession.mean)))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Median number of Queries in a session", (npNumQueriesInSession.median)))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Std dev of the number of Queries in a session", (npNumQueriesInSession.std)))
    writer.write("-" * 40 + "\n")
    writer.write("Session Length in Time\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:.3f}\n'.format("Maximum duration of a session", npTime.max))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Minimum duration of a session", npTime.min))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Mean duration of a session", npTime.mean))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Median duration of a session", npTime.median))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Std dev. of duration of a session", npTime.std))
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Vector Of Modified Session ", str(vectorOfModifiedSessions)))
    #["Nothing","Expansion","Shrinkage","Reformulation","ExpansionShrinkage","ExpansionReformulation","ShrinkageReformulation","ExpansionShrinkageReformulation"]
    #[vectorOfModifiedSessions[0], vectorOfModifiedSessions[4], vectorOfModifiedSessions[2], vectorOfModifiedSessions[1], vectorOfModifiedSessions[6], vectorOfModifiedSessions[5], vectorOfModifiedSessions[3], vectorOfModifiedSessions[7]
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Expansions", vectorOfModifiedSessions[4], 100.0 * vectorOfModifiedSessions[4]/numberOfSessions))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Shrinkages", vectorOfModifiedSessions[2], 100.0 * vectorOfModifiedSessions[2]/numberOfSessions))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Reformulations", vectorOfModifiedSessions[1], 100.0 * vectorOfModifiedSessions[1]/numberOfSessions))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("ExpansionsShrinkages", vectorOfModifiedSessions[6], 100.0 * vectorOfModifiedSessions[6]/numberOfSessions))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("ExpansionsReformulations", vectorOfModifiedSessions[5], 100.0 * vectorOfModifiedSessions[5]/numberOfSessions))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("ShrinkagesReformulations", vectorOfModifiedSessions[3], 100.0 * vectorOfModifiedSessions[3]/numberOfSessions))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("ExpansionsShrinkagesReformulations", vectorOfModifiedSessions[7], 100.0 * vectorOfModifiedSessions[7]/numberOfSessions))
    writer.write("-" * 40 + "\n")
    writer.write("-" * 40 + "\n")


    totalOfModifiedSessions = sum(vectorOfModifiedSessions)
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Number of Modified Session ", totalOfModifiedSessions, 100.0 * totalOfModifiedSessions/numberOfSessions))
    modifiedQueries = (numberOfExpansions + numberOfShrinkage + numberOfReformulations + numberOfRepetitions)
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Number of Modified Queries", modifiedQueries, 100.0 * modifiedQueries/numberOfQueries))
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Number of Expansions", numberOfExpansions, 100.0 * numberOfExpansions/numberOfQueries))    
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Number of Shrinkages", numberOfShrinkage, 100.0 * numberOfShrinkage/numberOfQueries))    
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Number of Reformulations", numberOfReformulations, 100.0 * numberOfReformulations/numberOfQueries))    
    writer.write('{0:45} ==> {1:10d} ({2:.3f}%)\n'.format("Number of Repetitions", numberOfRepetitions, 100.0 * numberOfRepetitions/numberOfQueries))    
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:.3f}\n'.format("Mean Number of Sessions Per Day", meanSessionsPerDay))    
    writer.write("-" * 40 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:d}, {2:.2f}(%)\n'.format("Number of users re-accessing information:", len(countingReAccess), 100*len(countingReAccess)/numberOfUsers))
    writer.write('{0:45} ==> {1:d}, {2:.2f}(%)\n'.format("Total number of re-access inter sessions:", sum(countingReAccess.values()), 100.0*sum(countingReAccess.values())/numberOfSessions))    
    writer.write("-" * 80 + "\n")

def printMeshClassificationMetrics(writer, countingMesh, countingDisease, numberOfQueries, hasMeshValues, countingMeshDepth):
    
    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("MESH CLASSIFICATION:\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:10d}\n'.format("Number of Queries with mesh identifiers", int(hasMeshValues)))
    writer.write('{0:45} ==> {1:.3f}\n'.format("HasMeshValues / #Queries ", hasMeshValues/numberOfQueries))
    writer.write("-" * 40 + "\n")
    
    totalMesh = sum (countingMesh.values() )
    writer.write('{0:45} ==> {1:10d}\n'.format("Number of Mesh identifiers", totalMesh ))
    writer.write('{0:45} ==> {1:.3f}\n'.format("(Mean) Mesh Identifies / #Queries ", totalMesh/numberOfQueries))
    
    writer.write("-" * 40 + "\n")
    for k,v in countingMesh.iteritems():
        writer.write('{0:>15} ------- {1:10d} ({2:.2f}%)\n'.format( k, v, 100 * v/totalMesh ))

    writer.write("-" * 40 + "\n")
    totalDisease = sum(countingDisease.values() )
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Disesase identifiers", totalDisease ) )
    writer.write('{0:45} ==> {1:.3f}\n'.format("(Mean) Diseases / #Queries ", totalDisease/numberOfQueries))
    writer.write("-" * 40 + "\n")
    for k,v in countingDisease.iteritems():
        writer.write('{0:>15} ------- {1:<10} ({2:.2f}%)\n'.format( k, v, 100 * v/totalDisease ))
    
    writer.write("-" * 40 + "\n")
    writer.write("-" * 40 + "\n")
    
    writer.write("MESH DEPTH:\n")
    writer.write('{0:>15} ------- {1:<10} ({2:>3}) )\n'.format( "Depth","Frequency","%"))
    totalMeshDepth = sum(countingMeshDepth.values() )
    for k,v in countingMeshDepth.iteritems():
        writer.write('{0:>15} ------- {1:<10} ({2:.2f}%)\n'.format( k, v, 100 * v/totalMeshDepth))
    writer.write("-" * 40 + "\n")
    writer.write("-" * 80 + "\n")

def printSemantic(writer, vectorOfActionSequence, vectorOfCicleSequence, countingFullSemanticTypes, numberOfQueries):

    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("ACTIONS FOCUS:\n")
    writer.write("-" * 40 + "\n")
    totalActions = sum(vectorOfActionSequence)
    writer.write('{0:45} ==> {1:30}\n'.format("Total number of actions (1 per session)", totalActions ))
    
    #["Dtst", "Nothing", "Symptom", "Cause", "Remedy", "SymptomCause", "SymptomRemedy", "CauseRemedy", "SymptomCauseRemedy"]
    #semanticFocusRow.append( [ dataName, vectorOfActionSequence[0], vectorOfActionSequence[1], vectorOfActionSequence[2], vectorOfActionSequence[4], vectorOfActionSequence[3], vectorOfActionSequence[5], vectorOfActionSequence[6], vectorOfActionSequence[7] ] )
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("Nothing", vectorOfActionSequence[0], 100 * vectorOfActionSequence[0]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("Symptom",vectorOfActionSequence[1], 100 * vectorOfActionSequence[1]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("Cause", vectorOfActionSequence[2], 100 * vectorOfActionSequence[2]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("Remedy", vectorOfActionSequence[4], 100 * vectorOfActionSequence[4]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("SymptomCause", vectorOfActionSequence[3], 100 * vectorOfActionSequence[3]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("SymptomRemedy", vectorOfActionSequence[5], 100 * vectorOfActionSequence[5]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("CauseRemedy", vectorOfActionSequence[6], 100 * vectorOfActionSequence[6]/totalActions))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("SymptomCauseRemedy", vectorOfActionSequence[7], 100 * vectorOfActionSequence[7]/totalActions))
    writer.write("-" * 40 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("CICLE SEQUENCE:\n")
    writer.write("-" * 40 + "\n")
    totalCicleSequence = sum(vectorOfCicleSequence)
    writer.write('{0:45} ==> {1:30}\n'.format("Total of cicle sequencies found", totalCicleSequence))
    ### {scs, srs, csc, crc, rsr, rcr}
    totalCicleSequence = 1e1000 if totalCicleSequence == 0 else totalCicleSequence
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("SCS", vectorOfCicleSequence[0], 100 * vectorOfCicleSequence[0]/totalCicleSequence))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("SRS", vectorOfCicleSequence[1], 100 * vectorOfCicleSequence[1]/totalCicleSequence))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("CSC", vectorOfCicleSequence[2], 100 * vectorOfCicleSequence[2]/totalCicleSequence))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("CRC", vectorOfCicleSequence[3], 100 * vectorOfCicleSequence[3]/totalCicleSequence))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("RSR", vectorOfCicleSequence[4], 100 * vectorOfCicleSequence[4]/totalCicleSequence))
    writer.write('{0:45} ==> {1:8d} ({2:.2f}%)\n'.format("RCR", vectorOfCicleSequence[5], 100 * vectorOfCicleSequence[5]/totalCicleSequence))
    writer.write("-" * 40 + "\n") 
    writer.write("FULL SEMANTIC TYPES IN ORDER:\n")
    writer.write('Type ==> Freq --- Freq/numSemantic ------- Freq/numQueries\n')
    writer.write("-" * 40 + "\n")
    allSemanticTypes = sum(countingFullSemanticTypes.values())
    for pair in countingFullSemanticTypes.most_common():
        writer.write('{0:45} ==> {1:30} --- {2:.3f}% ------- {3:.3f}%\n'.format(pair[0], str(pair[1]),100.0 * pair[1]/allSemanticTypes, 100.0 * pair[1]/numberOfQueries ))
    writer.write("-" * 40 + "\n")
    writer.write("-" * 80 + "\n")


def printOutliers(writer, outliersToRemove):
    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("OUTLIERS:\n")
    if removeOutliers:
        writer.write("--------- THEY WERE REMOVED ------------\n")

    writer.write('{0:45} ==> {1:30}\n'.format("Total of outliers found", len(outliersToRemove)))
    for id in outliersToRemove:
        writer.write('{0:45} ==> {1:30}\n'.format("ID", id))
    writer.write("-" * 40 + "\n")
    writer.write("-" * 80 + "\n")


