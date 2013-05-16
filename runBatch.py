import sys
from runClassifiers import *
from metrics import npStatistics
from scipy import stats

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
   
    print "comparing NB: "
    compareValues(6)


def compareValues(minIndex):
    blAccs, blF1s, blwF1s, cAccs, cF1s, cwF1s = [], [], [], [], [], []
    for group in returnedValues:
        accBaseline, f1Baseline, wf1Baseline, classacc, classf1, classwf1 = group[0:2], group[minIndex:minIndex+2]
        blAccs.append(accBaseline)
        blF1s.append(f1Baseline)
        blwF1s.append(wf1Baseline)
        cAccs.append(classacc)
        cF1s.append(classf1)
        cwF1s.append(classwf1)

    (tacc, probacc) = stats.ttest_rel(blAccs, cAccs)
    (tf1, probf1) = stats.ttest_rel(blf1, cf1)
    (wtf1, probwf1) = stats.ttest_rel(blwf1, cwf1)
    
    blAccStat = generateStatsVector(blAccs)
    blF1sStat = generateStatsVector(blF1s)
    blwF1Stat = generateStatsVector(blwF1s)
    cAccsStat = generateStatsVector(cAccs)
    cF1sStat  = generateStatsVector(cF1s)
    cwF1sStat = generateStatsVector(cwF1s)

    print "BL = %.3f (+/- %.2f)" % (blAcc.mean, blAccStat.std)
    print "F1 = %.3f (+/- %.2f)" % (blF1Stat.mean, blF1Stat.std)
    print "wF1 = %.3f (+/- %.2f)" % (blwF1Stat.mean, blwF1Stat.std)

    print "Classifier ACC = %.3f (+/- %.2f)" % (cAccStat.mean, cAccStat.std)
    print "F1 ACC         = %.3f (+/- %.2f)" % (cF1sStat.mean, cF1sStat.std)
    print "wF1 ACC        = %.3f (+/- %.2f)" % (cwF1sStat.mean, cwF1sStat.std)
 
    print "Tacc, Probacc = ", tacc, probacc, probacc > 0.05
    print "Tf1, probF1   = ", tf1, probf1, probf1 > 0.05
    print "wtF1, probwf1 = ", wtf1, probwf1, probwf1 > 0.05
    

    #(accBaseline, f1Baseline, wf1Baseline, ertacc, ertf1, ertwf1, nbacc, nbf1, nbwf1, knnacc, knnf1, knnwf1, dtacc, dtf1, dtwf1,lgacc, lgf1, lgwf1, svmacc, svmwf1, svmwf1)  




