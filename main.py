from statistics import calculateStatistics
from readCSV import readMyFormat 
import pandas as pd

PATH_TO_DATASETS = "/data/palotti/logAnalysisDataSets/"
AOLH_DATASET = "/data/palotti/logAnalysisDataSets/aolData/AOL-user-ct-collection/healthq.fixed.gz"
AOLNH_DATASET = "/data/palotti/logAnalysisDataSets/aolData/AOL-user-ct-collection/nhealthq.fixed.gz"
usingScoop = False
useHON = True
useGM = True
useTRIP = True
useAOLH = True
useAOLNH = False
useLAY = False
useEXP = False

if __name__ == "__main__A":
    datasets = []
    data = readMyFormat(PATH_TO_DATASETS + "trip/trip1.gz")
    datasets.append([data, "TEST"])
    
    calculateStatistics(datasets, usingScoop) 

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
        aolHealth = readMyFormat(AOLH_DATASET)
        datasets.append([aolHealth, "AOLH"])    
    
    if useAOLNH:
        aolnHealth = readMyFormat(AOLNH_DATASET)
        datasets.append([aolnHealth, "AOLNH"])    
    
    if useLAY:
        laypeople = hon + aolHealth
        datasets.append([laypeople, "LAY"])    
    
    if useEXP:
        experts = trip + gm
        datasets.append([experts, "EXP"])    

    calculateStatistics(datasets, usingScoop) 

