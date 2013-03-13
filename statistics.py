from __future__ import division
from collections import defaultdict, Counter
import operator
from datetime import datetime

from metrics import generateStatsVector
from myPlot import plotter
from latexTools import latexPrinter
from auxiliarFunctions import *
from plotFunctions import *

####TODO: Add relative metrics like (X / total of queries are of size Y). Change it along the code!


def calculateMetrics(dataList, usingMesh=True, removeStopWords=False, printPlotSizeOfWords=True, printPlotSizeOfQueries=True,\
                     printPlotFrequencyOfQueries=True, printPlotFrequencyOfTerms=True, printPlotAcronymFrequency=True,\
                     printQueriesPerSession=True, printTimePerSession=True, printValuesToFile=True):
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
    
    tableGeneralHeader = [ ["Dtst", "#Days", "#Qrs", "mnWrdsPQry", "mnQrsPDay", "Sssions", "mnQrsPrSsion","mTimePrSsion", "Exp", "Exp(%)", "Shr", "Shr(%)", "Ref", "Ref(%)", "Rep", "Rep(%)", "QrsWithMesh", "MeshIds", "DiseIds"] ]
    tableMeshHeader = [ ["Dtst","A","B","C","D","E","F","G","H","I","J","K","L","M","N","V","Z"] ]
    tableDiseasesHeader = [ ["Dtst","C01","C02","C03","C04","C05","C06","C07","C08","C09","C10","C11","C12","C13","C14","C15","C16","C17","C18","C19","C20","C21","C22","C23","C24","C25","C26"] ]
    tableSemanticFocusHeader = [ ["Dtst", "Nothing", "Symptom", "Cause", "Remedy", "SymptomCause", "SymptomRemedy", "CauseRemedy", "SymptomCauseRemedy"] ]
    tableModifiedSessionHeader = [["Dtst","Nothing","Expansion","Shrinkage","Reformulation","ExpansionShrinkage","ExpansionReformulation","ShrinkageReformulation","ExpansionShrinkageReformulation"]] 

    generalTableRow = []
    meshTableRow = []
    diseaseTableRow = []
    semanticFocusRow = []
    modifiedSessionRow = []

    for dataPair in dataList:
        data, dataName = dataPair[0], dataPair[1]
        print "Processing information for data: ", dataName

        data = preProcessData(data, removeStopWords)

        percentageAcronym, countingAcronyms = calculateAcronyms(data)
        numberOfUsers = calculateUsers(data)
        npTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, greatestQuery, countingQueries = calculateTerms(data)
        numberOfSessions, countingQueriesPerSession, npNumQueriesInSession, countingTimePerSession, npTime,\
                numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions,\
                countingSemantics, countingPureSemanticTypes, vectorOfActionSequence,\
                countingReAccess = calculateQueriesPerSession(data)
        firstDay, lastDay, countingSessionsPerDay, countingQueriesPerDay, meanSessionsPerDay, meanQueriesPerDay = calculateDates(data)
        countingNL = calculateNLuse(data)


        numberOfQueries = sum(countingQueries.values())

        hasMeshValues = 0
        if usingMesh:
            countingMesh, countingDisease, hasMeshValues = calculateMesh(data)

        # Print statistics
        with open(dataName + ".result", "w") as f:
            print "Writing file ", dataName + ".result..."
            f.write("Metrics calculated:\n")
            printGeneralMetrics(f, numberOfUsers, numberOfQueries, numberOfSessions, firstDay, lastDay)
            printMetricsForTerms(f, npTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, percentageAcronym, countingAcronyms, countingNL, numberOfUsers)
            printMetricsForQueries(f, greatestQuery, countingQueries, countingQueriesPerDay, meanQueriesPerDay)
            printMetricsForSessions(f, numberOfSessions, numberOfQueries, npNumQueriesInSession, npTime,\
                                    numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions,\
                                   countingSessionsPerDay, meanSessionsPerDay, countingReAccess, numberOfUsers)
            printMeshClassificationMetrics(f, countingMesh, countingDisease)

        countingAcronymsList.append([dataName, countingAcronyms])
        countingTimePerSessionList.append( [ dataName , countingTimePerSession ])
        countingTokensList.append( [dataName, countingTokens] )
        countingQueriesList.append([dataName, countingQueries] )
        countingQueriesPerSessionList.append([dataName, countingQueriesPerSession])
        if usingMesh:
            countingMeshList.append([dataName, countingMesh])
            countingDiseaseList.append([dataName, countingDisease])

        #Data for tables
        numberOfMeshTerms = sum(countingMesh.values())
        numberOfMeshDiseases = sum(countingDisease.values())


        generalTableRow.append( [ dataName, (lastDay - firstDay).days, numberOfQueries, npTerms.mean, meanQueriesPerDay, numberOfSessions, npNumQueriesInSession.mean, npTime.mean, numberOfExpansions, 100.0 * numberOfExpansions/ numberOfQueries , numberOfShrinkage, 100 * numberOfShrinkage/ numberOfQueries, numberOfReformulations, 100 * numberOfReformulations/numberOfQueries, numberOfRepetitions, 100 * numberOfRepetitions/numberOfQueries, hasMeshValues, numberOfMeshTerms, numberOfMeshDiseases] )
        
        #To avoid division by zero
        numberOfMeshTerms = numberOfMeshTerms if numberOfMeshTerms != 0 else 1
        numberOfMeshDiseases = numberOfMeshDiseases if numberOfMeshDiseases != 0 else 1
        
        meshTableRow.append( [ dataName, countingMesh["A"]/ numberOfMeshTerms, countingMesh["B"]/ numberOfMeshTerms, countingMesh["C"]/ numberOfMeshTerms, countingMesh["D"]/ numberOfMeshTerms, countingMesh["E"]/ numberOfMeshTerms, countingMesh["F"]/ numberOfMeshTerms, countingMesh["G"]/ numberOfMeshTerms, countingMesh["H"]/ numberOfMeshTerms, countingMesh["I"]/ numberOfMeshTerms, countingMesh["J"]/ numberOfMeshTerms, countingMesh["K"]/ numberOfMeshTerms, countingMesh["L"]/ numberOfMeshTerms, countingMesh["M"]/ numberOfMeshTerms, countingMesh["N"]/ numberOfMeshTerms, countingMesh["V"]/ numberOfMeshTerms, countingMesh["Z"]/ numberOfMeshTerms  ] )
        diseaseTableRow.append( [ dataName,  countingDisease["C01"]/ numberOfMeshDiseases, countingDisease["C02"]/ numberOfMeshDiseases, countingDisease["C03"]/ numberOfMeshDiseases, countingDisease["C04"]/ numberOfMeshDiseases, countingDisease["C05"]/ numberOfMeshDiseases, countingDisease["C06"]/ numberOfMeshDiseases, countingDisease["C07"]/ numberOfMeshDiseases, countingDisease["C08"]/ numberOfMeshDiseases, countingDisease["C09"]/ numberOfMeshDiseases, countingDisease["C10"]/ numberOfMeshDiseases, countingDisease["C11"]/ numberOfMeshDiseases, countingDisease["C12"]/ numberOfMeshDiseases, countingDisease["C13"]/ numberOfMeshDiseases, countingDisease["C14"]/ numberOfMeshDiseases, countingDisease["C15"]/ numberOfMeshDiseases, countingDisease["C16"]/ numberOfMeshDiseases, countingDisease["C17"]/ numberOfMeshDiseases, countingDisease["C18"]/ numberOfMeshDiseases, countingDisease["C19"]/ numberOfMeshDiseases, countingDisease["C20"]/ numberOfMeshDiseases, countingDisease["C21"]/ numberOfMeshDiseases, countingDisease["C22"]/ numberOfMeshDiseases, countingDisease["C23"]/ numberOfMeshDiseases, countingDisease["C24"]/ numberOfMeshDiseases, countingDisease["C25"]/ numberOfMeshDiseases, countingDisease["C26"]/ numberOfMeshDiseases ] )

        # ["Dtst", "Nothing", "Symptom", "Cause", "Remedy", "SymptomCause", "SymptomRemedy", "CauseRemedy", "SymptomCauseRemedy"]
        semanticFocusRow.append( [ dataName, vectorOfActionSequence[0], vectorOfActionSequence[1], vectorOfActionSequence[2], vectorOfActionSequence[4], vectorOfActionSequence[3], vectorOfActionSequence[5], vectorOfActionSequence[6], vectorOfActionSequence[7] ] )

        #["Dtst","Nothing","Expansion","Shrinkage","Reformulation","ExpansionShrinkage","ExpansionReformulation","ShrinkageReformulation","ExpansionShrinkageReformulation"]
        modifiedSessionRow.append( [dataName, vectorOfModifiedSessions[0], vectorOfModifiedSessions[4], vectorOfModifiedSessions[2], vectorOfModifiedSessions[1], vectorOfModifiedSessions[6], vectorOfModifiedSessions[5], vectorOfModifiedSessions[3], vectorOfModifiedSessions[7] ] )

    myPlotter = plotter()
    
    if printQueriesPerSession:
        plotQueriesPerSession(myPlotter, countingQueriesPerSessionList, printValuesToFile)
    if printPlotFrequencyOfTerms:
        plotFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile)
        plotLogLogFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile)
    if printPlotFrequencyOfQueries:
        plotFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile)
        plotLogLogFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile)
    if printTimePerSession:
        plotTimePerSession(myPlotter, countingTimePerSessionList, printValuesToFile)
    if printPlotAcronymFrequency:
        plotAcronymFrequency(myPlotter, countingAcronymsList, printValuesToFile)
    if printPlotSizeOfWords:
        plotSizeOfWords(myPlotter, dataList, printValuesToFile)
    if printPlotSizeOfQueries:
        plotSizeOfQueries(myPlotter, dataList, printValuesToFile)

    #Print latex tables:
    latexWriter = latexPrinter() 
    for l in generalTableRow: 
        tableGeneralHeader.append( l )
   
    for l in meshTableRow:
        tableMeshHeader.append( l )
    
    for l in diseaseTableRow:
        tableDiseasesHeader.append( l )

    for l in semanticFocusRow:
        tableSemanticFocusHeader.append(l)

    for l in modifiedSessionRow:
        tableModifiedSessionHeader.append(l)

    latexWriter.addTable(tableGeneralHeader, caption="General Numbers", transpose=True)
    latexWriter.addTable(tableModifiedSessionHeader, caption="Modifications in a session", transpose=True)
    latexWriter.addTable(tableMeshHeader, caption="Mesh Table", transpose=True)
    latexWriter.addTable(tableDiseasesHeader, caption="Diseases Table", transpose=True)
    latexWriter.addTable(tableSemanticFocusHeader, caption="Semantic Focus", transpose=True)



def hasNLword(words):
    #TODO: find a better list:
    # possibility: use Noun + Verb Phrase or other structures like that
    interestingWords = ["would", "wouldn't", "wouldnt", "could", "couldn't", "couldnt", "should", "shouldn't", "shouldnt", "how", "when", "where", "which", "who", "whom", "can", "cannot", "why", "what", "we", "they", "i", "do", "does"]
    return len( [ w for w in words if w.lower() in interestingWords ] ) > 0

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
    meshValues = ( member.mesh for member in data if member.mesh )
    meshValues = [ v for values in meshValues for v in values if v != '' ]

    hasMeshValues =  sum( 1 for member in data if member.mesh )
    
    meshDiseases = ( values for values in meshValues if values.startswith('C') )
    meshValues = ( values[0] for values in meshValues )
    countingDisease = Counter(meshDiseases)
    countingMesh = Counter(meshValues)
    
    #print countingDisease, countingMesh
    return countingMesh, countingDisease, hasMeshValues

def calculateUsers(data):
    return len(set( [ member.userId for member in data] ))

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

    acronymsSet = set()
    #http://en.wikipedia.org/wiki/List_of_acronyms_for_diseases_and_disorders
    #http://en.wikipedia.org/wiki/List_of_abbreviations_for_medical_organisations_and_personnel
    #http://en.wikipedia.org/wiki/Acronyms_in_healthcare
    #http://en.wikipedia.org/wiki/List_of_medical_abbreviations -- From A to Z

    for filename in [ "diseasesAcronyms.txt", "healthCareAcronyms.txt", "organizationAcronyms.txt", "medicalAbbreviations.txt" ]:
        with open(PATH_TO_AUX_FILES + filename,"r") as f:
            for line in f.readlines():
                acronymsSet.add( (line.split(",", 1)[0].strip()).lower() )
    
    hasAcronym = [ member.keywords for member in data for word in member.keywords if word in acronymsSet]
    acronymList = [ word for member in data for word in member.keywords if word in acronymsSet]
    percentageAcronym = len(hasAcronym) / len(data)
    countingAcronyms = Counter(acronymList)

    #print percentageAcronym
    #print acronymList
    #print hasAcronym
    return percentageAcronym, countingAcronyms

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

def calculateQueriesPerSession(data):
    '''
        I am considering all sessions here. An alternative option would be to consider only the sessions with more that X queries. (e.g. X > 3)
    '''
    sessions = defaultdict(dict)

    for member in data:

        # There are no previous keywords and no sessions of this id -> create the first one sessions[id][1] = list
        if member.previouskeywords is None and not sessions[member.userId]:
            sessions[member.userId][1] = [[member.datetime, member.keywords, member.semanticTypes]]

        # There are no previous keywords and there is at least one sessions of this id 
        elif member.previouskeywords is None and sessions[member.userId]:
            sessions[member.userId][ len(sessions[member.userId]) + 1 ] = [[member.datetime, member.keywords, member.semanticTypes]]
        
        elif member.previouskeywords is not None and not sessions[member.userId]:
            # This situation should not happen, but it does. It means that a session was not created but there were previous keywords.
            #print "ERROR!"
            #print member.userId, member.datetime, member.keywords, "previous ---> ", member.previouskeywords
            sessions[member.userId][1] = [[member.datetime, member.keywords, member.semanticTypes]]

        # There are previous keywords!
        else:
            sessions[member.userId][ len(sessions[member.userId]) ] += [[member.datetime,member.keywords, member.semanticTypes]]

    #for session, date in sessions.iteritems():
    #    print session, date

    numberOfSessions = sum( len(s) for s in sessions.values() )
    queriesPerSession = [ len(q) for session in sessions.values() for q in session.values() ]
    sessionsWithMoreThanOneQuery = len([ 1 for session in sessions.values() for q in session.values() if len(q) > 1 ])
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
    countingSemantics, countingPureSemanticTypes, vectorOfActionSequence = calculateSemanticTypes(sessions)

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
            vectorOfModifiedSessions, countingSemantics, countingPureSemanticTypes, vectorOfActionSequence, countingReAccess


def calculateReAccessInDifferentSessions(sessions):
    countingReAccess = defaultdict(int) # { usedId: numberOfReAcess } 
    '''
    Number of users who had a re-access: len(countingReAccess)
    Total number of re-access: sum(countingReAccess.values())
    '''
    
    for userId, session in sessions.iteritems():
        
        uniqueQueries = {}
        pastQueries = {}

        for subSession in session.values():
            queries = {}

            for query in subSession:
                queries[ tuple(set(query[1])) ] = 1 #using set to ignore order
                #print "usedId =>", userId, "Query => ", query[1]

                if tuple(set(query[1])) in pastQueries:
                    #print "FOUND RE ACCESS HERE ---> ", query[1]
                    countingReAccess[userId] += 1

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

"""
    Input:
        sessions ---> { id: { sessionCounter: [ [Query1], [Q2], [Q3] ], sessionCounter2: [[Q1], [Q2], [Q3]]  }  }
        id -> user identification
        QueryX -> [ datetime, keywords, semanticTypes]
        sessionCounter -> counter starting from 1

    Some important semantic types (list: http://metamap.nlm.nih.gov/SemanticTypeMappings_2011AA.txt)
        -> Symptom   -> sosy (Sign or Symptom)
        -> Cause     -> bact (Bacterium), virs (Virus), dsyn (Disease or Syndrome), orgm (Organism)
        -> Remedy    -> drdd (Drug Delivery Device), clnd (Clinical Drug), amas (Amino Acid Sequence ?)
        -> where     -> bpoc (Body Part, Organ, or Organ Component), bsoj (Body Space or Junction)
"""
def calculateSemanticTypes(sessions):

    countingSemantics = { "symptom":0, "cause": 0, "remedy": 0, "where": 0 }
    countingPureSemanticTypes = defaultdict(int)
    vectorOfActionSequence = [0] * 8 # [ 2^{remedy,cause,symptom} in this order ] 

    for session in sessions.values():
        for subSession in session.values():
            #print subSession
            
            actionSequency = []
            for query in subSession:
                if query[2] is not None:
                    #print "Semantic Type => ", query[2]
                    
                    for st in query[2]:
                        countingPureSemanticTypes[st] += 1
                        
                        if st in ["sosy"]:
                            actionSequency.append("symptom")
                            countingSemantics["symptom"] += 1
                        elif st in ["bact", "virs", "dsyn", "orgm"]:
                            actionSequency.append("cause")
                            countingSemantics["cause"] += 1
                        elif st in ["drdd", "clnd", "amas"]:
                            actionSequency.append("remedy")
                            countingSemantics["remedy"] += 1
                        elif st in ["bpoc", "bsoj"]:
                            actionSequency.append("where")
                            countingSemantics["where"] += 1

            #analyse the sequence of symptom followed by causes, etc.
            index = analyzeSequencyOfActions(actionSequency)
            #print "INDEX = ", index
            vectorOfActionSequence[index] += 1

    #print countingSemantics
    #print countingPureSemanticTypes
    #print "Vector of Action Sequence ", vectorOfActionSequence
    return countingSemantics, countingPureSemanticTypes, vectorOfActionSequence

def calculateTerms(data, coOccurrenceThreshold=0.6):
    """
        Calculate Max, Min, Mean, Median of terms along all the queries
        Also count the occurrences of each term and the co-occurrence of terms.
        The coOccurrenceThreshold is a parameter that indicates the minimal number of times that 
        term X has to appears together with term Y among all the apparences of term X or Y.
    """
   
    # I had to transforme the list into a tuple to use the counter
    allQueries = [ tuple(sorted(member.keywords)) for member in data ] 
    countingQueries = Counter(allQueries)

    # separate the information about the queries from the rest of the data
    listOfQueries = [ member.keywords for member in data ]
    
    # Count the number of keywords used in each single query
    queryInNumbers = [ len( query ) for query in listOfQueries]

    indexGreatestQuery, _ = max(enumerate(queryInNumbers), key=operator.itemgetter(1))
    greatestQuery = listOfQueries[indexGreatestQuery]

    #print queryInNumbers
    #print greatestQuery, len(greatestQuery)

    # Transform the query into a list of simple tokens and count them
    tokens = [ t.lower() for sublist in listOfQueries for t in sublist]
    countingTokens = Counter(tokens)

    # Calculate the Co-occurrence matrix
    matrix = defaultdict(dict)
    for query in listOfQueries:
        #print "Q = ", query
        for i in range(len(query) - 1):
            first = query[i].lower()
            
            for j in range(i + 1, len(query)):
                second = query[j].lower()

                d1, d2 = min(first,second), max(first,second)
                if not d2 in matrix[d1]:
                    matrix[d1] = defaultdict(int)
                matrix[d1][d2] += 1

    # Filter the results using the parameter coOccurrenceThreshold and generate the coOccurrenceList
    numberOfQueries = len(listOfQueries)
    coOccurrenceList = []
    simpleCoOccurrenceList = []

    for d1 in matrix:
        for d2 in matrix[d1]:
            #print d1, d2, countingTokens[d1], countingTokens[d2]
            if matrix[d1][d2] / countingTokens[d1] >= coOccurrenceThreshold or\
               matrix[d1][d2] / countingTokens[d2] >= coOccurrenceThreshold:
                #print d1, d2, matrix[d1][d2]
                coOccurrenceList.append( [d1, d2, matrix[d1][d2], matrix[d1][d2]/numberOfQueries, matrix[d1][d2]/countingTokens[d1], matrix[d1][d2]/countingTokens[d2]] )
            simpleCoOccurrenceList.append( [d1, d2, matrix[d1][d2], matrix[d1][d2]/numberOfQueries, matrix[d1][d2]/countingTokens[d1], matrix[d1][d2]/countingTokens[d2]] )

    # Calculate basic metrics
    npTerms = generateStatsVector(queryInNumbers)
    
    return npTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, greatestQuery, countingQueries


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
 
def printMetricsForTerms(writer, npTerms, countingTokens, coOccurrenceList, simpleCoOccurrenceList, percentageAcronym, countingAcronyms, countingNL, numberOfUsers):
    
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
    
    writer.write('{0:45} ==> {1:.3f}\n'.format('Percentage of Acronyms used', (percentageAcronym)))
    
    writer.write("-" * 45 + "\n")
    writer.write("10 Most Common Terms:\n")
    
    writer.write("-" * 45 + "\n")
    for pair in countingTokens.most_common(10):
        writer.write('{0:45} ==> {1:30}\n'.format(pair[0], str(pair[1])))
    writer.write("-" * 45 + "\n")
     
    writer.write("10 Most Common Acronyms:\n")
    writer.write("-" * 45 + "\n")
    for pair in countingAcronyms.most_common(10): 
        writer.write('{0:45} ==> {1:30}\n'.format(pair[0], str(pair[1])))
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
    writer.write('{0:45} ==> {1:d}\n'.format("Total number of NL in queries:", sum(countingNL.values())))    
    writer.write("-" * 45 + "\n")
    writer.write("-" * 80 + "\n")


def printMetricsForQueries(writer, greatestQuery, countingQueries, countingQueriesPerDay, meanQueriesPerDay):

    writer.write("-" * 80 + "\n")
    writer.write("-" * 45 + "\n")
    writer.write("For QUERIES:\n")
    writer.write("-" * 45 + "\n")

    uniqueQueries = len(countingQueries)
    allQueries = sum(countingQueries.values())
    writer.write('{0:45} ==> {1:30}\n'.format('Total Number of Unique Queries', str(uniqueQueries)))
    writer.write('{0:45} ==> {1:30}\n'.format('Total Number of Queries', str(allQueries)))
    writer.write('{0:45} ==> {1:.3f} %\n'.format('Percentage Of Repeated queries ', 100 * (allQueries - uniqueQueries)/allQueries ))
    writer.write('{0:45} ==> {1:30}\n'.format('Greatest Query', ' '.join(greatestQuery)))
    writer.write('{0:45} ==> {1:30}\n'.format("Mean number of Queries per day", str(meanQueriesPerDay)))
    
    writer.write("-" * 45 + "\n")
    writer.write("10 Most Common Queries:\n")
    writer.write("-" * 45 + "\n")
    for pair in countingQueries.most_common(10):
        writer.write('{0:45} ==> {1:30}\n'.format(pair[0], str(pair[1])))
    writer.write("-" * 45 + "\n")   
    writer.write("-" * 80 + "\n")
    

def printMetricsForSessions(writer, numberOfSessions, numberOfQueries, npNumQueriesInSession, npTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions, countingSessionsPerDay, meanSessionsPerDay, countingReAccess, numberOfUsers):

    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("For SESSIONS:\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Sessions", str(numberOfSessions)))
    writer.write("-" * 40 + "\n")
    writer.write("Session Length in Queries\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:.3f}\n'.format("Maximum number of Queries in a session", (npNumQueriesInSession.max)))
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
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Modified Session ", str(sum(vectorOfModifiedSessions))))
    writer.write('{0:45} ==> {1:.3f}\n'.format("Percentage of Modified Session ", sum(vectorOfModifiedSessions)/numberOfSessions))
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Modified Queries", str(numberOfExpansions + numberOfShrinkage + numberOfReformulations + numberOfRepetitions)))
    writer.write('{0:45} ==> {1:15}{2:.3f}(%)\n'.format("Number of Expansions", str(numberOfExpansions),numberOfExpansions/numberOfQueries))    
    writer.write('{0:45} ==> {1:15}{2:.3f}(%)\n'.format("Number of Shrinkages", str(numberOfShrinkage), numberOfShrinkage/numberOfQueries))    
    writer.write('{0:45} ==> {1:15}{2:.3f}(%)\n'.format("Number of Reformulations", str(numberOfReformulations), numberOfReformulations/numberOfQueries))    
    writer.write('{0:45} ==> {1:15}{2:.3f}(%)\n'.format("Number of Repetitions", str(numberOfRepetitions), numberOfRepetitions/numberOfQueries))    
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Mean Number of Sessions Per Day", str(meanSessionsPerDay)))    
    writer.write("-" * 40 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:d}, {2:.2f}(%)\n'.format("Number of users re-accessing information:", len(countingReAccess), 100*len(countingReAccess)/numberOfUsers))
    writer.write('{0:45} ==> {1:d}\n'.format("Total number of re-access inter sessions:", sum(countingReAccess.values())))    
    writer.write("-" * 80 + "\n")

def printMeshClassificationMetrics(writer, countingMesh, countingDisease):
    
    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("MESH CLASSIFICATION:\n")
    writer.write("-" * 40 + "\n")
    totalMesh = sum (countingMesh.values() )
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Mesh identifiers", totalMesh ))
    
    writer.write("-" * 40 + "\n")
    for k,v in countingMesh.iteritems():
        writer.write('{0:>15} ------- {1:<10} ({2:.2f}%)\n'.format( k, v, v/totalMesh ))

    writer.write("-" * 40 + "\n")
    totalDisease = sum(countingDisease.values() )
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Disesase identifiers", totalDisease ) )
    writer.write("-" * 40 + "\n")
    
    for k,v in countingDisease.iteritems():
        writer.write('{0:>15} ------- {1:<10} ({2:.2f}%)\n'.format( k, v, v/totalDisease ))
    
    writer.write("-" * 40 + "\n")
    writer.write("-" * 80 + "\n")

