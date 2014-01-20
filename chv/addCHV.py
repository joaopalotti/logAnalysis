from __future__ import division
import sys, csv, re
from readCSV import readMyFormat
from auxiliarFunctions import tokenize

"""
    Implementation decision:
        1) If combo value for the CHV entry is -1, I decided to substitute it for the mean combo value of all entries.
        2) When it is not found any CHV entry in the query, I assume that the combo value for that entry is the mean combo value (around 0.28)
"""

usingScoop = True
if usingScoop:
    from scoop import futures

chvfile = sys.argv[1]
v4datasetFile = sys.argv[2]
outfilename = sys.argv[3]

popularNames = []

data = readMyFormat(v4datasetFile, "v5")
queries = []

from collections import defaultdict
popCounter = defaultdict(int)

class CHV(object):
    def __init__(self, text, isCHV, isUMLS, misspelled, combo):
        self.text = text
        self.isCHV = isCHV
        self.isUMLS = isUMLS
        self.misspelled = misspelled
        self.comboScore = combo

for member in data:        
    query = tokenize(member.keywords)
    queries.append(query)

sumCombo = 0.0
with open(chvfile, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        #print row
        combo = float(row[11]) if row[11] != "\\N" else -1
        sumCombo += (combo if combo > 0 else 0)
        popularNames += [ CHV(text=tokenize(row[1]), isCHV=(row[5]=="yes"), isUMLS=(row[6]=="yes"), misspelled=(row[7]=="yes"), combo=combo)]

meanCombo = sumCombo / len(popularNames)
#print "Sum combo = ", sumCombo
#print "Mean combo value: ", meanCombo 
for chv in popularNames:
    if chv.comboScore == -1:
        chv.comboScore = meanCombo

#Two lists: Popular expression ["heart", "attack"] and query ["whatever", "it", "is"]
def contains(pop, query):

    lp, lq = len(pop), len(query)
    #Finds all the indices where pop[0] occurs
    startIndices = [i for i, x in enumerate(query) if x == pop[0]]

    for i in startIndices:
        found = True
        for j in range(1,lp):
            if i + j >= lq or pop[j] != query[i + j]:
                found = False
        if found:
            #print "Found!", pop, "in", query
            popCounter[''.join(pop)] += 1
            return True
    return False

def findAllContains(numberAndQuery, total):
    number, query = numberAndQuery
    percentage = number/total
    sys.stdout.write("\r%.3f" % percentage)
    sys.stdout.flush()
    return [p for p in popularNames if contains(p.text, query)]

if __name__ == "__main__":
    
    if usingScoop:
        originalFound = list(futures.map(findAllContains, zip(range(1, 1 + len(queries)),queries), len(queries) * [len(queries)]  ))
    else:
        originalFound = map(findAllContains, zip(range(1, 1 + len(queries)), queries), len(queries) * [len(queries)])

    found = [ f for f in originalFound if len(f) > 0]
    #iprint found

    print "Size popular names => ", len(popularNames)
    print "Number of queries containing CHV => ", len(found)
    bigTotal = sum( [len(f) for f in found] )
    print "Number of found CHV (more than one per query) => ", len(found)
 
    print "Mean number of CHV when it is found: ", sum( [len(f) for f in found] ) / len(found)

    print "Number of misspelled queries found: ", sum( [ 1 for l in found for f in l if f.misspelled == True ] ) / bigTotal
    print "Number of identical CHV: ", sum( [ 1 for l in found for f in l if f.isCHV == True ] ) / bigTotal
    print "Number of identical UMLS: ", sum( [ 1 for l in found for f in l if f.isUMLS == True ] ) / bigTotal
    print "Number of not CHV nor UMLS: ", sum( [ 1 for l in found for f in l if (f.isUMLS == False and f.isCHV == False) ] ) / bigTotal
    print "Number of CHV and NOT UMLS: ", sum( [ 1 for l in found for f in l if (f.isUMLS == False and f.isCHV == True) ] ) / bigTotal
    print "Number of UMLS and NOT CHV: ", sum( [ 1 for l in found for f in l if (f.isUMLS == True and f.isCHV == False) ] ) / bigTotal
    print "Number of UMLS and CHV: ", sum( [ 1 for l in found for f in l if (f.isUMLS == True and f.isCHV == True) ] ) / bigTotal

    print "Stats per query"
    print "Number of queries: ", len(queries)
    print "(query) Number of not CHV nor UMLS: ", sum( [ 1 for l in found for f in l if (f.isUMLS == False and f.isCHV == False) ] ) / len(query)
    print "(query) Number of CHV and NOT UMLS: ", sum( [ 1 for l in found for f in l if (f.isUMLS == False and f.isCHV == True) ] ) / len(query)
    print "(query) Number of UMLS and NOT CHV: ", sum( [ 1 for l in found for f in l if (f.isUMLS == True and f.isCHV == False) ] ) / len(query)
    print "(query) Number of UMLS and CHV: ", sum( [ 1 for l in found for f in l if (f.isUMLS == True and f.isCHV == True) ] ) / len(query)


    print "Term and frequency"
    #for pop, c in sorted(popCounter.items(), key=lambda t: t[1], reverse=True):
    #    print pop,"->", c
    
    outf = open(outfilename, "w")
    writer = csv.writer(outf, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
    for member, found in zip(data, originalFound):        
        CHVFound = len(found)
        hasCHV = any( [f.isCHV for f in found] )
        hasUMLS = any( [f.isUMLS for f in found] )
        hasCHVMisspelled = any( [f.misspelled for f in found] )
        if CHVFound == 0:
            meanComboScore = meanCombo
        else:
            meanComboScore = sum(f.comboScore for f in found if f.comboScore != -1) / (1.0 * len(tokenize(member.keywords)))

        #print found
        #print member.userId, member.keywords, CHVFound, hasCHV, hasUMLS, hasCHVMisspelled, meanComboScore, len(tokenize(member.keywords))
        #print "keywords = ", member.keywords
        #print "Mean combo score = ", meanComboScore 
        mesh = ';'.join(member.mesh) if member.mesh else ''
        semanticTypes = ';'.join(member.semanticTypes) if member.semanticTypes else ''

        writer.writerow( [str(member.datetime), member.userId, member.keywords, member.previouskeywords, mesh, semanticTypes, CHVFound, hasCHV, hasUMLS, hasCHVMisspelled, meanComboScore])
    outf.close()
