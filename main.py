import sys
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoiRank, readKhresmoi
from statistics import calculateStatistics

PATH_TO_DATASETS = "../logAnalysisDataSets/"
usingScoop = False
cikm = False
usingAugHON = True
testingAOLNotHealth = True
toyExample = False
testing = "" # "1."

if __name__ == "__main__":

    if toyExample:
        in50 = readMyFormat("in50", "v5")
        in502 = readMyFormat("in50", "v5")
        datasets =  [ [in50, "in50"], [in502, "in50-2"] ] 
        calculateStatistics(datasets, usingScoop)
        sys.exit(0)

    goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldMiner.v5." + testing + "dataset.gz", "v5")
    if usingAugHON:
        hon = readMyFormat(PATH_TO_DATASETS + "hon/honAugEnglish.v5." + testing + "dataset.gz", "v5")
    else:
        hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish.v5." + testing + "dataset.gz", "v5")

    trip = readMyFormat(PATH_TO_DATASETS + "trip/trip.v5." + testing + "dataset.gz", "v5")
    
    if cikm:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthCompleteFixed5.v5."+ testing + "dataset.gz", "v5")
        if testingAOLNotHealth:
            aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthFinal-noDash.v5." + testing + "dataset.gz", "v5")
    else:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthClean.v5."+ testing + "dataset.gz", "v5")
        if testingAOLNotHealth:
            aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthNoAnimal-noDash.v5." + testing + "dataset.gz", "v5")

    laypeople = hon + aolHealth
    experts = trip + goldMiner

    if testingAOLNotHealth:
        datasets =  [ [aolNotHealth, "aolNotHealth"], [aolHealth, "aolHealth"], [hon, "hon"], [laypeople, "laypeople"], [trip, "trip"], [goldMiner, "goldminer"], [experts, "experts" ] ]
    else:
        datasets =  [ [aolHealth, "aolHealth"], [hon, "hon"], [laypeople, "laypeople"], [trip, "trip"], [goldMiner, "goldminer"], [experts, "experts" ] ]
     
    calculateStatistics(datasets, usingScoop) 

