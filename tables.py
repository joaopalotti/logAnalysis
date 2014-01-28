from __future__ import division

#All the chaos goes here
tableGeneralHeader = [["Dtst", "#Days", "#Users", "#Qrs", "uniqueQrs", "mnWrdsPQry", "stdmnWrdsPQry", "medianWrdsPQry", "mnCharsPQry", "stdCharsPQey", "medianCharsPQry", "mnQrsPDay", "Sssions", "mnQrsPrSsion", "stdQrsPrSssion", "medianQrsPrSssion", "mTimePrSsion", "stdTimePrSssion", "medianTimePrSssion", "Users #NL", "Users %NL", "QueriesNL", "%QueriesNL", "%QsReACcess", "%UsersReAccess", "%SssnsReAccess", "QueriesAcronym", "%QAcronym", "UsersAcronym", "%UsersAcronym", "UsersSemantics", "%UserSemantics","Concepts/Queries", "Sources/Queries"]]

tableGeneralMeshHeader = [["Dtst", "QrsWithMesh", "% QrsWithMesh", "MeshIds", "MeshIds/#Qrs", "DiseIds", "DiseIds/#Qrs","#UsersUsingMesh","#UsersUsingMesh/#Users", "MeanUserMeshDepth"]]
tableMeshHeader = [ ["Dtst(%)","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
tableWeightedMeshHeader = [ ["Dtst(%)","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
tableDiseasesHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]
tableWeightedDiseasesHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]

tableSemanticFocusHeader = [ ["Dtst", "Nothing", "Symptom", "Cause", "Remedy", "SymptomCause", "SymptomRemedy", "CauseRemedy", "SymptomCauseRemedy"] ]
tableCicleSequenceHeader = [["Dtst", "Gross", "Perc", "SCS", "SRS", "CSC", "CRC", "RSR", "RCR"]] 

tableModifiedSessionHeader = [["Dtst","Nothing","Expansion","Shrinkage","Reformulation","ExpansionShrinkage","ExpansionReformulation","ShrinkageReformulation","ExpansionShrinkageReformulation"]] 
tableGeneralModifiedHeader = [["Dtst", "Exp", "Exp(%)", "Shr", "Shr(%)", "Ref", "Ref(%)", "Rep", "Rep(%)" ]]
tableMeshDepthHeader = [["Dtst(%)", "Depth 1", "Depth 2", "Depth 3", "Depth 4", "Depth 5", "Depth 6", "Depth 7", "Depth 8", "Depth 9", "Depth 10","Depth 11", "Depth 12"]]
tableSemanticByUserHeader = [["Dtst", "Symptom", "Symptom (%)", "Cause", "Cause (%)", "Remedy", "Remedy (%)", "Where", "Where (%)", "noMedical", "noMedical (%)"]] 
tableSemanticByUserWeightedHeader = [["Dtst", "Symptom", "Symptom (%)", "Cause", "Cause (%)", "Remedy", "Remedy (%)", "Where", "Where (%)", "noMedical", "noMedical (%)"]] 
tableMeshByUserHeader = [ ["Dtst","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
tableMeshWeightedByUserHeader = [ ["Dtst","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
tableDiseaseByUserHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]
tableDiseaseWeightedByUserHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]
tableMeshByUserWeightedHeader = [ ["Dtst","A (Anatomy)","B (Organisms)","C (Diseases)","D (Chemicals/Drugs)","E (Analytical, Diagnostic)","F(Psychiatry/Psychology)","G(Phenomena/Processes)","H(Disciplines/Occupations)","I(Anthropology/Education)","J(Technology/Industry)","K(Humanities)","L(Information Science)","M(Named Groups)","N(Health Care)","V(Publication Chars)","Z(Geographicals)"] ]
tableDiseaseByUserWeightedHeader = [ ["Dtst(%)","C01(Bacterial)","C02(Viral)","C03(Parasitic)","C04(Neoplasms)","C05(Musculoskeletal)","C06(Digestive)","C07(Stomatognathic)","C08(Respiratory)","C09(Otorhinolaryngologic)","C10(Nervous)","C11(Eye)","C12(Male Urogenital)","C13(Female Urogenital)","C14(Cardiovascular)","C15(Hemic and Lymphatic)","C16(Congenital)","C17(Skin)","C18(Nutritional)","C19(Endocrine)","C20(Immune)","C21(Environmental)","C22(Animal)","C23(Pathological Conditions)","C24(Occupational)","C25(Substance-Related)","C26(Wounds and Injuries)"] ]
tableBooleanUseHeader = [["Dtst", "# of ands", "% of ands", "# of ors", "% of ors",  "# of nots", "% of nots", "at least one", "% of booleans", "% UsersUsingBools" ]]
tableCHVHeader = [["Dtst", "CHVFound", "CHVId/query", "UMLSId/query", "CHVMisspelled/query", "MeanComboScore","0pComboS.","25pComboS.","50pComboS.","75pComboS.","100pComboS."]]
tablePOSHeader = [["Dtst", "Total/#Queries", "noun", "adj", "prep", "conj", "aux", "det", "pron", "verb", "punc", "shape", "adv"]]

generalTableRow, generalMeshRow, meshTableRow, diseaseTableRow, meshTableWeightedRow, diseaseTableWeightedRow = [], [], [], [], [], []
semanticFocusRow, cicleSequenceRow, generalModifiedRow, modifiedSessionRow, meshDepthRow, semanticByUserRow = [], [], [], [], [], []
semanticByUserWeightedRow, meshByUserRow, diseaseByUserRow, meshByUserWeightedRow, diseaseByUserWeightedRow, booleanUseRow = [], [], [], [], [], []
CHVRow, postagsRow  = [], []

#def append(table, args**):
def appendGeneral(dataName, lastDay, firstDay, numberOfUsers, numberOfQueries, npTerms, npChars, meanQueriesPerDay, numberOfSessions, npNumQueriesInSession, npTime, countingNL, countingReAccess, hasAcronym, percentageAcronymInQueries, usersUsingAcronyms, setOfUsersWithSemantic, uniqueQueries, numberOfConcepts, numberOfSources):
    generalTableRow.append( [ dataName, (lastDay - firstDay).days, numberOfUsers, numberOfQueries, uniqueQueries, npTerms.mean, npTerms.std, npTerms.median, npChars.mean, npChars.std, npChars.median, meanQueriesPerDay, numberOfSessions, npNumQueriesInSession.mean, npNumQueriesInSession.std, npNumQueriesInSession.median, npTime.mean, npTime.std, npTime.median, len(countingNL), 100*len(countingNL)/numberOfUsers, sum(countingNL.values()), 100 * sum(countingNL.values())/numberOfQueries, 100*(numberOfQueries - uniqueQueries)/numberOfQueries, 100*len(countingReAccess)/numberOfUsers, 100*sum(countingReAccess.values())/numberOfSessions, len(hasAcronym), percentageAcronymInQueries, len(usersUsingAcronyms), 100.0 * len(usersUsingAcronyms) / numberOfUsers, len(setOfUsersWithSemantic), 100.0 * len(setOfUsersWithSemantic) / numberOfUsers, numberOfConcepts/numberOfQueries,  numberOfSources/ numberOfQueries ] )
        
def appendGeneralModified(dataName, numberOfQueries, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions):
    generalModifiedRow.append( [dataName, numberOfExpansions, 100.0 * numberOfExpansions/ numberOfQueries , numberOfShrinkage, 100 * numberOfShrinkage/ numberOfQueries, numberOfReformulations, 100 * numberOfReformulations/numberOfQueries, numberOfRepetitions, 100 * numberOfRepetitions/numberOfQueries] )


def appendGeneralMesh(dataName, hasMeshValues, numberOfQueries, numberOfMeshTerms, numberOfMeshDiseases, usersUsingMesh, numberOfUsers, mapUserMeanMeshDepth):
    generalMeshRow.append( [dataName,  hasMeshValues, 100.0 * hasMeshValues/numberOfQueries, numberOfMeshTerms, numberOfMeshTerms/numberOfQueries, numberOfMeshDiseases, numberOfMeshDiseases/numberOfQueries, len(usersUsingMesh), 100.0*len(usersUsingMesh)/numberOfUsers, sum(mapUserMeanMeshDepth.values())/len(mapUserMeanMeshDepth.items()) ] ) 

def appendMesh(dataName, countingMesh, numberOfMeshTerms):
    meshTableRow.append( [ dataName, 100 * countingMesh["A"]/ numberOfMeshTerms, 100 * countingMesh["B"]/ numberOfMeshTerms, 100 * countingMesh["C"]/ numberOfMeshTerms, 100 * countingMesh["D"]/ numberOfMeshTerms, 100 * countingMesh["E"]/ numberOfMeshTerms, 100 * countingMesh["F"]/ numberOfMeshTerms, 100 * countingMesh["G"]/ numberOfMeshTerms, 100 * countingMesh["H"]/ numberOfMeshTerms, 100 * countingMesh["I"]/ numberOfMeshTerms, 100 * countingMesh["J"]/ numberOfMeshTerms, 100 * countingMesh["K"]/ numberOfMeshTerms, 100 * countingMesh["L"]/ numberOfMeshTerms, 100 * countingMesh["M"]/ numberOfMeshTerms, 100 * countingMesh["N"]/ numberOfMeshTerms, 100 * countingMesh["V"]/ numberOfMeshTerms, 100 * countingMesh["Z"]/ numberOfMeshTerms  ] )

def appendDisease(dataName, countingDisease, numberOfMeshDiseases):
    diseaseTableRow.append( [ dataName,  100 * countingDisease["C01"]/ numberOfMeshDiseases, 100 * countingDisease["C02"]/ numberOfMeshDiseases, 100 * countingDisease["C03"]/ numberOfMeshDiseases, 100 * countingDisease["C04"]/ numberOfMeshDiseases, 100 * countingDisease["C05"]/ numberOfMeshDiseases, 100 * countingDisease["C06"]/ numberOfMeshDiseases, 100 * countingDisease["C07"]/ numberOfMeshDiseases, 100 * countingDisease["C08"]/ numberOfMeshDiseases, 100 * countingDisease["C09"]/ numberOfMeshDiseases, 100 * countingDisease["C10"]/ numberOfMeshDiseases, 100 * countingDisease["C11"]/ numberOfMeshDiseases, 100 * countingDisease["C12"]/ numberOfMeshDiseases, 100 * countingDisease["C13"]/ numberOfMeshDiseases, 100 * countingDisease["C14"]/ numberOfMeshDiseases, 100 * countingDisease["C15"]/ numberOfMeshDiseases, 100 * countingDisease["C16"]/ numberOfMeshDiseases, 100 * countingDisease["C17"]/ numberOfMeshDiseases, 100 * countingDisease["C18"]/ numberOfMeshDiseases, 100 * countingDisease["C19"]/ numberOfMeshDiseases, 100 * countingDisease["C20"]/ numberOfMeshDiseases, 100 * countingDisease["C21"]/ numberOfMeshDiseases, 100 * countingDisease["C22"]/ numberOfMeshDiseases, 100 * countingDisease["C23"]/ numberOfMeshDiseases, 100 * countingDisease["C24"]/ numberOfMeshDiseases, 100 * countingDisease["C25"]/ numberOfMeshDiseases, 100 * countingDisease["C26"]/ numberOfMeshDiseases ] )

def appendMeshWeighted(dataName, countingMeshWeighted, numberOfMeshWeightedTerms):
    meshTableWeightedRow.append( [ dataName, 100 * countingMeshWeighted["A"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["B"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["C"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["D"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["E"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["F"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["G"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["H"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["I"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["J"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["K"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["L"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["M"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["N"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["V"]/ numberOfMeshWeightedTerms, 100 * countingMeshWeighted["Z"]/ numberOfMeshWeightedTerms  ] )

def appendDiseaseWeighted( dataName, countingDiseaseWeighted, numberOfMeshWeightedDiseases):
    diseaseTableWeightedRow.append( [ dataName,  100 * countingDiseaseWeighted["C01"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C02"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C03"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C04"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C05"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C06"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C07"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C08"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C09"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C10"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C11"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C12"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C13"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C14"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C15"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C16"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C17"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C18"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C19"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C20"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C21"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C22"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C23"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C24"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C25"]/ numberOfMeshWeightedDiseases, 100 * countingDiseaseWeighted["C26"]/ numberOfMeshWeightedDiseases ] )

def appendMeshByUser(dataName, countingMeshByUser, numberOfUsers):
    meshByUserRow.append( [ dataName, 100 * countingMeshByUser["A"]/ numberOfUsers, 100 * countingMeshByUser["B"]/ numberOfUsers, 100 * countingMeshByUser["C"]/ numberOfUsers, 100 * countingMeshByUser["D"]/ numberOfUsers, 100 * countingMeshByUser["E"]/ numberOfUsers, 100 * countingMeshByUser["F"]/ numberOfUsers, 100 * countingMeshByUser["G"]/ numberOfUsers, 100 * countingMeshByUser["H"]/ numberOfUsers, 100 * countingMeshByUser["I"]/ numberOfUsers, 100 * countingMeshByUser["J"]/ numberOfUsers, 100 * countingMeshByUser["K"]/ numberOfUsers, 100 * countingMeshByUser["L"]/ numberOfUsers, 100 * countingMeshByUser["M"]/ numberOfUsers, 100 * countingMeshByUser["N"]/ numberOfUsers, 100 * countingMeshByUser["V"]/ numberOfUsers, 100 * countingMeshByUser["Z"]/ numberOfUsers  ] )

def appendDiseaseByUser(dataName, countingDiseaseByUser, numberOfUsers):
    diseaseByUserRow.append( [ dataName,  100 * countingDiseaseByUser["C01"]/ numberOfUsers, 100 * countingDiseaseByUser["C02"]/ numberOfUsers, 100 * countingDiseaseByUser["C03"]/ numberOfUsers, 100 * countingDiseaseByUser["C04"]/ numberOfUsers, 100 * countingDiseaseByUser["C05"]/ numberOfUsers, 100 * countingDiseaseByUser["C06"]/ numberOfUsers, 100 * countingDiseaseByUser["C07"]/ numberOfUsers, 100 * countingDiseaseByUser["C08"]/ numberOfUsers, 100 * countingDiseaseByUser["C09"]/ numberOfUsers, 100 * countingDiseaseByUser["C10"]/ numberOfUsers, 100 * countingDiseaseByUser["C11"]/ numberOfUsers, 100 * countingDiseaseByUser["C12"]/ numberOfUsers, 100 * countingDiseaseByUser["C13"]/ numberOfUsers, 100 * countingDiseaseByUser["C14"]/ numberOfUsers, 100 * countingDiseaseByUser["C15"]/ numberOfUsers, 100 * countingDiseaseByUser["C16"]/ numberOfUsers, 100 * countingDiseaseByUser["C17"]/ numberOfUsers, 100 * countingDiseaseByUser["C18"]/ numberOfUsers, 100 * countingDiseaseByUser["C19"]/ numberOfUsers, 100 * countingDiseaseByUser["C20"]/ numberOfUsers, 100 * countingDiseaseByUser["C21"]/ numberOfUsers, 100 * countingDiseaseByUser["C22"]/ numberOfUsers, 100 * countingDiseaseByUser["C23"]/ numberOfUsers, 100 * countingDiseaseByUser["C24"]/ numberOfUsers, 100 * countingDiseaseByUser["C25"]/ numberOfUsers, 100 * countingDiseaseByUser["C26"]/ numberOfUsers ] )

def appendMeshByUserWeighted(dataName, countingMeshWeightedByUser, numberOfUsers):
    meshByUserWeightedRow.append( [ dataName, 100 * countingMeshWeightedByUser["A"]/ numberOfUsers, 100 * countingMeshWeightedByUser["B"]/ numberOfUsers, 100 * countingMeshWeightedByUser["C"]/ numberOfUsers, 100 * countingMeshWeightedByUser["D"]/ numberOfUsers, 100 * countingMeshWeightedByUser["E"]/ numberOfUsers, 100 * countingMeshWeightedByUser["F"]/ numberOfUsers, 100 * countingMeshWeightedByUser["G"]/ numberOfUsers, 100 * countingMeshWeightedByUser["H"]/ numberOfUsers, 100 * countingMeshWeightedByUser["I"]/ numberOfUsers, 100 * countingMeshWeightedByUser["J"]/ numberOfUsers, 100 * countingMeshWeightedByUser["K"]/ numberOfUsers, 100 * countingMeshWeightedByUser["L"]/ numberOfUsers, 100 * countingMeshWeightedByUser["M"]/ numberOfUsers, 100 * countingMeshWeightedByUser["N"]/ numberOfUsers, 100 * countingMeshWeightedByUser["V"]/ numberOfUsers, 100 * countingMeshWeightedByUser["Z"]/ numberOfUsers  ] )

def appendDiseaseByUserWeighted(dataName, countingDiseaseWeightedByUser, numberOfUsers):
    diseaseByUserWeightedRow.append( [ dataName,  100 * countingDiseaseWeightedByUser["C01"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C02"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C03"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C04"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C05"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C06"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C07"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C08"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C09"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C10"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C11"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C12"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C13"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C14"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C15"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C16"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C17"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C18"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C19"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C20"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C21"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C22"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C23"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C24"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C25"]/ numberOfUsers, 100 * countingDiseaseWeightedByUser["C26"]/ numberOfUsers ] )

def appendCHV(dataName, countingCHVFound, numberCHV, numberUMLS, numberCHVMisspelled, numberOfQueries, npComboScore):
    totalCHVFound = 0
    for k,v in countingCHVFound.iteritems():
        totalCHVFound += (k*v)

    CHVRow.append( [dataName, totalCHVFound/numberOfQueries, numberCHV/numberOfQueries, numberUMLS/numberOfQueries, numberCHVMisspelled/numberOfQueries, npComboScore.mean, npComboScore.p0, npComboScore.p25, npComboScore.p50, npComboScore.p75, npComboScore.p100])

def appendSemanticFocus(dataName, vectorOfActionSequence, totalActions):
    semanticFocusRow.append( [ dataName, 100 * vectorOfActionSequence[0]/totalActions, 100 * vectorOfActionSequence[1]/totalActions, 100 * vectorOfActionSequence[2]/totalActions, 100 * vectorOfActionSequence[4]/totalActions, 100 * vectorOfActionSequence[3]/totalActions, 100 * vectorOfActionSequence[5]/totalActions, 100 * vectorOfActionSequence[6]/totalActions, 100 * vectorOfActionSequence[7]/totalActions ] )

def appendModifiedSession(dataName, vectorOfModifiedSessions, totalOfModifiedSessions):
    modifiedSessionRow.append( [dataName, 100 * vectorOfModifiedSessions[0]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[4]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[2]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[1]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[6]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[5]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[3]/totalOfModifiedSessions, 100 * vectorOfModifiedSessions[7]/totalOfModifiedSessions ] )

def appendCicleSequence(dataName, totalCicleSequence, numberOfSessions, vectorOfCicleSequence):
    cicleSequenceRow.append( [dataName, totalCicleSequence, 100.0 * totalCicleSequence/numberOfSessions, 100 * vectorOfCicleSequence[0]/totalCicleSequence, 100 * vectorOfCicleSequence[1]/totalCicleSequence, 100 * vectorOfCicleSequence[2]/totalCicleSequence, 100 * vectorOfCicleSequence[3]/totalCicleSequence, 100 * vectorOfCicleSequence[4]/totalCicleSequence, 100 * vectorOfCicleSequence[5]/totalCicleSequence] )

def appendMeshDepth(dataName, totalMeshDepth, countingMeshDepth):
    meshDepthRow.append( [dataName, 100/totalMeshDepth * countingMeshDepth[1], 100/totalMeshDepth * countingMeshDepth[2], 100/totalMeshDepth * countingMeshDepth[3], 100/totalMeshDepth * countingMeshDepth[4], 100/totalMeshDepth * countingMeshDepth[5], 100/totalMeshDepth * countingMeshDepth[6], 100/totalMeshDepth * countingMeshDepth[7],100/totalMeshDepth * countingMeshDepth[8], 100/totalMeshDepth * countingMeshDepth[9], 100/totalMeshDepth * countingMeshDepth[10], 100/totalMeshDepth * countingMeshDepth[11], 100/totalMeshDepth * countingMeshDepth[12]  ])

def appendSemanticByUser(dataName, semanticTypesCountedByUser, numberOfUsers):
    semanticByUserRow.append( [dataName, semanticTypesCountedByUser["symptom"], 100.0 * semanticTypesCountedByUser["symptom"]/numberOfUsers, semanticTypesCountedByUser["cause"], 100.0 * semanticTypesCountedByUser["cause"]/ numberOfUsers, semanticTypesCountedByUser["remedy"], 100.0 * semanticTypesCountedByUser["remedy"]/numberOfUsers, semanticTypesCountedByUser["where"], 100.0 * semanticTypesCountedByUser["where"]/numberOfUsers, semanticTypesCountedByUser["noMedical"], 100.0 * semanticTypesCountedByUser["noMedical"]/numberOfUsers ])
    
def appendSemanticByUserWeighted(dataName, numberOfUsers, semanticTypesCountedByUserWeighted):
    semanticByUserWeightedRow.append( [dataName, semanticTypesCountedByUserWeighted["symptom"], 100.0 * semanticTypesCountedByUserWeighted["symptom"]/numberOfUsers, semanticTypesCountedByUserWeighted["cause"], 100.0 * semanticTypesCountedByUserWeighted["cause"]/ numberOfUsers, semanticTypesCountedByUserWeighted["remedy"], 100.0 * semanticTypesCountedByUserWeighted["remedy"]/numberOfUsers, semanticTypesCountedByUserWeighted["where"], 100.0 * semanticTypesCountedByUserWeighted["where"]/numberOfUsers, semanticTypesCountedByUserWeighted["noMedical"], 100.0 * semanticTypesCountedByUserWeighted["noMedical"]/numberOfUsers ])

def appendBooleanUse(dataName, booleanTerms, numberOfQueries, usersUsingBools, numberOfUsers):
    booleanUseRow.append( [dataName, booleanTerms['and'], 100.0 * booleanTerms['and']/numberOfQueries, booleanTerms['or'], 100.0 * booleanTerms['or']/numberOfQueries,booleanTerms['not'], 100.0 * booleanTerms['not'] / numberOfQueries, booleanTerms['any'], 100.0 * booleanTerms['any'] / numberOfQueries, 100 * usersUsingBools/numberOfUsers] )

def appendPOS(dataName, countingPOS, numberOfQueries):
    totalPOS = sum(countingPOS.values())
    postagsRow.append( [dataName, totalPOS / numberOfQueries, countingPOS["noun"]/totalPOS, countingPOS["adj"]/totalPOS, countingPOS["prep"]/totalPOS, countingPOS["conj"]/totalPOS, countingPOS["aux"]/totalPOS, countingPOS["det"]/totalPOS, countingPOS["pron"]/totalPOS, countingPOS["verb"]/totalPOS, countingPOS["punc"]/totalPOS, countingPOS["shape"]/totalPOS, countingPOS["adv"]/totalPOS ])

