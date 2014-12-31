from readCSV import checkSession, readMyFormat
from time import time
import gzip, csv, sys, re

def areBadKeyWords(keywords, level=0):
    if level == 0:
        return keywords == None or len(keywords) == 0
        
    if level == 1:
        return keywords == None or len(keywords) == 0 or keywords in ['-']
        
    if level == 2:
        return keywords == None or len(keywords) == 0 or keywords in ['-', "yahoo", "yahoo.com", "www.mapquest.com", "map quest", "free download", "free downloads", "jobs", "internet", "sex", "eva longoria", "y", "n", "a", "ask", "dogs", "buddy list", "penis", "names", "tattoos", "w", "baby names", "pottery barn", "shoes", "shoes", "cats", "my account", "horses", "89.com", "chat rooms", "oprah.com", "dogs"]
    
    if level == 3:
        return keywords == None or len(keywords) == 0 or keywords in ['-', "yahoo", "yahoo.com", "www.mapquest.com", "map quest", "free download", "free downloads", "horoscopes", "jobs", "internet", "sex", "eva longoria", "y", "n", "a", "ask", "dogs", "buddy list", "penis", "names", "tattoos", "w", "baby names", "pottery barn", "shoes", "shoes", "cats", "my account", "hair styles", "horses", "89.com", "chat rooms", "oprah.com", "dogs", "hairstlyes"]

    if level >= 4:
        print "LEVEL DOESNT EXIST! Please use a level smaller than 4"
        sys.exit(0)

def readIn(filename, fileVersion, verbose=True): 

    if verbose:
        print ("Reading information of file already transformed into MY FORMAT! Filename: ", filename)

    #data already sorted
    #data = readMyFormat(filename, fileVersion, verbose)
    data = readMyFormat(filename, verbose)

    return data

def checkSessionAndFilterContent(data, outFileName, filterLevel, verbose=True):
    
    start = time()

    removedLines = 0
    previousRow = data[0]
    lastGoodPreviousRow = 1
    outFile = open(outFileName, "w")

    if not areBadKeyWords(previousRow.keywords, filterLevel):
        previousRow.previouskeywords = None
        previousRow.printMe(outFile)
    
    else:
        while areBadKeyWords(previousRow.keywords, filterLevel):
            removedLines += 1
            previousRow = data[lastGoodPreviousRow]
            lastGoodPreviousRow += 1    
        previousRow.previouskeywords = None
        previousRow.printMe(outFile)

    for row in data[lastGoodPreviousRow:]:
        #print row, len(row)
            
        #No keywords in this line, skip it
        if areBadKeyWords(row.keywords, filterLevel):
            removedLines += 1
            continue

        if checkSession(previousRow.vectorizeMe(), row.vectorizeMe(), idIndex=1, dateIndex=0, dateFormat='%Y-%m-%d %H:%M:%S'):
            row.previouskeywords = previousRow.keywords
            row.printMe(outFile)
        else:
            row.previouskeywords = None
            row.printMe(outFile)
       
        previousRow = row
    
    if verbose:
        print ("Number of removed lines: %d" % int(removedLines))
        print ("Data transformed in %.2f seconds" % float(time() - start))

if __name__ == "__main__":
    filename = sys.argv[1]
    filterLevel = int(sys.argv[2])
    fileVersion = "v5"
    verbose = True
    outFileName = filename + ".fixed"
    
    checkSessionAndFilterContent( readIn(filename, fileVersion, verbose=True), outFileName, filterLevel, verbose)

