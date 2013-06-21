import sys
from runClassifiers import *
from metrics import generateStatsVector
from scipy import stats

def compareValues(minIndex):
    blAccs, blF1s, blwF1s, cAccs, cF1s, cwF1s = [], [], [], [], [], []
    for group in returnedValues:
        accBaseline, f1Baseline, wf1Baseline, classacc, classf1, classwf1 = group[0], group[1], group[2], group[minIndex], group[minIndex+1], group[minIndex+2]
        blAccs.append(accBaseline)
        blF1s.append(f1Baseline)
        blwF1s.append(wf1Baseline)
        cAccs.append(classacc)
        cF1s.append(classf1)
        cwF1s.append(classwf1)

    (tacc, probacc) = stats.ttest_rel(blAccs, cAccs)
    (tf1, probf1) = stats.ttest_rel(blF1s, cF1s)
    (wtf1, probwf1) = stats.ttest_rel(blwF1s, cwF1s)
    
    blAccsStat = generateStatsVector(blAccs)
    blF1sStat = generateStatsVector(blF1s)
    blwF1sStat = generateStatsVector(blwF1s)
    cAccsStat = generateStatsVector(cAccs)
    cF1sStat  = generateStatsVector(cF1s)
    cwF1sStat = generateStatsVector(cwF1s)

    print "BL = %.3f (+/- %.5f)" % (blAccsStat.mean, blAccsStat.std)
    print "F1 = %.3f (+/- %.5f)" % (blF1sStat.mean, blF1sStat.std)
    print "wF1 = %.3f (+/- %.5f)" % (blwF1sStat.mean, blwF1sStat.std)

    print "Classifier ACC = %.3f (+/- %.5f)" % (cAccsStat.mean, cAccsStat.std)
    print "Classifier F1          = %.3f (+/- %.5f)" % (cF1sStat.mean, cF1sStat.std)
    print "Classifier wF1        = %.3f (+/- %.5f)" % (cwF1sStat.mean, cwF1sStat.std)
  
    print "ACC GAIN --> %0.2f%% " % (100.0 * (cAccsStat.mean - blAccsStat.mean) / blAccsStat.mean)
    print "F1 GAIN --> %0.2f%% " %  (100.0 * (cF1sStat.mean - blF1sStat.mean) / blF1sStat.mean)
    print "WF1 GAIN --> %0.2f%% " % (100.0 * (cwF1sStat.mean - blwF1sStat.mean) / blwF1sStat.mean)



    print "Tacc, Probacc = ", tacc, probacc, probacc > 0.05
    print "Tf1, probF1   = ", tf1, probf1, probf1 > 0.05
    print "wtF1, probwf1 = ", wtf1, probwf1, probwf1 > 0.05
    
if __name__ == "__main__":
    
    preProcessing = sys.argv[1]
    forceBalance = int(sys.argv[2])
    proportional = int(sys.argv[3])
    minNumberOfQueries = int(sys.argv[4])
    numberOfTimes = int(sys.argv[5])
    
    returnedValues = []

    print "It is going to run this experiment ", numberOfTimes, " times."
    print "Preprocessing:", preProcessing, " forceBalance =", forceBalance, " proportional ", proportional, " minNumberOfQueries=", minNumberOfQueries

    for i in range(0,numberOfTimes):
        print "RUNNING EXPERIMENT ", i
        returnedValues.append( runClassify(preProcessing, forceBalance, proportional, minNumberOfQueries, i) )
    

    print returnedValues
    print "------- comparing ERT ---------- "
    compareValues(3)
   
    print "------- comparing NB  ---------- "
    compareValues(6)

    print "------- comparing KNN ---------- "
    compareValues(9)
    
    print "------- comparing DT ---------- "
    compareValues(12)

    print "------- comparing LG ---------- "
    compareValues(15)
    
    print "------- comparing SVM ---------- "
    compareValues(18)
    
    #(accBaseline, f1Baseline, wf1Baseline, ertacc, ertf1, ertwf1, nbacc, nbf1, nbwf1, knnacc, knnf1, knnwf1, dtacc, dtf1, dtwf1,lgacc, lgf1, lgwf1, svmacc, svmwf1, svmwf1)  




