#Report
from sklearn import cross_validation
from sklearn.metrics import classification_report, f1_score, accuracy_score
#General
from collections import Counter, defaultdict

def makeIncrementalReport(X, y, listOfYs, accBaseline, f1Baseline, wf1Baseline):
    a, f, wf = [], [], []
    for i in listOfYs:
        print "Partition ", i
        print len(listOfYs[i])
        #print listOfYs[i]
        acc, sf1, wf1 = makeReport(X, y, listOfYs[i], accBaseline, f1Baseline, wf1Baseline)
        a, f, wf = a + [acc], f + [sf1], wf + [wf1]
    return a, f, wf

def makeReport(X, y, y_pred, accBaseline, f1Baseline, wf1Baseline):
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    
    target_names = ['Layman', 'Specialist']
    
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred, average=None)
    sf1 = f1_score(y, y_pred)
    
    print(classification_report(y, y_pred, target_names=target_names))
    
    ns = Counter(y)
    wf1 = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    
    print "F1 Scores (no average) --> ", (f1)
    
    print "wf1 -> ", wf1
    print "GAIN --> %0.2f%% " % (100.0 * (wf1 - wf1Baseline) / wf1Baseline)

    print "sf1 -> ", sf1
    print "GAIN --> %0.2f%% " % (100.0 * (sf1 - f1Baseline) / f1Baseline)

    print "ACC Score --> ", (acc)
    print "GAIN --> %0.2f%% " % (100.0 * (acc - accBaseline) / accBaseline)

    return acc, sf1, wf1, 

def classify(clf, X, y, CV, nJobs, tryToMeasureFeatureImportance=False):

    # http://scikit-learn.org/stable/modules/naive_bayes.html#naive-bayes   ---> clf = GaussianNB()
    #http://scikit-learn.org/dev/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression ---> clf = LogisticRegression()
    #http://scikit-learn.org/dev/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC ---> clf = SVC(kernel=parameters["kernel"], cache_size=parameters["cacheSize"], C=parameters["C"])
    #http://scikit-learn.org/dev/modules/generated/sklearn.neighbors.KNeighborsClassifier.html ---> clf = KNeighborsClassifier(n_neighbors=parameters["K"])
    #http://scikit-learn.org/dev/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier ---> clf = DecisionTreeClassifier(random_state=0, compute_importances=True)
    # http://scikit-learn.org/dev/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html ---> ExtraTreesClassifier(random_state=0, compute_importances=True, n_jobs=parameters["nJobs"], n_estimators=parameters["n_estimators"])

    print clf
    nSamples, nFeatures = X.shape

    kFold = cross_validation.KFold(n=nSamples, n_folds=CV, indices=True)

    # Run classifier
    lists = [clf.fit(X[train], y[train]).predict(X[test]) for train, test in kFold]
    
    y_pred = []
    for l in lists:
        y_pred += list(l)
    
    scores = cross_validation.cross_val_score(clf, X, y, cv=CV, n_jobs=nJobs) #, scoring="f1") 
    if tryToMeasureFeatureImportance:
        measureFeatureImportance(clf)

    print "Done"
    return y_pred

#llq -> listOfListOfQueries
def classifyIncremental(clf, X, listOfLists, y, CV, nJobs, tryToMeasureFeatureImportance=False):
    
    print clf
    nSamples, nFeatures = X.shape

    for l in listOfLists:
        print "l = ",l.shape
    print "x = ", X.shape
    print "y = ", y.shape

    kFold = cross_validation.KFold(n=nSamples, n_folds=CV, indices=True)

    # Run classifier
    #lists = [clf.fit(X[train], y[train]).predict(X[test]) for train, test in kFold]
    results = defaultdict(list)
    for train, test in kFold:
        for i, l in zip(range(len(listOfLists)), listOfLists):
            results[i] += list(clf.fit(X[train], y[train]).predict(l[test]))

    scores = cross_validation.cross_val_score(clf, X, y, cv=CV, n_jobs=nJobs) #, scoring="f1") 
    if tryToMeasureFeatureImportance:
        measureFeatureImportance(clf)

    print "Result size = ", len(results)
    print "Done"
    return results

def measureFeatureImportance(classifier):
    
    import numpy as np
    importances = classifier.feature_importances_
    std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print "Feature ranking:"

    for f in xrange(len(indices)):
        print "%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]])
    
    # Plot the feature importances of the forest
    #import pylab as pl
    #pl.figure()
    #pl.title("Feature importances")
    #pl.bar(xrange(len(indices)), importances[indices],
    #          color="r", yerr=std[indices], align="center")
    #pl.xticks(xrange(len(indices)), indices)
    #pl.xlim([-1, len(indices)])
    #pl.show()
