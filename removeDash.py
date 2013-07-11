from readCSV import checkSession, readMyFormat
from time import time
import gzip, csv, sys, re

filename = sys.argv[1]
version = "v5"
print "File used = ", filename

print ("Reading information of file already transformed into MY FORMAT! Filename: ", filename)
start = time()

#data already sorted
data = readMyFormat(filename, version)

outFile = open(filename + ".fixed", 'w')
#writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)

def areBadKeyWords(keywords):
    return keywords == None or len(keywords) == 0 or keywords in ['-', "yahoo", "yahoo.com", "www.mapquest.com", "map quest", "free download", "free downloads", "horoscopes", "jobs", "internet", "sex", "eva longoria", "y", "n", "a", "ask", "dogs", "buddy list", "penis", "names", "tattoos", "w", "baby names", "pottery barn", "shoes", "shoes", "cats", "my account", "hair styles", "horses", "89.com", "chat rooms", "oprah.com", "dogs", "hairstlyes"]

previousRow = data[0]
lastGoodPreviousRow = 1

if not areBadKeyWords(previousRow.keywords):
    print "Primeira linha eh boa!"
    previousRow.previouskeywords = None
    previousRow.printMe(outFile)
else:
    print "primeira linha eh ruim!"
    while areBadKeyWords(previousRow.keywords):
        previousRow = data[lastGoodPreviousRow]
        lastGoodPreviousRow += 1    
        print "testando linha ", lastGoodPreviousRow
    previousRow.previouskeywords = None
    previousRow.printMe(outFile)

for row in data[lastGoodPreviousRow:]:
    #print row, len(row)
        
    #No keywords in this line, skip it
    if areBadKeyWords(row.keywords):
        continue

    print "Row = ", row.vectorizeMe()
    print "Previous = ", previousRow.vectorizeMe()

    if checkSession(previousRow.vectorizeMe(), row.vectorizeMe(), idIndex=1, dateIndex=0, dateFormat='%Y-%m-%d %H:%M:%S'):
        row.previouskeywords = previousRow.keywords
        row.printMe(outFile)
    else:
        row.previouskeywords = None
        row.printMe(outFile)
   
    previousRow = row

print ("Data transformed in %.2f seconds" % float(time() - start))


