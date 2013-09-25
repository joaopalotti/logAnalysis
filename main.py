import sys
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoiRank, readKhresmoi
from statistics import calculateStatistics

PATH_TO_DATASETS = "../logAnalysisDataSets/"
usingScoop = False
cikm = False
usingAugHON = True
toyExample = False
testing = "" # "1."
version = "v6"
khresmoiOnly = False

aolNotHealthOption = 0
# 0) NOT using it
# 1) aolNotHealthFinal-noDash  (CIKM)
# 2) aolHealthNoAnimal-noDash-clicked
# 3) aolNotHealthODP (WSDM)
# 4) aolNotHealthODPNoScience

if __name__ == "__main__":
    
    if khresmoiOnly:
        khresmoi = readMyFormat(PATH_TO_DATASETS + "hon/khresmoi_hon.v5.dataset.gz", "v5")
        datasets =  [ [khresmoi, "khresmoi"] ]
        calculateStatistics(datasets, usingScoop) 
        sys.exit(0)

    if toyExample:
        in50 = readMyFormat("v6", "v6")
        in502 = readMyFormat("v6", "v6")
        #in50 = readMyFormat("in50", "v5")
        #in502 = readMyFormat("in50", "v5")
        datasets =  [ [in50, "in50"], [in502, "in50-2"] ] 
        calculateStatistics(datasets, usingScoop)
        sys.exit(0)

    goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldMiner." + version + "." + testing + "dataset.gz", version)
    if usingAugHON:
        hon = readMyFormat(PATH_TO_DATASETS + "hon/honAugEnglish." + version + "." + testing + "dataset.gz", version)
    else:
        hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish." + version + "." + testing + "dataset.gz", version)

    trip = readMyFormat(PATH_TO_DATASETS + "trip/trip." + version + "." + testing + "dataset.gz", version)
         
    if aolNotHealthOption > 0:
        if aolNotHealthOption == 1:
            aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthFinal-noDash." + version + "." + testing + "dataset.gz", version)
        elif aolNotHealthOption == 2:
            aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthNoAnimal-noDash-clicked." + version + "." + testing + "dataset.gz", version)
        elif aolNotHealthOption == 3:
            aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthODP." + version + "." + testing + "dataset.gz", version)
        elif aolNotHealthOption == 4:
            aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthODPNoScience." + version + "." + testing + "dataset.gz", version)
   
    if cikm:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthCompleteFixed5."+ version + "." + testing + "dataset.gz", version)
    else:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthClean." + version + "." + testing + "dataset.gz", version)

    laypeople = hon + aolHealth
    experts = trip + goldMiner

    if aolNotHealthOption > 0:
        datasets =  [ [aolNotHealth, "aolNotHealth"], [aolHealth, "aolHealth"], [hon, "hon"], [laypeople, "laypeople"], [trip, "trip"], [goldMiner, "goldminer"], [experts, "experts" ] ]
    else:
        datasets =  [ [aolHealth, "aolHealth"], [hon, "hon"], [laypeople, "laypeople"], [trip, "trip"], [goldMiner, "goldminer"], [experts, "experts" ] ]
     
    calculateStatistics(datasets, usingScoop) 

