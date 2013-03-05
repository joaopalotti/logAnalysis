from __future__ import division
from collections import defaultdict, Counter
import operator
from myPlot import plotter
import statsmodels.distributions as sm
import numpy as np
from datetime import datetime
from nltk.tokenize.punkt import PunktWordTokenizer
from metrics import generateStatsVector
from latexTools import latexPrinter
#from nltk import word_tokenize, wordpunct_tokenize

####TODO: Add relative metrics like (X / total of queries are of size Y). Change it along the code!

PATH_TO_AUX_FILES = "auxFiles/"

def preProcessData(data, removeStopWords):
    data = tokenizeAllData(data)
    
    if removeStopWords:
        data = filterStopWords(data)
    return data

def calculateMetrics(dataList, removeStopWords=True, printPlotSizeOfWords=True, printPlotSizeOfQueries=True,\
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
    
    tableHeader = [ ["Dtst", "#Days", "#Qrs", "mnWrdsPQry", "mnQrsPDay", "Sssions", "mnQrsPrSsion","mTimePrSsion", "Exp", "Exp(%)", "Shr", "Shr(%)", "Ref", "Ref(%)", "Rep", "Rep(%)"] ]
    generalTableRow = []

    for dataPair in dataList:
        data, dataName = dataPair[0], dataPair[1]
        print "Processing information for data: ", dataName

        data = preProcessData(data, removeStopWords)

        percentageAcronym, countingAcronyms = calculateAcronyms(data)
        numberOfUsers = calculateUsers(data)
        npTerms, countingTokens, coOccurrenceList, greatestQuery, countingQueries = calculateTerms(data)
        numberOfSessions, countingQueriesPerSession, npNumQueriesInSession,\
                countingTimePerSession, npTime,\
                numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions = calculateQueriesPerSession(data)
        firstDay, lastDay, countingSessionsPerDay, countingQueriesPerDay, meanSessionsPerDay, meanQueriesPerDay = calculateDates(data)

        numberOfQueries = sum(countingQueries.values())
        
        # Print statistics
        with open(dataName + ".result", "w") as f:
            f.write("Metrics calculated:\n")
            printGeneralMetrics(f, numberOfUsers, numberOfQueries, numberOfSessions, firstDay, lastDay)
            printMetricsForTerms(f, npTerms, countingTokens, coOccurrenceList, percentageAcronym, countingAcronyms)
            printMetricsForQueries(f, greatestQuery, countingQueries, countingQueriesPerDay, meanQueriesPerDay)
            printMetricsForSessions(f, numberOfSessions, numberOfQueries, npNumQueriesInSession, npTime,\
                                    numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions,\
                                   countingSessionsPerDay, meanSessionsPerDay)

        countingAcronymsList.append([dataName, countingAcronyms])
        countingTimePerSessionList.append( [ dataName , countingTimePerSession ])
        countingTokensList.append( [dataName, countingTokens] )
        countingQueriesList.append([dataName, countingQueries] )
        countingQueriesPerSessionList.append([dataName, countingQueriesPerSession])

        #Data for tables
        generalTableRow.append( [ dataName, (lastDay - firstDay).days, numberOfQueries, npTerms.mean, meanQueriesPerDay, numberOfSessions, npNumQueriesInSession.mean, npTime.mean, numberOfExpansions, 100.0 * numberOfExpansions/ numberOfQueries , numberOfShrinkage, 100 * numberOfShrinkage/ numberOfQueries, numberOfReformulations, 100 * numberOfReformulations/numberOfQueries, numberOfRepetitions, 100 * numberOfRepetitions/numberOfQueries])

    
    myPlotter = plotter()
    
    if printQueriesPerSession:
        plotQueriesPerSession(myPlotter, countingQueriesPerSessionList, printValuesToFile)
    if printPlotFrequencyOfTerms:
        plotFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile)
    if printPlotFrequencyOfQueries:
        plotFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile)
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
        tableHeader.append( l )
    latexWriter.addTable(tableHeader, caption="General Numbers", transpose=True)


def calculateUsers(data):
    return   len(set( [ member.userId for member in data] ))

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

def plotCountingTimePerSessionListAcc(myPlotter, countingTimePerSessionList, printValuesToFile):
    
    for countingTimePerSessionPair in countingTimePerSessionList[:-1]:
        dataName = countingTimePerSessionPair[0]
        countingTimePerSession = countingTimePerSessionPair[1]

        ecdf = sm.ECDF( list(countingTimePerSession.elements()) )
        x = np.linspace(min(countingTimePerSession.keys()), max(countingTimePerSession.keys()))
        y = ecdf(x)
        myPlotter.plotXY(x, y, label=dataName, ylabelName="Frequency", xlabelName="Acc Time Per Session", showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="accTimePerSession")
    
    dataName, countingTimePerSession = countingTimePerSessionList[-1][0], countingTimePerSessionList[-1][1]
    ecdf = sm.ECDF( list(countingTimePerSession.elements()) )
    x = np.linspace(min(countingTimePerSession.keys()), max(countingTimePerSession.keys()))
    y = ecdf(x)
    
    myPlotter.plotXY(x, y, label=dataName, ylabelName="Frequency", xlabelName="Acc Time Per Session", saveName="accTimePerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotTimePerSession(myPlotter, countingTimePerSessionList, printValuesToFile):
    
    plotCountingTimePerSessionListAcc(myPlotter, countingTimePerSessionList, printValuesToFile)
    
    for countingTimePerSessionPair in countingTimePerSessionList[:-1]:
        dataName, countingTimePerSession = countingTimePerSessionPair[0], countingTimePerSessionPair[1]
        myPlotter.plotCounter(countingTimePerSession, label=dataName, ylabelName="Frequency", xlabelName="Time Per Session (Seconds)", showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="timePerSession")

    countingTimePerSessionPair = countingTimePerSessionList[-1]
    dataName, countingTimePerSession = countingTimePerSessionPair[0], countingTimePerSessionPair[1]
    myPlotter.plotCounter(countingTimePerSession, label=dataName, ylabelName="Frequency", xlabelName="Time Per Session (Seconds)", \
                saveName="timePerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)


def plotQueriesPerSession(myPlotter, countingQueriesPerSessionList, printValuesToFile):

    for countingQueriesPerSessionPair in countingQueriesPerSessionList[:-1]:
        dataName, countingQueriesPerSession = countingQueriesPerSessionPair[0], countingQueriesPerSessionPair[1]
        myPlotter.plotCounter(countingQueriesPerSession, label=dataName, xlabelName="Queries Per Session", ylabelName="Frequency", showIt=False, lastOne=False, printValuesToFile=printValuesToFile,saveName="queriesPerSession")
    
    countingQueriesPerSessionPair = countingQueriesPerSessionList[-1]
    dataName, countingQueriesPerSession = countingQueriesPerSessionPair[0], countingQueriesPerSessionPair[1]
    myPlotter.plotCounter(countingQueriesPerSession, label=dataName, xlabelName="Queries Per Session", ylabelName="Frequency", saveName="queriesPerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotAcronymFrequency(myPlotter, countingAcronymsList, printValuesToFile):
    
    for countingAcronymsPair in countingAcronymsList[:-1]:
        dataName, countingAcronyms = countingAcronymsPair[0], countingAcronymsPair[1]
        myPlotter.plotFrequency(countingAcronyms.values(), "Acronyms Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="acronymFreq")
    
    countingAcronymsPair = countingAcronymsList[-1]
    dataName, countingAcronyms = countingAcronymsPair[0], countingAcronymsPair[1]
    myPlotter.plotFrequency(countingAcronyms.values(), "Acronyms Repetition", label=dataName, saveName="acronymFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile):
    
    for countingQueriesPair in countingQueriesList[:-1]:
        dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
        myPlotter.plotFrequency(countingQueries.values(), "Query Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesFre")

    countingQueriesPair = countingQueriesList[-1]
    dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
    myPlotter.plotFrequency(countingQueries.values(), "Query Repetition", label=dataName, saveName="queriesFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile):

    for countingTokensPair in countingTokensList[:-1]:
        dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
        myPlotter.plotFrequency(countingTokens.values(), "Term Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="termFreq")
    
    countingTokensPair = countingTokensList[-1]
    dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
    myPlotter.plotFrequency(countingTokens.values(), "Term Repetition", label=dataName, saveName="termFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotSizeOfQueries(myPlotter, dataList, printValuesToFile):
    
    queriesSize = []
    for dataItem in dataList[:-1]:
        data, dataName = dataItem[0], dataItem[1]
        queriesSize = [ len(member.keywords) for member in data ] 
        myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesSize")

    data, dataName = dataList[-1][0], dataList[-1][1]
    queriesSize = [ len(member.keywords) for member in data ] 
    myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, saveName="queriesSize", showIt=False, lastOne=True, relative=True, printValuesToFile=printValuesToFile)

def plotSizeOfWords(myPlotter, dataList, printValuesToFile):
    
    wordsSize = []
    for dataItem in dataList[:-1]:
        data, dataName = dataItem[0], dataItem[1]
        queriesSize = [ len(member.keywords) for member in data ] 
        wordsSize = [ len(word) for member in data for word in member.keywords]
        myPlotter.plotFrequency(wordsSize, "Word Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="wordSize")

    wordsSize = [ len(word) for member in dataList[-1][0] for word in member.keywords]
    dataName = dataList[-1][1]
    myPlotter.plotFrequency(wordsSize, "Word Size", label=dataName, saveName="wordSize", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def tokenizeAllData(data):
    
    for member in data:
        member.keywords = tokenize(member.keywords)
        if member.previouskeywords:
            member.previouskeywords = tokenize(member.previouskeywords)
    return data

def filterStopWords(data):
    
    stopWords = set()
    #Using as reference: http://jmlr.csail.mit.edu/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
    with open(PATH_TO_AUX_FILES + "stopWords.txt","r") as f:
        for line in f:
            stopWords.add(line.strip())

    for member in data:
        noStopWords = [ keyword for keyword in member.keywords if keyword not in stopWords]
        member.keywords = noStopWords[:]
        if member.previouskeywords:
            noStopWords = [ keyword for keyword in member.previouskeywords if keyword not in stopWords]
            member.previouskeywords = noStopWords[:]

    return data

def compareSets(set1, set2):
    #print "Comparing ", set1, " and ", set2
    #numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions
    if set1 == set2:
        return 0,0,0,1
    elif set1 > set2:
        return 0,1,0,0
    elif set1 < set2:
        return 1,0,0,0
    else: 
        return 0,0,1,0
    

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
            subQueryE, subQueryS, subQueryRef, subQueryRep = 0,0,0,0
            for query in subSession[1:]:
                e, s, ref, rep = compareSets( set(previousQuery[1]), set(query[1]))
                numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions =\
                        e + numberOfExpansions, s + numberOfShrinkage, ref + numberOfReformulations, rep + numberOfRepetitions
                subQueryE, subQueryS, subQueryRef, subQueryRep = subQueryE + e, subQueryS + s, subQueryRef + ref, subQueryRep + rep
                
                #print "Session === ", subSession
                #print "Q1  = ", set(previousQuery[1]), " Q2 = ", set(query[1])
                #print " numberOfExpansions = ", numberOfExpansions, " numberOfShrinkage = ", numberOfShrinkage, " numberOfReformulations = ", numberOfReformulations, " numberOfRepetitions = ", numberOfRepetitions

                # If a repetition occurs, we do not consider it as a modified session
                if e > 0 or s > 0 or ref > 0:
                    modifiedSubSession = True 
                previousQuery = query
                
            if modifiedSubSession:
                be, bs, bref, brep = 0 if subQueryE == 0 else 1, 0 if subQueryS == 0 else 1, 0 if subQueryRef == 0 else 1, 0 if subQueryRep == 0 else 1
                indexVal =  int( str(be) + str(bs) + str(bref), 2) if ignoreRepetition else int( str(be) + str(bs) + str(bref) + str(brep), 2)
                #print "INDEX = ", indexVal
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
            sessions[member.userId][1] = [[member.datetime, member.keywords]]

        # There are no previous keywords and there is at least one sessions of this id 
        elif member.previouskeywords is None and sessions[member.userId]:
            sessions[member.userId][ len(sessions[member.userId]) + 1 ] = [[member.datetime, member.keywords]]
        
        elif member.previouskeywords is not None and not sessions[member.userId]:
            # This situation should not happen, but it does. It means that a session was not created but there were previous keywords.
            #print "ERROR!"
            #print member.userId, member.datetime, member.keywords, "previous ---> ", member.previouskeywords
            sessions[member.userId][1] = [[member.datetime, member.keywords]]

        # There are previous keywords!
        else:
            sessions[member.userId][ len(sessions[member.userId]) ] += [[member.datetime,member.keywords]]

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
    
    # The number of sessions with more that 2 queries HAVE to be the same that the number of modified session
    #print "SUM = ", sum(vectorOfModifiedSessions), " More than one = ", sessionsWithMoreThanOneQuery, " rep =", numberOfRepetitions
    #print vectorOfModifiedSessions
    ###TODO CHECK code :
    #assert sum(vectorOfModifiedSessions) == sessionsWithMoreThanOneQuery
    

    #print numberOfSessions, npNumQueriesInSession, npTime
    return numberOfSessions, countingQueriesPerSession, npNumQueriesInSession,\
            countingTimePerSession, npTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions,\
            vectorOfModifiedSessions

def tokenize(keywordList):
    # split query into words and eliminate blank spaces
    
    #return [ w.strip().lower() for w in keywordList.split(" ") if w.strip() ]
    #return [ w.strip().lower() for w in nltk.wordpunct_tokenize(keywordList) if w.strip() ]
    return [ w.strip().lower() for w in PunktWordTokenizer().tokenize(keywordList) if w.strip() ]
    

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
    for d1 in matrix:
        for d2 in matrix[d1]:
            #print d1, d2, countingTokens[d1], countingTokens[d2]
            if matrix[d1][d2] / countingTokens[d1] >= coOccurrenceThreshold or\
               matrix[d1][d2] / countingTokens[d2] >= coOccurrenceThreshold:
                #print d1, d2, matrix[d1][d2]
                coOccurrenceList.append( [d1, d2, matrix[d1][d2], matrix[d1][d2]/numberOfQueries, matrix[d1][d2]/countingTokens[d1], matrix[d1][d2]/countingTokens[d2]] )

    # Calculate basic metrics
    npTerms = generateStatsVector(queryInNumbers)
    
    return npTerms, countingTokens, coOccurrenceList, greatestQuery, countingQueries


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
 
def printMetricsForTerms(writer, npTerms, countingTokens, coOccurrenceList, percentageAcronym, countingAcronyms):
    
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
    writer.write('{0:30} | {1:30} | {2:4} | {3:4} | {4:7} | {5:7}\n'.format("Word1","Word2","Tog.","% Tog.","W1W2","W2W1"))
    #writer.write("Word1\tWord2\t\t\tTimes together\tSupport W1W2\tConfidence W1->W2\t Confidence W2->W1" + "\n")
    coOccurrenceList = sorted(coOccurrenceList, key=operator.itemgetter(3),reverse=True)
    for nestedList in coOccurrenceList:
        writer.write('{0:30} | {1:30} | {2:4d} | {3:.4f} | {4:.5f} | {5:.5f}\n'.format(nestedList[0],nestedList[1],nestedList[2],nestedList[3],nestedList[4],nestedList[5]))
        #writer.write( nestedList[0], '\t',  nestedList[1], '\t\t\t' , nestedList[2], '\t', nestedList[3], '\t', nestedList[4], '\t', nestedList[5]
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
    

def printMetricsForSessions(writer, numberOfSessions, numberOfQueries, npNumQueriesInSession, npTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions, countingSessionsPerDay, meanSessionsPerDay):

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
    writer.write("-" * 80 + "\n")

