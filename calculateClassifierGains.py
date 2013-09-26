from __future__ import division

from collections import defaultdict
from auxiliarFunctions import generateStatsVector
import itertools as it
import sys, math
from scipy import stats

#### in file should be like:
# clf, Val1, Val2, Val3, Val4
# clf2, Val1, Val2, Val3, Val4
# clf, Val1, Val2, Val3, Val4
# ....etc

filename = sys.argv[1]

with open(filename, "r") as f:
    lines = f.readlines()


clfs = defaultdict(list)
means = defaultdict(list)
clfs2 = defaultdict(dict)
nMeasures = -1
k = -1

for l in lines:
    fields = l.strip().split(",")
    nMeasures = len(fields) - 1
    clfs[fields[0]].append(map(float,fields[1:]))

for classify, listOfValues in clfs.items():
    print classify, listOfValues
    k = len(listOfValues)

for classify, listOfValues in clfs.items():
    vs = defaultdict(list)
    for n in range(nMeasures):
        for values in listOfValues:
            vs[n].append(values[n])
    
    for n in range(nMeasures):
        clfs2[classify][n] = vs[n]
     
    for v in vs.values():
        npv = generateStatsVector(v)
        means[classify].append( (npv.mean, npv.std) )

# all the keys in pais (A,B), (A,C), (B,C)...
for clf in list(it.combinations(clfs.keys(), 2)):
    print "=== Comparing", clf[0], "and", clf[1], "==="

    for n in range(nMeasures):
        print "============"
        print "Measure ", n
        vec1 = clfs2[clf[0]][n]
        vec2 = clfs2[clf[1]][n]
        mean0 =  means[clf[0]][n][0]
        mean1 =  means[clf[1]][n][0]
        print "%s %.3f (%.3f) " % (clf[0], mean0, means[clf[0]][n][1])
        print "%s %.3f (%.3f) " % (clf[1], mean1, means[clf[1]][n][1])

        if mean0 > mean1:
            print "Mean %s > Mean %s: %.3f%s" % ( clf[0], clf[1], 100.0 * (mean0 - mean1) / mean1, "%")
        else:
            print "Mean %s > Mean %s: %.3f%s" % ( clf[1], clf[0], 100.0 * (mean1 - mean0) / mean0, "%")

        #http://projectile.sv.cmu.edu/research/public/talks/t-test.htm
        #http://easycalculation.com/statistics/t-distribution-critical-value-table.php
        t, p = stats.ttest_rel(vec1,vec2)
        print "p =>>", p
        print "100% - p = ", 1.0 - p
        if 1.0 - p >= 0.95:
            print "Different in 95% t-test"
        else:
            print "Equal in 95% t-test!"

        print "\n"


