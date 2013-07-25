
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoiRank, readKhresmoi
from statistics import calculateMetrics
import gzip

PATH_TO_DATASETS = "dataSetsOfficials/"

if __name__ == "__main__":

    in50 = readMyFormat("in50", "v5")
    in502 = readMyFormat("in50", "v5")
    in503 = readMyFormat("in50", "v5")
    in50 += in502
    in50 += in503
    calculateMetrics([ [in50, "in50"] ] ) 
    
    #in50 = readMyFormat("out.v5", "v5")
    #calculateMetrics([ [in50, "outv5"] ] ) 
    
    #khr = readKhresmoiRank("../../logs/krslogs/clicked_rank_task1.csv")
    #calculateMetrics([ [khr, "khr4"]] ) 
    #khr = readKhresmoiRank("../../logs/krslogs/clicked_rank_task2.csv")
    #calculateMetrics([ [khr, "khr2"]] ) 
    #khr = readKhresmoiRank("../../logs/krslogs/clicked_rank_task3.csv")
    #calculateMetrics([ [khr, "khr3"]] ) 
    #khr = readKhresmoiRank("../../logs/krslogs/clicked_rank_task4.csv")
    #calculateMetrics([ [khr, "khr4"]] ) 

    #khr = readKhresmoi("../../logs/krslogs/clickthru_task1.csv")
    #calculateMetrics([ [khr, "khr1"]] ) 

    #khr = readKhresmoi("../../logs/krslogs/clickthru_task2.csv")
    #calculateMetrics([ [khr, "khr2"]] ) 

    #khr = readKhresmoi("../../logs/krslogs/clickthru_task3.csv")
    #calculateMetrics([ [khr, "khr3"]] ) 

    #khr = readKhresmoi("../../logs/krslogs/clickthru_task4.csv")
    #calculateMetrics([ [khr, "khr4"]] ) 

    
    #goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldMiner.v5.dataset.gz", "v5")
    #hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish.v5.dataset.gz", "v5")
    #trip = readMyFormat(PATH_TO_DATASETS + "trip/trip_mod.v5.dataset.gz", "v5")
    #aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthCompleteFixed.v5.dataset.gz", "v5")
    #aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthAndNotClick.v4.dataset.gz", "v4")
    #calculateMetrics([ [aolHealth, "aolHealth"], [hon, "hon"], [trip, "trip"], [goldMiner, "goldminer"] ]) 
    #calculateMetrics([ [aolHealth, "aolHealth"], [hon, "hon"], [trip, "trip"], [goldMiner, "goldminer"], [aolNotHealth, "aolNotHealth" ] ]) 
    #calculateMetrics([ [goldMiner, "goldminer"] ]) 
    
    
    #hon = readMyFormat("dataSetsOfficials/hon/olds/hon3")
    #calculateMetrics([ [hon, "hon"] ] ) 
    
    #hon = readMyFormat(PATH_TO_DATASETS + "honEnglishResult.v3.dataset.gz")
    #hon = readMyFormat(PATH_TO_DATASETS + "honEnglish.v4.dataset")
    #hon = readMyFormat("test")

    #hon = readMyFormat(PATH_TO_DATASETS + "honEnglish.dataset")
    #hon = readHONDataSet(PATH_TO_DATASETS + "honEnglish.dataset")
    #hon = readHONDataSet(PATH_TO_DATASETS + "honSmall.csv")
    #aolNotHealth = readAolDataSet(PATH_TO_DATASETS + "aolNotHealthsitesSmall.csv")
    #goldminer = readGoldMiner(PATH_TO_DATASETS + "goldminer-v4.txt")
    
    #for member in hon:
    #    member.normalPrint()

    #calculateMetrics([ [aol, "Aol"], [ trip, "Trip"], [hon, "HoN" ] ]) 
    #calculateMetrics([ [trip, "Trip"] ] ) 
    #calculateMetrics([ [hon, "Hon"], [trip, "Trip"] ] ) 
    #calculateMetrics([ [aol, "Aol"] ] ) 
    #calculateMetrics([ [aolNotHealth, "~aol"] ] ) 
    #calculateMetrics([ [goldMiner, "goldMiner"], [hon, "Hon"] ]) 
    #calculateMetrics([ [goldMiner, "goldMiner"] ]) 

