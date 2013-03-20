
def plotCountingTimePerSessionListAcc(myPlotter, countingTimePerSessionList, printValuesToFile):
    
    import statsmodels.distributions as sm
    import numpy as np

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
        myPlotter.plotCounter(countingQueriesPerSession, label=dataName, xlabelName="Queries Per Session", ylabelName="Frequency", showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesPerSession", xEndRange=20)
    
    countingQueriesPerSessionPair = countingQueriesPerSessionList[-1]
    dataName, countingQueriesPerSession = countingQueriesPerSessionPair[0], countingQueriesPerSessionPair[1]
    myPlotter.plotCounter(countingQueriesPerSession, label=dataName, xlabelName="Queries Per Session", ylabelName="Frequency", saveName="queriesPerSession", showIt=False, lastOne=True, printValuesToFile=printValuesToFile, xEndRange=20)

def plotAcronymFrequency(myPlotter, countingAcronymsList, printValuesToFile):
    
    for countingAcronymsPair in countingAcronymsList[:-1]:
        dataName, countingAcronyms = countingAcronymsPair[0], countingAcronymsPair[1]
        myPlotter.plotFrequency(countingAcronyms.values(), "Acronyms Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="acronymFreq")
    
    countingAcronymsPair = countingAcronymsList[-1]
    dataName, countingAcronyms = countingAcronymsPair[0], countingAcronymsPair[1]
    myPlotter.plotFrequency(countingAcronyms.values(), "Acronyms Repetition", label=dataName, saveName="acronymFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotLogLogFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile):
    for countingQueriesPair in countingQueriesList[:-1]:
        dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
        myPlotter.plotLogLogFrequency(countingQueries.values(), "Query Frequency (log)", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesLogLogFreq")

    countingQueriesPair = countingQueriesList[-1]
    dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
    myPlotter.plotLogLogFrequency(countingQueries.values(), "Query Frequency (log)", label=dataName, saveName="queriesLogLogFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)


def plotFrequencyOfQueries(myPlotter, countingQueriesList, printValuesToFile):
    for countingQueriesPair in countingQueriesList[:-1]:
        dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
        myPlotter.plotFrequency(countingQueries.values(), "Query Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesFreq")

    countingQueriesPair = countingQueriesList[-1]
    dataName, countingQueries = countingQueriesPair[0], countingQueriesPair[1]
    myPlotter.plotFrequency(countingQueries.values(), "Query Repetition", label=dataName, saveName="queriesFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotLogLogFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile):
    for countingTokensPair in countingTokensList[:-1]:
        dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
        myPlotter.plotLogLogFrequency(countingTokens.values(), "Term Repetition (log)", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="termLogLogFreq")
    
    countingTokensPair = countingTokensList[-1]
    dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
    myPlotter.plotLogLogFrequency(countingTokens.values(), "Term Repetition (log)", label=dataName, saveName="termLogLogFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)


def plotFrequencyOfTerms(myPlotter, countingTokensList, printValuesToFile):
    for countingTokensPair in countingTokensList[:-1]:
        dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
        myPlotter.plotFrequency(countingTokens.values(), "Term Repetition", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="termFreq")
    
    countingTokensPair = countingTokensList[-1]
    dataName, countingTokens = countingTokensPair[0], countingTokensPair[1]
    myPlotter.plotFrequency(countingTokens.values(), "Term Repetition", label=dataName, saveName="termFreq", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)

def plotSizeOfQueries(myPlotter, dataList, printValuesToFile):
    plotSizeOfQueriesAbsolute(myPlotter, dataList, printValuesToFile)
    plotSizeOfQueriesRelative(myPlotter, dataList, printValuesToFile)

def plotSizeOfQueriesAbsolute(myPlotter, dataList, printValuesToFile):
    queriesSize = []
    for dataItem in dataList[:-1]:
        data, dataName = dataItem[0], dataItem[1]
        queriesSize = [ len(member.keywords) for member in data ] 
        myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesSize")

    data, dataName = dataList[-1][0], dataList[-1][1]
    queriesSize = [ len(member.keywords) for member in data ] 
    myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, saveName="queriesSize", showIt=False, lastOne=True, relative=False, printValuesToFile=printValuesToFile)

def plotSizeOfQueriesRelative(myPlotter, dataList, printValuesToFile):

    queriesSize = []
    for dataItem in dataList[:-1]:
        data, dataName = dataItem[0], dataItem[1]
        queriesSize = [ len(member.keywords) for member in data ] 
        myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="queriesSizeRelative")

    data, dataName = dataList[-1][0], dataList[-1][1]
    queriesSize = [ len(member.keywords) for member in data ] 
    myPlotter.plotFrequency(queriesSize, "Query Size", label=dataName, saveName="queriesSizeRelative", showIt=False, lastOne=True, relative=True, printValuesToFile=printValuesToFile)

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

def plotMeshDepth(myPlotter, dataList, printValuesToFile):
    
    for dataItem in dataList[:-1]:
        dataName, data = dataItem[0], dataItem[1]
        myPlotter.plotCounter(data, xlabelName="Mesh Depth", ylabelName="Occurences", label=dataName, showIt=False, lastOne=False, printValuesToFile=printValuesToFile, saveName="meshDepth")

    dataName, data = dataList[-1]
    myPlotter.plotCounter(data, xlabelName="Mesh Depth", ylabelName="Occurences", label=dataName, saveName="meshDepth", showIt=False, lastOne=True, printValuesToFile=printValuesToFile)


