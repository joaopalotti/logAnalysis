
import pickle
import pylab as pl
import sys
from collections import defaultdict
featureFileName = sys.argv[1]

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

print "TOP", topX, "features"
for i in range(topX):
    print i, featureNamesSorted[i]


G1 = ["AvgCharsPerQuery", "AvgWordsPerQuery", "AvgUseOfNL", "AnyPastUseOfNL", "AvgUseOfMedAbb", "AnyPastUseOfMedAbb", "CharsInQuery", "WordsInQuery", "UsedNLQuery", "UsedMedAbbQuery"]
G2 = ["AvgQueriesPerSession", "AvgTimePerSession"]
G3 = ["AvgNumberOfExpansions", "AnyPastExpansion", "ExpandedQuery", "AvgNumberOfReductions", "AnyPastReductions", "ReductedQuery", "AvgNumberOfModifications", "AnyPastModification", "ModifiedQuery", "AvgNumberOfKeeps", "AnyPastKeep", "KeptQuery"]
G4 = ["AvgSymptomsPerQuery", "AnyPastSearchForSymptoms", "AvgCausesPerQuery", "AnyPastSearchForCauses", "AvgRemediesPerQuery", "AnyPastSearchForRemedies", "AvgNonSymCauseRemedyTypesPerQuery", "AnyPastSearchForNonSymCauseRemedyTypes",  "SearchedSymptomQuery", "SearchedCauseQuery", "SearchedRemedyQuery", "SearchedForNonSymCauseRemedyQuery"]
G5 = ["AvgQueriesUsingMeSH", "AvgNumberOfMeSHPerQuery", "AvgMeSHDepth", "HasUsedMeSHBefore", "NumberOfMeshInQuery", "MeSHDepthInQuery", "AvgQueriesUsingSources", "AvgNumberOfSourcesPerQuery", "TotalNumberOfDifferentSourcesUsed", "NumberOfSourcesInQuery", "AvgQueriesUsingConcepts", "AvgNumberOfConceptsPerQuery", "TotalNumberOfDifferentConceptsUsed", "NumberOfConceptsInQuery"]
G6 = ["AvgNumberOfCHVDataFound", "AnyCHVDataInPast", "AvgNumberOfCHVFound", "AnyCHVInPast", "AvgNumberOfUMLSFound", "AnyUMLSInPast", "AvgNumberOfCHVMisspelledFound", "AnyCHVMisspelledInPast", "AvgNumberOfComboScoreFound", "NumberOfCHVDataQuery", "NumberOfUMLSQuery", "NumberOfCHVMisspelledQuery", "NumberOfComboScoreQuery"]
G7 = ["PercentageOfNouns", "PercentageOfAdjectives", "PercentageOfConjuctions", "PercentageOfVerbs", "PercentageOfShapes", "PercentageOfPunctuations", "PercentageOfAdverbs", "PercentageOfDeterminers", "PercentageOfAuxiliars", "PercentageOfPrepositions", "PercentageOfPronouns", "hasNouns", "hasAdjectives", "hasConjuctions", "hasVerbs", "hasShapes", "hasPunctuations", "hasAdverbs", "hasDeterminers", "hasAuxiliars", "hasPrepositions", "hasPronotuns"]

range1 = 11
range2 = 21
range3 = 31
range4 = 41
range5 = 51
range6 = 61
range7 = 71
range8 = 81

groups = {}
for g in ["g1", "g2", "g3", "g4", "g5", "g6", "g7"]:
    groups[g] = dict()
    for i in range(9):
        groups[g][i] = 0

def putInGroup(groupsDict, group , i):
    if i < range1:
        groupsDict[group][0] += 1
    elif i < range2:
        groupsDict[group][1] += 1
    elif i < range3:
        groupsDict[group][2] += 1
    elif i < range4:
        groupsDict[group][3] += 1
    elif i < range5:
        groupsDict[group][4] += 1
    elif i < range6:
        groupsDict[group][5] += 1
    elif i < range7:
        groupsDict[group][6] += 1
    elif i < range8:
        groupsDict[group][7] += 1
    else:
        groupsDict[group][8] += 1

for i in range(len(featureNamesSorted)):
    if featureNamesSorted[i] in G1:
        putInGroup(groups, "g1", i)
    
    elif featureNamesSorted[i] in G2:
        putInGroup(groups, "g2", i)
    
    elif featureNamesSorted[i] in G3:
        putInGroup(groups, "g3", i)

    elif featureNamesSorted[i] in G4:
        putInGroup(groups, "g4", i)
    
    elif featureNamesSorted[i] in G5:
        putInGroup(groups, "g5", i)
    
    elif featureNamesSorted[i] in G6:
        putInGroup(groups, "g6", i)
    
    elif featureNamesSorted[i] in G7:
        putInGroup(groups, "g7", i)

################################### ----> Table 1
print("\\begin{table}[ht]")
print("\\caption{Table}")
print("\\label{tab:comparison2x2}")
print("\\centering")
print("\\begin{tabular}{|c||c|c|c|c|c|c|c|c|c|c|}")
print("\\toprule")
print "Groups & 1-10 & 11-20 & 21-30 & 31-40 & 41-50 & 51-60 & 61-70 & 71-80 & 81-87 \\\\"
print("\\midrule")
for g, ranges in sorted(groups.items()):
    print g, "&", ranges[0],
    for i in range(1,9):
        print " & ", ranges[i],
    print ("\\\\ \\hline")
#print ("\\bottomrule")
print ("\\end{tabular}")
print ("\\end{table}")

################################### ----> Table 1

top = defaultdict(list)
for i in range(len(featureNamesSorted)):
    if featureNamesSorted[i] in G1:
        top["g1"].append(featureNamesSorted[i] + " ("+str(i)+")")
    elif featureNamesSorted[i] in G2:
        top["g2"].append(featureNamesSorted[i] + " ("+str(i)+")")
    elif featureNamesSorted[i] in G3:
        top["g3"].append(featureNamesSorted[i] + " ("+str(i)+")")
    elif featureNamesSorted[i] in G4:
        top["g4"].append(featureNamesSorted[i] + " ("+str(i)+")")
    elif featureNamesSorted[i] in G5:
        top["g5"].append(featureNamesSorted[i] + " ("+str(i)+")")
    elif featureNamesSorted[i] in G6:
        top["g6"].append(featureNamesSorted[i] + " ("+str(i)+")")
    elif featureNamesSorted[i] in G7:
        top["g7"].append(featureNamesSorted[i] + " ("+str(i)+")")
        
for name, features in top.items():
    print name, features

print("\\begin{table}[ht]")
print("\\caption{Table}")
print("\\label{tab:comparison2x2}")
print("\\\hspace{-3cm}")
print("\\\scriptsize")
print("\\begin{tabular}{|c|c|c|c|c|c|c|}")
print("\\toprule")
print "Group 1 & Group 2 & Group 3 & Group 4 & Group 5 & Group 6 & Group 7 \\\\"
print("\\midrule")
print top["g1"][0] , "&", top["g2"][0], "&", top["g3"][0], "&", top["g4"][0], "&", top["g5"][0], "&", top["g6"][0], "&", top["g7"][0], "\\\\ \hline" 
print top["g1"][1] , "&", top["g2"][1], "&", top["g3"][1], "&", top["g4"][1], "&", top["g5"][1], "&", top["g6"][1], "&", top["g7"][1], "\\\\ \hline" 
print top["g1"][2] , "&", "&", top["g3"][2], "&", top["g4"][2], "&", top["g5"][2], "&", top["g6"][2], "&", top["g7"][2], "\\\\ \hline" 
print top["g1"][3] , "&", "&", top["g3"][3], "&", top["g4"][3], "&", top["g5"][3], "&", top["g6"][3], "&", top["g7"][3], "\\\\ \hline" 
print top["g1"][4] , "&", "&", top["g3"][4], "&", top["g4"][4], "&", top["g5"][4], "&", top["g6"][4], "&", top["g7"][4], "\\\\ \hline" 
#print ("\\bottomrule")
print ("\\end{tabular}")
print ("\\end{table}")





