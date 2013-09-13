#Report
from sklearn import cross_validation
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_recall_curve, auc, roc_curve
# Searching parameters
from sklearn.grid_search import GridSearchCV
#General
from collections import Counter, defaultdict
from auxClassifier import ResultMetrics

def makeIncrementalReport(X, y, listOfYs, accBaseline, sf1Baseline, wf1Baseline, mf1Baseline):
    a, f, wf, mf = [], [], [], []
    for i in listOfYs:
        print "Partition ", i
        print len(listOfYs[i])
        #print listOfYs[i]
        acc, sf1, wf1, mf1 = makeReport(X, y, listOfYs[i], accBaseline, sf1Baseline, wf1Baseline, mf1Baseline)
        a, f, wf, mf = a + [acc], f + [sf1], wf + [wf1], mf + [mf1]
    return a, f, wf, mf

def makeReport(X, y, y_pred, baselines, target_names=['Layman', 'Specialist']):
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred, average=None)
    # Simple F1 calculated by the f1 function
    sf1 = f1_score(y, y_pred)
    # Mean F1 ==> (F1(c1) + F1(c2)) / 2 
    mf1 = f1.mean()
    # Weighted F1
    ns = Counter(y)
    wf1 = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    
    print(classification_report(y, y_pred, target_names=target_names))
    
    print "F1 Scores (no average) --> ", (f1)
    
    print "sf1 -> ", sf1
    print "GAIN --> %0.2f%% " % (100.0 * (sf1 - baselines.sf1) / baselines.sf1)
    
    print "mf1 -> ", mf1
    print "GAIN --> %0.2f%% " % (100.0 * (mf1 - baselines.mf1) / baselines.mf1)
    
    print "wf1 -> ", wf1
    print "GAIN --> %0.2f%% " % (100.0 * (wf1 - baselines.wf1) / baselines.wf1)
    
    print "ACC Score --> ", (acc)
    print "GAIN --> %0.2f%% " % (100.0 * (acc - baselines.acc) / baselines.acc)

    return ResultMetrics(acc, sf1, mf1, wf1)

def convertToSingleList(listOfLists):
    result = []
    for l in listOfLists:
        result += list(l)
    return result

def runClassifier(clf, X, y, CV, nJobs, others={}):

    tryToMeasureFeatureImportance = False if "tryToMeasureFeatureImportance" not in others else others["tryToMeasureFeatureImportance"]
    featureNames = None if "featureNames" not in others else others["featureNames"]
    useGridSearch= False if "useGridSearch" not in others else others["useGridSearch"]
    gridParameters= None if "gridParameters" not in others else others["gridParameters"]
    gridScore= "f1" if "gridScore" not in others else others["gridScore"]
   
    if tryToMeasureFeatureImportance and useGridSearch:
        print "Using Grid search and feature importance at the same time is not a good idea"
        print "Disabling feature importance"
        tryToMeasureFeatureImportance = False

    print "OTHERS ==> ", others
    print clf
    originalClf = clf
    if useGridSearch:
        print "Using grid search"
        clf = GridSearchCV(clf, gridParameters, cv=CV, scoring=gridScore, n_jobs=nJobs)

    nSamples, nFeatures = X.shape

    kFold = cross_validation.KFold(n=nSamples, n_folds=CV, indices=True)

    probas = []
    preds = []
    # Run classifier
    for train, test in kFold:
        preds.append( clf.fit(X[train], y[train]).predict(X[test]) )
        probas.append( clf.fit(X[train], y[train]).predict_proba(X[test]) )
        if useGridSearch:
            print("Best parameters set found on development set:")
            print()
            print(clf.best_estimator_)
            print()
            print("Grid scores on development set:")
            print()
            for params, mean_score, scores in clf.grid_scores_:
                print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))
            print()

    y_probas = convertToSingleList(probas)
    y_pred = convertToSingleList(preds)
    
    #scores = cross_validation.cross_val_score(clf, X, y, cv=CV, n_jobs=nJobs) #, scoring="f1") 
    if tryToMeasureFeatureImportance:
        measureFeatureImportance(originalClf, featureNames)

    print "Done"
    return y_pred, y_probas

def classify(clf, label, X, y, nCV, nJobs, baselines, options={}):
    print "Running ", label
    y_ ,probas_ = runClassifier(clf, X, y, nCV, nJobs, options)
    resultMetrics = makeReport(X, y, y_, baselines)
    precRecall = getPrecisionRecall(y, probas_)
    roc = getROC(y, probas_)
    return (label, resultMetrics, precRecall, roc)

def parallelClassify(pars):
    
    print "SIZE = ", len(pars)
    if len(pars) > 6:
        print "FOUND THE DICTIONARY HERE"
        return classify(pars[0], pars[1], pars[2], pars[3], pars[4], pars[5], pars[6], pars[7])
    else:
        return classify(pars[0], pars[1], pars[2], pars[3], pars[4], pars[5], pars[6], {})

#llq -> listOfListOfQueries
def classifyIncremental(clf, X, listOfLists, y, CV, nJobs, tryToMeasureFeatureImportance=False, featureNames=None):
    
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
        measureFeatureImportance(clf, featureNames)

    print "Result size = ", len(results)
    print "Done"
    return results

def plotGraph(precRecallDict, fileName, xlabel, ylabel, generatePickle=True, hasPlotLibs=False):
    if generatePickle:
        import pickle
        with open(fileName + ".pk", 'wb') as output:
            pickle.dump(precRecallDict, output, pickle.HIGHEST_PROTOCOL)
    
    if not hasPlotLibs:
        return

    import matplotlib.pylab as plt
    
    for title, yx in precRecallDict.items():
        plt.plot(yx[1], yx[0], label=title)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    #plt.legend(loc=2)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

    if fileName:
        plt.savefig(fileName + ".eps" , papertype="a4", orientation="portrait")
    else:
        plt.show()
    
    plt.close()

def getPrecisionRecall(y, probas):

    probas1 = [p[1] for p in probas]
    
    precision, recall, thresholds = precision_recall_curve(y, probas1)
    area = auc(recall, precision)
    print "Area Under Curve: %0.2f" % area
    print "thresholds = ", thresholds
    return (precision, recall)
   
def getROC(y, probas):
    
    probas1 = [p[1] for p in probas]
    
    fpr, tpr, thresholdsROC = roc_curve(y, probas1)
    roc_auc = auc(fpr, tpr)
    print("Area under the ROC curve : %f" % roc_auc)
    print "thresholdsROC = ", thresholdsROC
    print "Probas ===> ", probas
    print "Fpr -> ", fpr, "tpr -> ", tpr

    return (tpr, fpr)

def getCurves(results):
    precRecall, roc = {}, {}
    for r in results:
        precRecall[ r[0] ] = r[2]
        roc[ r[0] ] = r[3]
    return precRecall, roc

def measureFeatureImportance(classifier, featureNames):
    
    import numpy as np
    importances = classifier.feature_importances_
    std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print "Feature ranking:"

    for f in xrange(len(indices)):
        if featureNames:
            print "%d. feature %s (%f)" % (f + 1, featureNames[indices[f]], importances[indices[f]])
        else:
            print "%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]])
