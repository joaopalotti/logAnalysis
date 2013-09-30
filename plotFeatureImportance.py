
import pickle
import pylab as pl
featureFileName = "featureImportance.pk"

with open(featureFileName, 'rb') as input:
    featureDict = pickle.load(input)

indices = featureDict["indices"]
featureNames = featureDict["featureNames"]
std = featureDict["std"]
importances = featureDict["importances"]

nFeatures = len(indices)
featureNamesSorted = [featureNames[i].split(".")[1] for i in indices]
topX = 10 #nFeatures
topXIndices = indices[0:10]

print "len - > ", len(topXIndices)
pl.figure()
pl.title("Feature importances")
pl.bar(range(topX), importances[topXIndices], color="r", yerr=std[topXIndices], align="center")
pl.xticks(range(topX), featureNamesSorted[0:topX], rotation='vertical')
pl.xlim([-1, topX])
pl.show()

