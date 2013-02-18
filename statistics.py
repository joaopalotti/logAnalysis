from __future__ import division
from tripData import TripData
from collections import defaultdict, Counter
import operator
from myPlot import plotFrequency, plotXY, plotCounter, plotFrequency
import statsmodels.distributions as sm
import numpy as np
from nltk.tokenize.punkt import PunktWordTokenizer
#from nltk import word_tokenize, wordpunct_tokenize

####TODO: think about percentages instead of numbers. It means X / total of queries are of size Y....change it along the code!

PATH_TO_AUX_FILES = "auxFiles/"

def calculateMetrics(dataList, removeStopWords=True, printPlotSizeOfWords=True, printPlotSizeOfQueries=True,\
                     printPlotFrequencyOfQueries=True, printPlotFrequencyOfTerms=True, printPlotAcronymFrequency=True,\
                     printQueriesPerSession=True, printTimePerSession=True):
    """
        Expected a list of list of DataSet (TripData or AolData) objects
    """
    
    countingAcronymsList = []
    countingTimePerSessionList = []
    countingTokensList = []
    countingQueriesList = []
    countingQueriesPerSessionList = []

    for dataPair in dataList:
        
        data, dataName = dataPair[0], dataPair[1]

        data = tokenizeAllData(data)
    
        if removeStopWords:
            data = filterStopWords(data)

        percentageAcronym, countingAcronyms = calculateAcronyms(data)
        maxValue, minValue, meanValue, medianValue, countingTokens, coOccurrenceList, greatestQuery, countingQueries= calculateTerms(data)
        #numExpasions, numExtractions, numReformulations = calculateExpansionShrinkageReformulations(data)
        numSessions, countingQueriesPerSession, maxNumQueries, minNumQueries, meanNumQueries, medianNumQueries,\
                countingTimePerSession, maxTime, minTime, meanTime, medianTime,\
                numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions = calculateQueriesPerSession(data)

        # Print statistics
        with open(dataName + ".result", "w") as f:
            f.write("Metrics calculated:\n")
            printMetricsForTerms(f, maxValue, minValue, meanValue, medianValue, countingTokens, coOccurrenceList,\
                                 percentageAcronym, countingAcronyms, countingQueries, greatestQuery)
            printMetricsForSessions(f, numSessions, maxNumQueries, minNumQueries, meanNumQueries, medianNumQueries,\
                                    maxTime, minTime, meanTime, medianTime, numberOfExpansions, numberOfShrinkage,\
                                    numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions)

        countingAcronymsList.append(countingAcronyms)
        countingTimePerSessionList.append(countingTimePerSession)
        countingTokensList.append(countingTokens)
        countingQueriesList.append(countingQueries)
        countingQueriesPerSessionList.append(countingQueriesPerSession)

    if printQueriesPerSession:
        plotQueriesPerSession(countingQueriesPerSessionList)
    if printPlotFrequencyOfTerms:
        plotFrequencyOfTerms(countingTokensList)
    if printPlotFrequencyOfQueries:
        plotFrequencyOfQueries(countingQueriesList)
    if printTimePerSession:
        plotTimePerSession(countingTimePerSessionList)
    if printPlotAcronymFrequency:
        plotAcronymFrequency(countingAcronymsList)
    if printPlotSizeOfWords:
           plotSizeOfWords(dataList)
    if printPlotSizeOfQueries:
        plotSizeOfQueries(dataList)

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

def plotCoutingTimePerSessionListAcc(countingTimePerSessionList):
    
    for countingTimePerSession in countingTimePerSessionList[:-1]:

        ecdf = sm.ECDF( list(countingTimePerSession.elements()) )
        x = np.linspace(min(countingTimePerSession.keys()), max(countingTimePerSession.keys()))
        y = ecdf(x)
        plotXY(x, y, ylabelName="Frequency", xlabelName="Acc Time Per Session", showIt=False, lastOne=False)
    
    countingTimePerSession = countingTimePerSessionList[-1]
    ecdf = sm.ECDF( list(countingTimePerSession.elements()) )
    x = np.linspace(min(countingTimePerSession.keys()), max(countingTimePerSession.keys()))
    y = ecdf(x)
    plotXY(x, y, ylabelName="Frequency", xlabelName="Acc Time Per Session", saveName = "accTimePerSession.png", showIt=False, lastOne=True)

def plotTimePerSession(countingTimePerSessionList):
    
    plotCoutingTimePerSessionListAcc(countingTimePerSessionList)
    
    for countingTimePerSession in countingTimePerSessionList[:-1]:
        plotCounter(countingTimePerSession, ylabelName="Frequency", xlabelName="Time Per Session (Seconds)", showIt=False, lastOne=False)

    countingTimePerSession = countingTimePerSessionList[-1]
    plotCounter(countingTimePerSession, ylabelName="Frequency", xlabelName="Time Per Session (Seconds)", \
                saveName = "timePerSession.png", showIt=False, lastOne=True)


def plotQueriesPerSession(countingQueriesPerSessionList):

    for countingQueriesPerSession in countingQueriesPerSessionList[:-1]:
        plotCounter(countingQueriesPerSession, xlabelName="Queries Per Session", ylabelName="Frequency", showIt=False, lastOne=False)
    
    countingQueriesPerSession = countingQueriesPerSessionList[-1]
    plotCounter(countingQueriesPerSession, xlabelName="Queries Per Session", ylabelName="Frequency", saveName="queriesPerSession.png", showIt=False, lastOne=True)

def plotAcronymFrequency(countingAcronymsList):
    
    for countingAcronyms in countingAcronymsList[:-1]:
        plotFrequency(countingAcronyms.values(), "Acronyms Repetition", showIt=False, lastOne=False)
    
    countingAcronyms = countingAcronymsList[-1]
    plotFrequency(countingAcronyms.values(), "Acronyms Repetition", saveName = "acronymFreq.png", showIt=False, lastOne=True)

def plotFrequencyOfQueries(countingQueriesList):
    
    for countingQueries in countingQueriesList[:-1]:
        plotFrequency(countingQueries.values(), "Query Repetition", showIt=False, lastOne=False)

    countingQueries = countingQueriesList[-1]
    plotFrequency(countingQueries.values(), "Query Repetition", saveName = "queriesFreq.png", showIt=False, lastOne=True)

def plotFrequencyOfTerms(countingTokensList):

    for countingTokens in countingTokensList[:-1]:
        plotFrequency(countingTokens.values(), "Term Repetition", showIt=False, lastOne=False)
    
    countingTokens = countingTokensList[-1]
    plotFrequency(countingTokens.values(), "Term Repetition", saveName = "termFreq.png", showIt=False, lastOne=True)

def plotSizeOfQueries(dataList):
    
    queriesSize = []
    for dataItem in dataList[:-1]:
        data = dataItem[0]
        queriesSize = [ len(member.keywords) for member in data ] 
        plotFrequency(queriesSize, "Query Size", showIt=False, lastOne=False)

    data = dataList[-1][0]
    queriesSize = [ len(member.keywords) for member in data ] 
    plotFrequency(queriesSize, "Query Size", saveName = "queriesSize.png", showIt=False, lastOne=True)

## TODO: remove later
#def plotSizeOfQueries(data):
#    queriesSize = []
#    queriesSize = [ len(member.keywords) for member in data ]
#    plotFrequency(queriesSize, "Query Size", saveName = "queriesSize.png", showIt=False)

def plotSizeOfWords(dataList):
    
    wordsSize = []
    for dataItem in dataList[:-1]:
        data = dataItem[0]
        wordsSize = [ len(word) for member in data for word in member.keywords]
        plotFrequency(wordsSize, "Word Size", showIt=False, lastOne=False)

    wordsSize = [ len(word) for member in dataList[-1][0] for word in member.keywords]
    plotFrequency(wordsSize, "Word Size", saveName = "wordSize.png", showIt=False, lastOne=True)

#TODO: remove later
#def plotSizeOfWords(data):
#    wordsSize = []
#    for member in data:
#        wordsSize += [ len(word) for word in member.keywords ]
#    plotFrequency(wordsSize, "Word Size", saveName = "wordSize.png", showIt=False)

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
    if set1 > set2:
        return 0,1,0,0
    if set1 < set2:
        return 1,0,0,0
    else: 
        return 0,0,1,0
    

def calculateExpansionShrinkageReformulations(sessions):
    
    numberOfExpansions = 0
    numberOfShrinkage = 0
    numberOfReformulations = 0
    numberOfRepetitions = 0
    # TODO: if I remove the ''keep dimmension'', the number of dimmensions would be only 3 -> 2**3 -> 8
    vectorOfModifiedSessions = [0]*16

    for session in sessions.values():
        for subSession in session.values():
            
            modifiedSubSession = False
            previousQuery = subSession[0]
            for query in subSession[1:]:
                e, s, ref, rep = compareSets( set(previousQuery[1]), set(query[1]))
                numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions =\
                        e + numberOfExpansions, s + numberOfShrinkage, ref + numberOfReformulations, rep + numberOfRepetitions
                previousQuery = query
                
                #TODO: modified should be only when they are actually modified...
                modifiedSubSession = True
        
            if modifiedSubSession:
                indexVal = int( str(e) + str(s) + str(ref) + str(rep), 2)
                vectorOfModifiedSessions[indexVal] += 1


    return numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions

def calculateQueriesPerSession(data):
    '''
        I am considering all sessions here. An alternative option would be to consider only the sessions with more that X queries. (e.g. X > 3)
    '''
    sessions = defaultdict(dict)

    for member in data:

        # There are no previous keywords and no sessions of this id -> create the first one sessions[id][1] = list
        if member.previouskeywords is None and not sessions[member.sessionid]:
            sessions[member.sessionid][1] = [[member.datatime, member.keywords]]

        # There are no previous keywords and there is at least one sessions of this id 
        elif member.previouskeywords is None and sessions[member.sessionid]:
            sessions[member.sessionid][ len(sessions[member.sessionid]) + 1 ] = [[member.datatime, member.keywords]]
        
        elif member.previouskeywords is not None and not sessions[member.sessionid]:
            # This situation should not happen, but it does. It means that a session was not created but there were previous keywords.
            #print "ERROR!"
            #print member.sessionid, member.datatime, member.keywords, "previous ---> ", member.previouskeywords
            sessions[member.sessionid][1] = [[member.datatime, member.keywords]]

        # There are previous keywords!
        else:
            sessions[member.sessionid][ len(sessions[member.sessionid]) ] += [[member.datatime,member.keywords]]

    #for session, date in sessions.iteritems():
    #    print session, date

    numSessions = sum( len(s) for s in sessions.values() )
    queriesPerSession = [ len(q) for session in sessions.values() for q in session.values() ]
    sessionsWithMoreThanOneQuery = len([ 1 for session in sessions.values() for q in session.values() if len(q) > 1 ])
    countingQueriesPerSession = Counter(queriesPerSession)

    allSessions = [ span for session in sessions.values() for span in session.values() ]
    timeSpansInSeconds = [ (max(span[-1][0],span[0][0]) - min(span[-1][0],span[0][0])).total_seconds() for span in allSessions]
    countingTimePerSession = Counter(timeSpansInSeconds)

    # Basic statistics for queries inside sessions
    maxNumQueries = max(queriesPerSession)
    minNumQueries = min(queriesPerSession)
    meanNumQueries = sum(queriesPerSession) / len(queriesPerSession)
    medianNumQueries = sorted(queriesPerSession)[len(queriesPerSession)//2]
    
    # Basic statistics for the time spend in each session (metric used is seconds) 
    maxTime = max(timeSpansInSeconds)
    minTime = min(timeSpansInSeconds) 
    meanTime = sum(timeSpansInSeconds) / len(timeSpansInSeconds)
    medianTime = sorted(timeSpansInSeconds)[len(timeSpansInSeconds)//2]
   
    #calculate extra metrics for sessions
    numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions,\
            vectorOfModifiedSessions = calculateExpansionShrinkageReformulations(sessions)
    modifiedQueries = numberOfExpansions + numberOfShrinkage + numberOfReformulations + numberOfRepetitions 
    # The number of sessions with more that 2 queries HAVE to be the same that the number of modified session
    print sum(vectorOfModifiedSessions),sessionsWithMoreThanOneQuery
    assert sum(vectorOfModifiedSessions) == sessionsWithMoreThanOneQuery
    

    #print numSessions, maxNumQueries, minNumQueries, meanNumQueries, medianNumQueries, maxTime, minTime, meanTime, medianTime
    return numSessions, countingQueriesPerSession, maxNumQueries, minNumQueries, meanNumQueries, medianNumQueries,\
            countingTimePerSession, maxTime, minTime, meanTime, medianTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions,\
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

    
    allQueries = [ ' '.join(member.keywords) for member in data ]
    countingQueries = Counter(allQueries)
    
    # separate the information about the queries from the rest of the data
    listOfQueries = [ member.keywords for member in data ]
    #print "list = ", listOfQueries 
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
    avg = sum(queryInNumbers) / len(queryInNumbers)
    median = sorted(queryInNumbers)[len(queryInNumbers)//2]
    max_ = max(queryInNumbers)
    min_ = min(queryInNumbers)
    
    return max_, min_, avg, median, countingTokens, coOccurrenceList, greatestQuery, countingQueries


def printMetricsForTerms(writer, maxValue, minValue, meanValue, medianValue, countingTokens, coOccurrenceList, percentageAcronym, countingAcronyms, countingQueries, greatestQuery):
    
    writer.write("-" * 80 + "\n")
    writer.write("-" * 45 + "\n")
    writer.write("For TERMS:\n")
    writer.write("-" * 45 + "\n")
    
    table = {'Number Of Types': len(countingTokens), 'Number Of Terms': sum(countingTokens.values()),\
             'Relation Type/Terms': sum(countingTokens.values()) / len(countingTokens),\
             'Greatest Query': ' '.join(greatestQuery),\
             'Max. number of Terms in a query': maxValue,\
             'Min. number of Terms in a query': minValue,\
             'Mean number of Terms in a query': meanValue,\
             'Median number of Terms in a query': medianValue,\
             'Percentage of Acronyms used': percentageAcronym
            }

    for name, value in table.items():
        writer.write('{0:45} ==> {1:30}\n'.format(name, value))

    writer.write("-" * 45 + "\n")
    writer.write("10 Most Common Terms:\n")
    
    writer.write("-" * 45 + "\n")
    for pair in countingTokens.most_common(10):
        writer.write('{0:45} ==> {1:30}\n'.format(pair[0], str(pair[1])))
    writer.write("-" * 45 + "\n")
     
    writer.write("10 Most Common Queries:\n")
    writer.write("-" * 45 + "\n")
    for pair in countingQueries.most_common(10):
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


def printMetricsForSessions(writer,numSessions, maxNumQueries, minNumQueries, meanNumQueries, medianNumQueries, maxTime, minTime, meanTime, medianTime, numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions, vectorOfModifiedSessions):

    writer.write("-" * 80 + "\n")
    writer.write("-" * 40 + "\n")
    writer.write("For QUERIES:\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Sessions", str(numSessions)))
    writer.write("-" * 40 + "\n")
    writer.write("Session Length in Queries\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Maximum number of Queries in a session", str(maxNumQueries)))
    writer.write('{0:45} ==> {1:30}\n'.format("Minimum number of Queries in a session", str(minNumQueries)))
    writer.write('{0:45} ==> {1:30}\n'.format("Mean number of Queries in a session", str(meanNumQueries)))
    writer.write('{0:45} ==> {1:30}\n'.format("Median number of Queries in a session", str(medianNumQueries)))
    writer.write("-" * 40 + "\n")
    writer.write("Session Length in Time\n")
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Maximum duration of a session", str(maxTime)))
    writer.write('{0:45} ==> {1:30}\n'.format("Minimum duration of a session", str(minTime)))
    writer.write('{0:45} ==> {1:30}\n'.format("Mean duration of a session", str(meanTime)))
    writer.write('{0:45} ==> {1:30}\n'.format("Median duration of a session", str(medianTime)))
    writer.write("-" * 40 + "\n")
    writer.write('{0:45} ==> {1:30}\n'.format("Vector Of Modified Session ", str(vectorOfModifiedSessions)))
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Modified Session ", str(sum(vectorOfModifiedSessions))))
    writer.write('{0:45} ==> {1:30}\n'.format("Percentage of Modified Session ", str(sum(vectorOfModifiedSessions)/numSessions)))
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Modified Queries", str(numberOfExpansions + numberOfShrinkage + numberOfReformulations + numberOfRepetitions)))
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Expansions", str(numberOfExpansions)))    
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Shrinkages", str(numberOfShrinkage)))    
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Reformulations", str(numberOfReformulations)))    
    writer.write('{0:45} ==> {1:30}\n'.format("Number of Repetitions", str(numberOfRepetitions)))    
    writer.write("-" * 40 + "\n")
    writer.write("\n")

