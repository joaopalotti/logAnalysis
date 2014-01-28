from statistics import calculateStatistics
from readCSV import readMyFormat 
import pandas as pd

PATH_TO_DATASETS = "../logAnalysisDataSets/"
usingScoop = False
useHON = True
useGM = True
useTRIP = True
useAOLH = True
useAOLNH = True
useLAY = True
useEXP = True

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
    
    if useAOLNH:
        aolHealth = readMyFormat(PATH_TO_DATASETS + "aolnh/aolnh.gz")
        datasets.append([aolHealth, "AOLNH"])    
    
    if useLAY:
        laypeople = hon + aolHealth
        datasets.append([laypeople, "LAY"])    
    
    if useEXP:
        experts = trip + gm
        datasets.append([experts, "EXP"])    

    calculateStatistics(datasets, usingScoop) 

