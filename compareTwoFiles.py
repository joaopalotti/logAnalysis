from __future__ import division

import sys 
from auxiliarFunctions import generateStatsVector

# input for this program is a list of files each one like this:
# clf, PX, Val1, Val2, Val3, Val4
# clf, PY, Val1, Val2, Val3, Val4
# clf2, PX, Val1, Val2, Val3, Val4
# ....etc
# Also, the files should have this pattern for name: classification.result.i.gX -> where X can be any combination of the 7 groups

file1 = sys.argv[1]
file2 = sys.argv[2]

#import glob, os
#os.chdir(pathToFiles)
#for file in glob.glob("*"):
#    print file

def getVector(filename, alg, metricIndex):
    try:
        f = file(filename, "r")
        print "File %s found!" % (filename)
    except IOError:
        print "Error: File %s not found!" % (filename)
        return [0,0]

    algLines = []
    metricVec = []
    for line in f:
        if alg in line:
            algLines.append(line.strip())

    for line in algLines:
        #print line
        metric = line.split(",")[metricIndex].strip()
        #print metric
        metricVec.append(float(metric))

    return metricVec

def calculateWinner(filename1, filename2, alg, metricIndex):
    # MetricIndex => 2: Acc, 3: f1

    metricVec0 = getVector(filename1, alg, metricIndex)
    metricVec1 = getVector(filename2, alg, metricIndex)

    metricSv0 = generateStatsVector(metricVec0)
    metricSv1 = generateStatsVector(metricVec1)

    winner = -1
    if metricSv0.mean > metricSv1.mean:
        winner = 0
    elif metricSv1.mean > metricSv0.mean:
        winner = 1
   
    print metricSv0.mean, metricSv1.mean
    #from scipy import stats
    #t, p = stats.ttest_rel(metricVec0, metricVec1)
    #if p > 0.05:
    #    winner = -1

    return winner

def main():
    classifiers = ["Random Forest", "SVM", "Decision Tree", "Logistic Regression", "Naive Bayes", "KNN"]

    for classifier in classifiers:
        accWinner = calculateWinner(file1, file2, classifier, 2)
        f1Winner = calculateWinner(file1, file2, classifier, 3)
        
        print classifier, accWinner, f1Winner


if __name__ == "__main__":
    main()
