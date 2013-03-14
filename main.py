
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat
from statistics import calculateMetrics
import gzip

PATH_TO_DATASETS = "dataSets/"

def convertFile(filename, filetype, outputname=None, gzipIt=True):
    if not outputname:
        outputname = PATH_TO_DATASETS + filename + ".dataset"
    else:
        outputname = PATH_TO_DATASETS + outputname
    
    if filetype is "trip":
        tmp = readTripDataSet(filename)
    elif filetype is "aol":
        tmp = readAolDataSet(filename)
    elif filetype is "hon":
        tmp = readHONDataSet(filename)
    elif filetype is "goldminer":
        tmp = readGoldMiner(filename)
    
        
    if gzipIt:
        print "Creating file ", outputname + ".gz"
        f = gzip.open( outputname + ".gz", "wb")
    else:
        print "Creating file ", outputname
        f = open( outputname, "w")

    for line in tmp:
        line.printMe(f)
    f.close()
    

if __name__ == "__main__":

    #convertFile(PATH_TO_DATASETS + "tripTest4.csv", "trip", "tripSmall.dataset",gzipIt=False)

    hon = readMyFormat(PATH_TO_DATASETS + "honEnglishResult.v3.dataset")
    #calculateMetrics([ [test, "test"],[test2, "test2" ]] ) 
    
    #trip = readTripDataSet(PATH_TO_DATASETS + "tripTest4.csv")
    #aol = readHONDataSet(PATH_TO_DATASETS + "honSmall2.csv")
    #hon = readHONDataSet(PATH_TO_DATASETS + "honSmall.csv")
    #aolNotHealth = readAolDataSet(PATH_TO_DATASETS + "aolNotHealthsitesSmall.csv")
    #goldminer = readGoldMiner(PATH_TO_DATASETS + "goldminer-v4.txt")
    
    #calculateMetrics([ [aol, "Aol"], [ trip, "Trip"], [hon, "HoN" ] ]) 
    #calculateMetrics([ [trip, "Trip"] ] ) 
    calculateMetrics([ [hon, "Hon"] ] ) 
    #calculateMetrics([ [hon, "Hon"], [trip, "Trip"] ] ) 
    #calculateMetrics([ [aol, "Aol"] ] ) 
    #calculateMetrics([ [aolNotHealth, "~aol"] ] ) 
    #calculateMetrics([ [goldminer, "goldMinerTest"] ] ) 

