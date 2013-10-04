from __future__ import division
import sys, csv

f = sys.argv[1]

popularNames = set()
chv = set()
umls = set()
onlyCHV = set()
onlyUMLS = set()
none = set()
misspelling = set()
minus1Score = 0
zeroScore = 0
oneScore = 0
sumScore = 0
totalLines = 0

with open(f, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        totalLines += 1
        print row
        popularNames.add(row[1])
        #print "Concept=%s" % row[1]
        if row[5] == "yes":
            chv.add(row[1])
        if row[6] == "yes":
            umls.add(row[1])
        if row[5] == "yes" and row[6] == "no":
            onlyCHV.add(row[1])
        if row[5] == "no" and row[6] == "yes":
            onlyUMLS.add(row[1])
        if row[5] == "no" and row[6] == "no":
            none.add(row[1])
        if row[7] == "yes":
            misspelling.add(row[1])
        if row[11] == "\\N":
            row[11] = -1
        if row[11] == "-1":
            minus1Score += 1
        elif row[11] == "0":
            zeroScore += 1
        elif row[11] == "1":
            oneScore += 1
        else:
            sumScore += float(row[11])


print "Size popular names => ", len(popularNames)
print "chv => ", len(chv)
print "chv only => ", len(onlyCHV)
print "umls => ", len(umls)
print "umls only => ", len(onlyUMLS)
print "misspelling => ", len(misspelling)
print "same chv and umls => ", len( chv & umls)

print "total lines => ", totalLines
print "Zero score => ", zeroScore
print "Zero score percentage => ", zeroScore / totalLines
print "minus1Score => ", minus1Score
print "minus1Score percentage =>", minus1Score / totalLines
print "oneScore => ", oneScore
print "onecore percentage =>", oneScore / totalLines
print "sumScore => ", sumScore
print "sumScore + oneScore => ", sumScore + oneScore
print "meanScore => ", (sumScore + oneScore) / totalLines



