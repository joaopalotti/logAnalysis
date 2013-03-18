
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat
from statistics import calculateMetrics
import gzip

PATH_TO_DATASETS = "dataSets/"

if __name__ == "__main__":

    #goldMiner = readMyFormat(PATH_TO_DATASETS + "goldMiner.output")
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
    #calculateMetrics([ [goldMiner, "goldMiner"], [hon, "Hon"] ]) 
    #calculateMetrics([ [goldMiner, "goldMiner"] ]) 

