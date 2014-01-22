from __future__ import division
from readCSV import readMyFormat
from auxiliarFunctions import generateStatsVector
from collections import Counter
import sys, math

def analyseData(data):
    #for member in data:
    #    print member.CHVFound, member.hasCHV, member.hasUMLS, member.hasCHVMisspelled, member.comboScore

    #combo = [ round(member.comboScore, 3) for member in data if round(member.comboScore,3) != 0.290]
    combo = [ round(member.comboScore, 3) for member in data]
    npCombo = generateStatsVector(combo)
    countingCombo = Counter(combo)

    print "Combo Score: Mean - %.3f (+/- %.3f) Median - %.4f " % (npCombo.mean, npCombo.std, npCombo.median)
    return npCombo, countingCombo

def DCohen(mean1, mean2, std1, std2):
    return 1.0*(mean1 - mean2)/ math.sqrt( (std1 * std1 + std2 * std2)/2 )

def calculateDCohen(values, idx1, idx2):
    n1 = values[idx1]
    n2 = values[idx2]
    return DCohen(n1.mean, n2.mean, n1.std, n2.std)

values = []
#for file in sys.argv[1:]:
#    data = readMyFormat(file, "v5")
#    npCombo, countingCombo = analyseData(data)
#    for k, c in sorted(countingCombo.items(), key= lambda x:x[0]  ):
#       print "%f,%d" % (k, c)
    
#    values.append(npCombo)

file = sys.argv[1]
data = readMyFormat(file, "v5")
file = sys.argv[2]
data += readMyFormat(file, "v5")

file = sys.argv[3]
data2 = readMyFormat(file, "v5")
file = sys.argv[4]
data2 += readMyFormat(file, "v5")


npCombo, countingCombo = analyseData(data)
values.append(npCombo)

npCombo2, countingCombo = analyseData(data2)
values.append(npCombo2)

print "Cohen 1 and 2: ", calculateDCohen(values, 0, 1)
print "Cohen 2 and 1: ", calculateDCohen(values, 1, 0)


