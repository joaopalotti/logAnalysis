import sys, csv

f = sys.argv[1]

popularNames = set()
chv = set()
umls = set()
onlyCHV = set()
onlyUMLS = set()
none = set()
misspelling = set()

with open(f, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        #print row
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


print "Size popular names => ", len(popularNames)
print "chv => ", len(chv)
print "chv only => ", len(onlyCHV)
print "umls => ", len(umls)
print "umls only => ", len(onlyUMLS)
print "misspelling => ", len(misspelling)
print "same chv and umls => ", len( chv & umls)

