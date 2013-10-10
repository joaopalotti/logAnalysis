import pickle, sys

from classifiers import classify, makeReport, plotGraph, getPrecisionRecall, getROC
path = sys.argv[1]

with open(path + "ROC.pk", 'rb') as input:
    roc = pickle.load(input)
print roc

with open(path + "precisionAndRecall.pk", 'rb') as input:
    precisionAndRecall = pickle.load(input)

plotGraph(roc, fileName="ROC", xlabel="False Positive Rate", ylabel="True Positive Rate", generatePickle=False, hasPlotLibs=True)
plotGraph(precisionAndRecall, fileName="precisionAndRecall", xlabel="Recall", ylabel="Precision", generatePickle=False, hasPlotLibs=True)

