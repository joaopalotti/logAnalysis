
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoiRank, readKhresmoi
from statistics import calculateStatistics


PATH_TO_DATASETS = "../logAnalysisDataSets/"

if __name__ == "__main__":

    #in50 = readMyFormat("in50", "v5")
    #in502 = readMyFormat("in50", "v5")
    #in503 = readMyFormat("in50", "v5")
    #in50 += in502
    #in50 += in503
    #datasets =  [ [in50, "in50"], [in502, "in50-2"] ] 
    #calculateStatistics(datasets)
   
    cikm = True

    goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldMiner.v5.dataset.gz", "v5")
    hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish.v5.dataset.gz", "v5")
    trip = readMyFormat(PATH_TO_DATASETS + "trip/trip.v5.dataset.gz", "v5")
    
    if cikm:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthCompleteFixed5.v5.dataset.gz", "v5")
        aolNotHealth = readMyFormat( PATH_TO_DATASETS + "aolNotHealth/aolNotHealthFinal-noDash.v5.dataset.gz", "v5")
    else:
        aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNOThealthNoAnimal-NoDash.v5.dataset.gz", "v5")
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthClean.v5.dataset.gz", "v5")

    laypeople = hon + aolHealth
    experts = trip + goldMiner

    datasets =  [ [aolNotHealth, "aolNotHealth"], [aolHealth, "aolHealth"], [hon, "hon"], [laypeople, "laypeople"], [trip, "trip"], [goldMiner, "goldminer"], [experts, "experts" ] ]
     
    calculateStatistics(datasets) 

