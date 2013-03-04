
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner
from statistics import calculateMetrics

PATH_TO_DATASETS = "dataSets/"

if __name__ == "__main__":

    trip = readTripDataSet(PATH_TO_DATASETS + "tripTest2.csv")
    aol = readAolDataSet(PATH_TO_DATASETS + "aolSmall.csv")
    hon = readHONDataSet(PATH_TO_DATASETS + "honSmall.csv")
    #aolNotHealth = readAolDataSet(PATH_TO_DATASETS + "aolNotHealthsitesSmall.csv")
    #goldminer = readGoldMiner(PATH_TO_DATASETS + "goldminer-v4.txt")
    
    
    #trip = readTripDataSet(PATH_TO_DATASETS + "triplogs1yrMine.gz")
    #aol = readAolDataSet(PATH_TO_DATASETS + "aolHealthSites.csv")
    #hon = readAolDataSet(PATH_TO_DATASETS + "honAll.csv")
    
    
    calculateMetrics([ [aol, "Aol"], [ trip, "Trip"], [hon, "HoN" ] ]) 
    #calculateMetrics([ [hon, "honTest"] ] ) 
    #calculateMetrics([ [aol, "Aol"] ] ) 
    #calculateMetrics([ [aolNotHealth, "~aol"] ] ) 
    #calculateMetrics([ [goldminer, "goldMinerTest"] ] ) 

