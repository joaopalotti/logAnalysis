import pickle, sys

from classifiers import classify, makeReport, plotGraph, getPrecisionRecall, getROC

with open("ROC.pk", 'rb') as input:
    roc = pickle.load(input)

with open("precisionAndRecall.pk", 'rb') as input:
    precisionAndRecall = pickle.load(input)

plotGraph(roc, fileName="ROC", xlabel="Recall", ylabel="Precision", generatePickle=False, hasPlotLibs=True)
plotGraph(precisionAndRecall, fileName="precisionAndRecall", xlabel="Recall", ylabel="Precision", generatePickle=False, hasPlotLibs=True)

