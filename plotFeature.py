from __future__ import division
import pandas as pd
import numpy as np

importances = pd.read_pickle("features.pk")
std = pd.read_pickle("features_std.pk")
groups = tuple(["sem","chv","umls","pos","basic"])
factor = 10.0

def getLabels(group):
    labels = []
    semantic_labels = ["AvgSymptomsPerQuery","AvgCausesPerQuery","AvgRemediesPerQuery","AvgNonSymCauseRemedyTypesPerQuery"]
    umls_labels = ["AvgQueriesUsingMeSH","AvgNumberOfMeSHPerQuery","AvgMeSHDepth","AvgQueriesUsingSources", "AvgNumberOfSourcesPerQuery", "AvgQueriesUsingConcepts", "AvgNumberOfConceptsPerQuery"]
    chv_labels = ["AvgNumberOfCHVDataFound", "AvgNumberOfCHVFound", "AvgNumberOfUMLSFound", "AvgNumberOfCHVMisspelledFound", "AvgNumberOfComboScoreFound"]
    pos_labels = ["PercentageOfAdjectives", "PercentageOfAdverbs","PercentageOfAuxiliars","PercentageOfConjuctions", "PercentageOfDeterminers",\
              "PercentageOfModals", "PercentageOfNouns", "PercentageOfPrepositions", "PercentageOfPronouns", "PercentageOfPunctuations",\
              "PercentageOfShapes", "PercentageOfVerbs"]
    basic_labels = ["AvgCharsPerQuery", "AvgWordsPerQuery"]

    if "sem" in group:
        labels.extend(semantic_labels)
    if "chv" in group:
        labels.extend(chv_labels)
    if "umls" in group:
        labels.extend(umls_labels)
    if "pos" in group:
        labels.extend(pos_labels)
    if "basic" in group:
        labels.extend(basic_labels)
    return np.array(labels)

labels = getLabels(groups)
indices = np.argsort(importances[groups])[::-1]

# Plot the feature importances of the forest
import pylab as pl

for n in [5,10]:
    pl.figure()
    pl.title("Feature importances")
    pl.bar(range(n), factor * importances[groups][indices][0:n], color="r", yerr=(factor * std[groups][indices][0:n]), align="center")
    pl.xticks(range(n), indices)
    pl.xlim([-1, n])
    pl.savefig("top%d.png" % (n))




