
from readCSV import readTripDataSet, readAolDataSet
from statistics import calculateMetrics

PATH_TO_DATASETS = "dataSets/"

if __name__ == "__main__":

    #trip = readTripDataSet(PATH_TO_DATASETS + "tripTest2.csv")
    #trip = readTripDataSet(PATH_TO_DATASETS + "triplogs1yrMine.gz")
    #aol = readAolDataSet(PATH_TO_DATASETS + "aolHealthSites.csv")
    aol = readAolDataSet(PATH_TO_DATASETS + "aolSmall.csv")
    
    #calculateMetrics([ [aol,"aol"], [trip,"trip"] ] ) 
    calculateMetrics([ [aol, "aolTest"] ] ) 
