
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




    #goldMiner = readMyFormat(PATH_TO_DATASETS + "goldminer/goldminer.v4.dataset.gz")
    #hon = readMyFormat(PATH_TO_DATASETS + "hon/honEnglish.v4.dataset")
    trip = readMyFormat(PATH_TO_DATASETS + "trip/tripResult.v4.dataset.gz")
    #aolHealth = readMyFormat(PATH_TO_DATASETS + "aolHealth/aolHealth.v4.dataset.gz")
    
    #calculateMetrics([ [goldMiner, "goldminer"],[hon, "hon"],[trip, "trip"],[aolHealth, "aolHealth"] ] ) 
    calculateMetrics([ [trip, "hon"] ] ) 
    
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

