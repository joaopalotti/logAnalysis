from sklearn import cross_validation

def makeReport(X, y, y_pred, baseline):
    
    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    #print "y ===> ", y
    #print "y_pred ===> ", y_pred
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    
    from sklearn.metrics import classification_report, f1_score
    target_names = ['Layman', 'Specialist']
    f1 = f1_score(y[half:], y_pred)
    print(classification_report( y[half:], y_pred, target_names=target_names))
    print "F1 Score --> %.2f" % (f1)
    print "GAIN --> %0.2f%% " % (100.0 * (f1 - baseline) / baseline)

def runNB(X, y, nCV, baseline):
    
    print "Running NB"

    # http://scikit-learn.org/stable/modules/naive_bayes.html#naive-bayes
    n_samples, n_features = X.shape
    half  = int(n_samples/2)

    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    
    from sklearn import metrics
    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV, n_jobs=-1) # in 0.14 i am going to use it: scoring="f1")   
    print "Accuracy NB: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    print "GAIN --> %0.2f%% " % (100.0 * (scores.mean() - baseline) / baseline)

    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])
    
    print "Done"
    return y_pred
 
def runSVM(X, y, parameters, nCV, baseline):
    
    print "Running SVM"
    n_samples, n_features = X.shape
    half = int(n_samples / 2)
    
    from sklearn import svm
    # Run classifier
    clf = svm.SVC(kernel='linear', probability=True)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV, n_jobs=-1,scoring="f1")   
    print "Accuracy SVM: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    print "GAIN --> %0.2f%% " % (100.0 * (scores.mean() - baseline) / baseline)
    
    print "Done"
    return y_pred

def runKNN(X, y, parameters, nCV, baseline):
    #http://scikit-learn.org/dev/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

    print "Running KNN"
    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    from sklearn.neighbors import KNeighborsClassifier
    clf = KNeighborsClassifier(n_neighbors=3)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV, n_jobs=-1)   
    print "Accuracy KNN: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    print "GAIN --> %0.2f%% " % (100.0 * (scores.mean() - baseline) / baseline)
    
    print "Done"
    return y_pred

def runDecisionTree(X, y, parameters, nCV, baseline):
    #http://scikit-learn.org/dev/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

    print "Running Decision Tree"
    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(random_state=0)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV, n_jobs=-1)   
    print "Accuracy DT: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    print "GAIN --> %0.2f%% " % (100.0 * (scores.mean() - baseline) / baseline)
    
    print "Done"
    return y_pred

def runExtraTreeClassifier(X, y, parameters, nCV, baseline):

    print "Running Extremely Randomized Trees"
    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    from sklearn.ensemble import ExtraTreesClassifier
    clf = ExtraTreesClassifier(random_state=0, compute_importances=True)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV, n_jobs=-1)   
    print "Accuracy eRT: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    print "GAIN --> %0.2f%% " % (100.0 * (scores.mean() - baseline) / baseline)
   
    measureFeatureImportance(clf)
    print "Done"
    return y_pred


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
    import pylab as pl
    pl.figure()
    pl.title("Feature importances")
    pl.bar(xrange(len(indices)), importances[indices],
              color="r", yerr=std[indices], align="center")
    pl.xticks(xrange(len(indices)), indices)
    pl.xlim([-1, len(indices)])
    pl.show()
