
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat
from statistics import calculateMetrics
import gzip

PATH_TO_DATASETS = "dataSets/"

def convertFile(filename, filetype, outputname=None):
    if filetype is "trip":
        tmp = readTripDataSet(filename)
    elif filetype is "aol":
        tmp = readAolDataSet(filename)
    elif filetype is "hon":
        tmp = readHONDataSet(filename)
    elif filetype is "goldminer":
        tmp = readGoldMiner(filename)
    
    if outputname:
        f = gzip.open( PATH_TO_DATASETS + outputname + ".gz", "wb")
    else:
        f = gzip.open( PATH_TO_DATASETS + filename + ".dataset.gz", "wb")

    for line in tmp:
        line.printMe(f)
    f.close()
    

if __name__ == "__main__":

    #convertFile(PATH_TO_DATASETS + "tripTest2.csv", "trip", "tripSmall.dataset")
    #convertFile(PATH_TO_DATASETS + "aolHealthSites.csv", "aol", "aolHealthSites.dataset")

    #trip = readMyFormat(PATH_TO_DATASETS + "tripSmall.dataset.gz")
    
    #trip = readTripDataSet(PATH_TO_DATASETS + "tripTest3.csv")
    #aol = readAolDataSet(PATH_TO_DATASETS + "aolSmall.csv")
    hon = readHONDataSet(PATH_TO_DATASETS + "honSmall.csv")
    #aolNotHealth = readAolDataSet(PATH_TO_DATASETS + "aolNotHealthsitesSmall.csv")
    #goldminer = readGoldMiner(PATH_TO_DATASETS + "goldminer-v4.txt")
    
    #calculateMetrics([ [aol, "Aol"], [ trip, "Trip"], [hon, "HoN" ] ]) 
    #calculateMetrics([ [trip, "Trip"] ] ) 
    #calculateMetrics([ [aol, "Aol"] ] ) 
    calculateMetrics([ [hon, "Hon"] ] ) 
    #calculateMetrics([ [aolNotHealth, "~aol"] ] ) 
    #calculateMetrics([ [goldminer, "goldMinerTest"] ] ) 

