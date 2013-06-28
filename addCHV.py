import sys, csv, re
from readCSV import readMyFormat
from auxiliarFunctions import tokenize

from scoop import futures

chvfile = sys.argv[1]
v4datasetFile = sys.argv[2]

popularNames = []

data = readMyFormat(v4datasetFile)
queries = []

for member in data:        
    query = tokenize(member.keywords)
    queries.append(query)

with open(chvfile, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        #print row
        popularNames += [tokenize(row[1])]


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
            return query
            #return True
    return None
    #return False

def findAllContains(query):
    result = []
    for p in popularNames:
        contains(p,query)
    return result

if __name__ == "__main__":
    
    found = []

        #print "Q = ", query
        #for popName in popularNames:
        #    if contains(popName, query):
        #        print "Found!"
        #        print "pop=%s, keywords=%s" % (popName, query)
        #        found.append(query)
    found = futures.map(findAllContains, queries)
    found = [f for f in found if f != None]

    print "Size popular names => ", len(popularNames)
    print "Size keywords => ", len(found)

