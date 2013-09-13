from auxiliarFunctions import preProcessData

def plotQueryRanking(myPlotter, countingQueryRankingList, printValuesToFile, plottingInstalled=True):
    for countingQueryRankingPair in countingQueryRankingList[:-1]:
        dataName, countingQueryRanking = countingQueryRankingPair[0], countingQueryRankingPair[1]
        myPlotter.plotCounter(countingQueryRanking, xlabelName="Query Ranking", ylabelName="Freq", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queryRanking", plottingInstalled=plottingInstalled)
    
    countingQueryRankingPair = countingQueryRankingList[-1]
    dataName, countingQueryRanking = countingQueryRankingPair[0], countingQueryRankingPair[1]
    myPlotter.plotCounter(countingQueryRanking, "Query Ranking", "Freq", label=dataName, saveName="queryRanking", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotCountingTimePerSessionListAcc(myPlotter, countingTimePerSessionList, printValuesToFile, plottingInstalled=True):
    
    import statsmodels.distributions as sm
    import numpy as np

    for countingTimePerSessionPair in countingTimePerSessionList[:-1]:
        dataName = countingTimePerSessionPair[0]
        countingTimePerSession = countingTimePerSessionPair[1]

        ecdf = sm.ECDF( list(countingTimePerSession.elements()) )
        x = np.linspace(min(countingTimePerSession.keys()), max(countingTimePerSession.keys()))
        y = ecdf(x)
        myPlotter.plotXY(x, y, label=dataName, ylabelName="Frequency", xlabelName="Acc Time Per Session", showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="accTimePerSession", plottingInstalled=plottingInstalled)
    
    dataName, countingTimePerSession = countingTimePerSessionList[-1][0], countingTimePerSessionList[-1][1]
    ecdf = sm.ECDF( list(countingTimePerSession.elements()) )
    x = np.linspace(min(countingTimePerSession.keys()), max(countingTimePerSession.keys()))
    y = ecdf(x)
    
    myPlotter.plotXY(x, y, label=dataName, ylabelName="Frequency", xlabelName="Acc Time Per Session", saveName="accTimePerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotTimePerSession(myPlotter, countingTimePerSessionList, printValuesToFile, plottingInstalled=True):
    
    plotCountingTimePerSessionListAcc(myPlotter, countingTimePerSessionList, printValuesToFile, plottingInstalled=plottingInstalled)
    
    for countingTimePerSessionPair in countingTimePerSessionList[:-1]:
        dataName, countingTimePerSession = countingTimePerSessionPair[0], countingTimePerSessionPair[1]
        myPlotter.plotCounter(countingTimePerSession, label=dataName, ylabelName="Frequency", xlabelName="Time Per Session (Seconds)", showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="timePerSession", plottingInstalled=plottingInstalled)

    countingTimePerSessionPair = countingTimePerSessionList[-1]
    dataName, countingTimePerSession = countingTimePerSessionPair[0], countingTimePerSessionPair[1]
    myPlotter.plotCounter(countingTimePerSession, label=dataName, ylabelName="Frequency", xlabelName="Time Per Session (Seconds)", \
                saveName="timePerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotQueriesPerSession(myPlotter, countingQueriesPerSessionList, printValuesToFile, plottingInstalled=True):

    for countingQueriesPerSessionPair in countingQueriesPerSessionList[:-1]:
        dataName, countingQueriesPerSession = countingQueriesPerSessionPair[0], countingQueriesPerSessionPair[1]
        myPlotter.plotCounter(countingQueriesPerSession, label=dataName, xlabelName="Queries Per Session", ylabelName="Frequency", showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesPerSession", xEndRange=20, plottingInstalled=plottingInstalled)
    
    countingQueriesPerSessionPair = countingQueriesPerSessionList[-1]
    dataName, countingQueriesPerSession = countingQueriesPerSessionPair[0], countingQueriesPerSessionPair[1]
    myPlotter.plotCounter(countingQueriesPerSession, label=dataName, xlabelName="Queries Per Session", ylabelName="Frequency", saveName="queriesPerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, xEndRange=20, plottingInstalled=plottingInstalled)

def plotAcronymFrequency(myPlotter, countingAcronymsList, printValuesToFile, plottingInstalled=True):
    
    for countingAcronymsPair in countingAcronymsList[:-1]:
        dataName, countingAcronyms = countingAcronymsPair[0], countingAcronymsPair[1]
        myPlotter.plotFrequency(countingAcronyms.values(), "Acronyms Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="acronymFreq", plottingInstalled=plottingInstalled)
    
    countingAcronymsPair = countingAcronymsList[-1]
    dataName, countingAcronyms = countingAcronymsPair[0], countingAcronymsPair[1]
    myPlotter.plotFrequency(countingAcronyms.values(), "Acronyms Repetition", label=dataName, saveName="acronymFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotLogLogFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile, plottingInstalled=True):
    for countingQueriesPair in countingQueriesList[:-1]:
        dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
        myPlotter.plotLogLogFrequency(countingQueries.values(), "Query Frequency (log)", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesLogLogFreq", plottingInstalled=plottingInstalled)

    countingQueriesPair = countingQueriesList[-1]
    dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
    myPlotter.plotLogLogFrequency(countingQueries.values(), "Query Frequency (log)", label=dataName, saveName="queriesLogLogFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile, plottingInstalled=True):
    for countingQueriesPair in countingQueriesList[:-1]:
        dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
        myPlotter.plotFrequency(countingQueries.values(), "Query Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesFreq", plottingInstalled=plottingInstalled)

    countingQueriesPair = countingQueriesList[-1]
    dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
    myPlotter.plotFrequency(countingQueries.values(), "Query Repetition", label=dataName, saveName="queriesFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotLogLogFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile, plottingInstalled=True):
    for countingTokensPair in countingTokensList[:-1]:
        dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
        myPlotter.plotLogLogFrequency(countingTokens.values(), "Term Repetition (log)", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="termLogLogFreq", plottingInstalled=plottingInstalled)
    
    countingTokensPair = countingTokensList[-1]
    dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
    myPlotter.plotLogLogFrequency(countingTokens.values(), "Term Repetition (log)", label=dataName, saveName="termLogLogFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile, plottingInstalled=True):
    for countingTokensPair in countingTokensList[:-1]:
        dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
        myPlotter.plotFrequency(countingTokens.values(), "Term Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="termFreq", plottingInstalled=plottingInstalled)
    
    countingTokensPair = countingTokensList[-1]
    dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
    myPlotter.plotFrequency(countingTokens.values(), "Term Repetition", label=dataName, saveName="termFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotSizeOfQueries(myPlotter, queryInNumbers, printValuesToFile, plottingInstalled=True):
    plotSizeOfQueriesAbsolute(myPlotter, queryInNumbers, printValuesToFile, plottingInstalled=plottingInstalled)
    plotSizeOfQueriesRelative(myPlotter, queryInNumbers, printValuesToFile, plottingInstalled=plottingInstalled)

def plotSizeOfQueriesAbsolute(myPlotter, queryInNumbers, printValuesToFile, plottingInstalled=True):
    queriesSize = []
    for dataItem in queryInNumbers[:-1]:
        dataName, queriesSize = dataItem[0], dataItem[1]
        myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesSize", plottingInstalled=plottingInstalled)

    dataName, queriesSize = queryInNumbers[-1][0], queryInNumbers[-1][1]
    myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, saveName="queriesSize", showIt=False, lastOne=True, relative=False, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotSizeOfQueriesRelative(myPlotter, queryInNumbers, printValuesToFile, plottingInstalled=True):

    queriesSize = []
    for dataItem in queryInNumbers[:-1]:
        dataName, queriesSize = dataItem[0], dataItem[1]
        myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesSizeRelative", plottingInstalled=plottingInstalled)

    dataName, queriesSize = queryInNumbers[-1][0], queryInNumbers[-1][1]
    myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, saveName="queriesSizeRelative", showIt=False, lastOne=True, relative=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotSizeOfWords(myPlotter, queryInCharsList, printValuesToFile, plottingInstalled=True):
    
    for dataItem in queryInCharsList[:-1]:
        dataName, wordSize = dataItem[0], dataItem[1]
        myPlotter.plotFrequency(wordSize, "Word Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="wordSize", plottingInstalled=plottingInstalled)

    dataName, wordSize = queryInCharsList[-1][0], queryInCharsList[-1][1]
    myPlotter.plotFrequency(wordSize, "Word Size", label=dataName, saveName="wordSize", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotMeshDepth(myPlotter, dataList, printValuesToFile, plottingInstalled=True):
    for dataItem in dataList[:-1]:
        dataName, data = dataItem[0], dataItem[1]
        myPlotter.plotCounter(data, xlabelName="Mesh Depth", ylabelName="Occurences", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="meshDepth", plottingInstalled=plottingInstalled)

    dataName, data = dataList[-1]
    myPlotter.plotCounter(data, xlabelName="Mesh Depth", ylabelName="Occurences", label=dataName, saveName="meshDepth", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

def plotUsersByNumberOfQueries(myPlotter, dataList, printValuesToFile, plottingInstalled=True):
    for dataItem in dataList[:-1]:
        dataName, data = dataItem[0], dataItem[1]
        myPlotter.plotCounter(data, xlabelName="Number Of Queries", ylabelName="Number Of Users", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesPerUser", plottingInstalled=plottingInstalled)

    dataName, data = dataList[-1]
    myPlotter.plotCounter(data, xlabelName="Number of Queries", ylabelName="Number of Users", label=dataName, saveName="queriesPerUser", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, plottingInstalled=plottingInstalled)

