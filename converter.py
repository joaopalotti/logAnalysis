
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoi
from statistics import calculateMetrics
import gzip, sys


def convertFile(filename, filetype, outputname=None, gzipIt=True):
    
    if filetype is "trip":
        tmp = readTripDataSet(filename)
    elif filetype is "aol":
        tmp = readAolDataSet(filename)
    elif filetype is "hon":
        tmp = readHONDataSet(filename)
    elif filetype is "goldminer":
        tmp = readGoldMiner(filename)
    elif filetype is "khr":
        tmp = readKhresmoi(filename)
    
    if gzipIt:
        print "Creating file ", outputname + ".gz"
        f = gzip.open( outputname + ".gz", "wb")
    else:
        print "Creating file ", outputname
        f = open( outputname, "w")

    for line in tmp:
        line.printMe(f)
        #line.normalPrint()
    f.close()
    

if __name__ == "__main__":

    pathToFile = sys.argv[1]
    print "Using file: " + pathToFile
    convertFile( pathToFile, "aol", "aolNotHealth_complete.dataset", gzipIt=True)
    #convertFile( pathToFile, "goldminer", "goldminer.dataset", gzipIt=False)
    #convertFile( pathToFile, "goldminer", "goldMiner.dataset", gzipIt=True)
    #convertFile( pathToFile, "hon", "hon.dataset", gzipIt=False)
    #convertFile( pathToFile, "trip", "trip.dataset", gzipIt=False)

