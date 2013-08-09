
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoiRank, readKhresmoi
from statistics import calculateStatistics


PATH_TO_DATASETS = "../logAnalysisDataSets/"

if __name__ == "__main__":

    in50 = readMyFormat("in50", "v5")
    in502 = readMyFormat("in50", "v5")
    #in503 = readMyFormat("in50", "v5")
    #in50 += in502
    #in50 += in503
    datasets =  [ [in50, "in50"], [in502, "in50-2"] ] 
    calculateStatistics(datasets)
    
    #goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldMiner.v5.dataset.gz", "v5")
    #hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish.v5.dataset.gz", "v5")
    #trip = readMyFormat(PATH_TO_DATASETS + "trip/trip.v5.dataset.gz", "v5")
    #aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthClean.v5.dataset.gz", "v5")
    #aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/ ", "v5")

    #laypeople = hon + aolHealth
    #experts = goldMiner + trip
    #calculateMetrics([ [aolHealth, "aolHealth"], [hon, "hon"], [laypeople, "laypeople"], [trip, "trip"], [goldMiner, "goldminer"], [experts, "experts" ], [aolNotHealth, "aolNotHealth"] ]) 
    
    #calculateMetrics([ [aolHealth, "aolHealth"], [hon, "hon"],[trip, "trip"], [goldMiner, "goldminer"] ]) 
    #calculateMetrics([ [laypeople, "laypeople"], [experts, "experts" ] ]) 
    
    #aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthAndNotClick.v4.dataset.gz", "v4")
    #calculateMetrics([ [aolHealth, "aolHealth"], [hon, "hon"], [trip, "trip"], [goldMiner, "goldminer"], [aolNotHealth, "aolNotHealth" ] ]) 
   
  
