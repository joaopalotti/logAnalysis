
from readCSV import readTripDataSet, readAolDataSet, readHONDataSet, readGoldMiner, readMyFormat, readKhresmoiRank, readKhresmoi
from statistics import calculateMetrics
import gzip

PATH_TO_DATASETS = "dataSetsOfficials/"

if __name__ == "__main__":

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

    
    #goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldMiner.v4.dataset.gz")
    #hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish.v4.dataset.gz")
    #trip = readMyFormat(PATH_TO_DATASETS + "trip/trip_mod.v4.dataset.gz")
    #aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealthCompleteFixed.v4.dataset.gz")
    #aolNotHealth = readMyFormat(PATH_TO_DATASETS + "aolNotHealth/aolNotHealthAndNotClick.v4.dataset.gz")
    #calculateMetrics([ [aolHealth, "aolHealth"], [hon, "hon"], [trip, "trip"], [goldMiner, "goldminer"], [aolNotHealth, "aolNotHealth" ] ]) 
    
    
    hon = readMyFormat("dataSetsOfficials/hon/olds/hon3")
    calculateMetrics([ [hon, "hon"] ] ) 
    
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

