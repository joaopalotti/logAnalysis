from statistics import calculateStatistics
from readCSV import readMyFormat 
import pandas as pd

PATH_TO_DATASETS = "../logAnalysisDataSets/"
usingScoop = False
useHON = True
useGM = False
useTRIP = False
useAOLH = False

#aolNotHealthOption = 0
# 0) NOT using it
# 1) aolNotHealthFinal-noDash  (CIKM)
# 2) aolHealthNoAnimal-noDash-clicked
# 3) aolNotHealthODP (WSDM) *
# 4) aolNotHealthODPNoScience

if __name__ == "__main__":
    
    datasets = []

    #GoldMiner
    if useGM:
        gm = readMyFormat(PATH_TO_DATASETS + "gm/gm.gz")
        datasets.append([gm, "GM"])
   
    #HON
    if useHON:
        hon = readMyFormat(PATH_TO_DATASETS + "hon/hon.gz")
        datasets.append([hon, "HON"])
        
    #Trip
    if useTRIP:
        trip = readMyFormat(PATH_TO_DATASETS + "trip/trip.gz")
        datasets.append([trip, "TRIP"])    

    #AOL-Health
    if useAOLH:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolh/aolh.gz")
        datasets.append([aolHealth, "AOLH"])    
    
    #if mergeLaypeople:
    #    laypeople = hon + aolHealth
    
    #if mergeExperts:
    #    experts = trip + goldMiner

    calculateStatistics(datasets, usingScoop) 

