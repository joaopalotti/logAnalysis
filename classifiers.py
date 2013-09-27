import logging
#Report
from sklearn import cross_validation
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_recall_curve, auc, roc_curve
# Searching parameters
from sklearn.grid_search import GridSearchCV
#General
from collections import Counter, defaultdict
from auxClassifier import ResultMetrics

moduleL = logging.getLogger("classifiers.py")

def makeIncrementalReport(y, listOfYs, baselines):
    a, f, wf, mf = [], [], [], []
    for i in listOfYs:
        print "Partition ", i
        print len(listOfYs[i])
        #print listOfYs[i]
        tempR = makeReport(y, listOfYs[i], baselines)
        a, f, mf, wf = a + [tempR.acc], f + [tempR.sf1], mf + [tempR.mf1], wf + [tempR.wf1]
    return ResultMetrics(a, f, mf, wf)

def makeReport(y, y_pred, baselines, target_names=['Layman', 'Specialist']):
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
    
    moduleL.info(classification_report(y, y_pred, target_names=target_names))
    
    moduleL.info("F1 Scores (no average) --> %s", (f1))
    moduleL.info("sf1 -> %s", sf1)
    moduleL.info("GAIN --> %0.2f%% " % (100.0 * (sf1 - baselines.sf1) / baselines.sf1))
    moduleL.info("mf1 -> %s", mf1)
    moduleL.info("GAIN --> %0.2f%% " % (100.0 * (mf1 - baselines.mf1) / baselines.mf1))
    moduleL.info("wf1 -> %s", wf1)
    moduleL.info("GAIN --> %0.2f%% " % (100.0 * (wf1 - baselines.wf1) / baselines.wf1))
    moduleL.info("ACC Score --> %s", (acc))
    moduleL.info("GAIN --> %0.2f%% " % (100.0 * (acc - baselines.acc) / baselines.acc))

    return ResultMetrics(acc, sf1, mf1, wf1)

def runClassifier(clf, X, y, CV, nJobs, others={}, incrementalData=None):
 
    moduleL.info("OTHERS ==> %s", others)
    moduleL.info("Classifier ==> %s", clf)

    tryToMeasureFeatureImportance = False if "tryToMeasureFeatureImportance" not in others else others["tryToMeasureFeatureImportance"]
    featureNames = None if "featureNames" not in others else others["featureNames"]
    useGridSearch= False if "useGridSearch" not in others else others["useGridSearch"]
    gridParameters= None if "gridParameters" not in others else others["gridParameters"]
    gridScore= "f1" if "gridScore" not in others else others["gridScore"]
    measureProbas = False if "measureProbas" not in others else others["measureProbas"]
   
    if tryToMeasureFeatureImportance and useGridSearch:
        moduleL.warning("Using Grid search and feature importance at the same time is not a good idea")
        moduleL.warning("Disabling feature importance")
        tryToMeasureFeatureImportance = False

    originalClf = clf
    if useGridSearch:
        moduloL.info("Using grid search")
        clf = GridSearchCV(clf, gridParameters, cv=CV, scoring=gridScore, n_jobs=nJobs)

    nSamples = y.shape[0]

    kFold = cross_validation.KFold(n=nSamples, n_folds=CV, indices=True)

    if incrementalData:
        #moduleL.info("Using incremental data!")
        preds = defaultdict(list)
        probas = defaultdict(list)
    else:
        probas = []
        preds = []

    # Run classifier
    for train, test in kFold:
        if incrementalData:
            for i, l in zip(range(len(incrementalData)), incrementalData):
                preds[i] += list(clf.fit(l[train], y[train]).predict(l[test]))
                if measureProbas:
                    probas[i] += list(clf.fit(l[train], y[train]).predict_proba(l[test]))
        else:
            preds.extend( list(clf.fit(X[train], y[train]).predict(X[test])) )
            if measureProbas:
                probas.extend( list(clf.fit(X[train], y[train]).predict_proba(X[test])))

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

    logging.debug(preds)

    #scores = cross_validation.cross_val_score(clf, X, y, cv=CV, n_jobs=nJobs) #, scoring="f1") 
    if tryToMeasureFeatureImportance:
        measureFeatureImportance(originalClf, featureNames)

    moduleL.info("Done")
    return preds, probas

def classify(clf, label, X, y, nCV, nJobs, baselines, options={}, incremental=None):
    moduleL.info("Running: %s", label)
       
    y_ , probas_ = runClassifier(clf, X, y, nCV, nJobs, options, incremental)
    
    if incremental:
        resultMetrics = makeIncrementalReport(y, y_, baselines)
        precRecall = getPrecisionRecall(y, probas_)
        roc = getROC(y, probas_)
    else:
        resultMetrics = makeReport(y, y_, baselines)
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

def plotGraph(precRecallDict, fileName, xlabel, ylabel, generatePickle=True, hasPlotLibs=False):
    if generatePickle:
        import pickle
        with open(fileName + ".pk", 'wb') as output:
            pickle.dump(precRecallDict, output, pickle.HIGHEST_PROTOCOL)
    
    if not hasPlotLibs:
        return

    import matplotlib.pylab as plt
    
    for title, yx in precRecallDict.items():
        if title == "Random Forest":
            plt.plot(yx[1], yx[0], label="Random Forest (AUC=0.94)")
    
    for title, yx in precRecallDict.items():
        if title != "Random Forest":
            if title == "DummyMostFrequent":
                title = "Most Freq. Class Classifier (AUC=0.50)"
            
            if title == "Naive Bayes":
                title = "Naive Bayes (AUC=0.72)"
            
            if title == "KNN":
                title = "KNN (AUC=0.93)"
            
            if title == "Decision Tree":
                continue
                title = "Decision Tree (AUC=0.81)"
            
            if title == "Logistic Regression":
                title = "Logistic Regression (AUC=0.89)"
            
            if title == "SVM":
                title = "SVM (AUC=0.93)"
            plt.plot(yx[1], yx[0], label=title)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.ylim([0.0, 1.01])
    plt.xlim([0.0, 1.0])
    plt.legend(loc=4)
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True) # upper part
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.00), fancybox=True, shadow=True, ncol=5)

    if fileName:
        plt.savefig(fileName + ".eps" , papertype="a4", orientation="portrait")
    else:
        plt.show()
    
    plt.close()

def getPrecisionRecall(y, probas):
    if not probas:
        return []

    probas1 = [p[1] for p in probas]
    
    precision, recall, thresholds = precision_recall_curve(y, probas1)
    area = auc(recall, precision)
    #print "Area Under Curve: %0.2f" % area
    #print "thresholds = ", thresholds
    return (precision, recall)
   
def getROC(y, probas):
    if not probas:
        return []

    probas1 = [p[1] for p in probas]
    
    fpr, tpr, thresholdsROC = roc_curve(y, probas1)
    roc_auc = auc(fpr, tpr)
    #print("Area under the ROC curve : %f" % roc_auc)
    #print "thresholdsROC = ", thresholdsROC
    #print "Probas ===> ", probas
    #print "Fpr -> ", fpr, "tpr -> ", tpr

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
