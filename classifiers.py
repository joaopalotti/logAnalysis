from sklearn import cross_validation

def makeReport(X, y, y_pred):
    
    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    #print "y ===> ", y
    #print "y_pred ===> ", y_pred
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html#sklearn.metrics.classification_report
    
    from sklearn.metrics import classification_report
    target_names = ['Layman', 'Specialist']
    print(classification_report( y[half:], y_pred, target_names=target_names))

def runNB(X, y, nCV):
    # http://scikit-learn.org/stable/modules/naive_bayes.html#naive-bayes
    n_samples, n_features = X.shape
    half  = int(n_samples/2)

    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB()
    
    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV)   
    print "Accuracy NB: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])
    return y_pred
 
def runSVM(X, y, parameters, nCV):
    
    n_samples, n_features = X.shape
    half = int(n_samples / 2)
    
    from sklearn import svm
    # Run classifier
    clf = svm.SVC(kernel='linear', probability=True)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV)   
    print "Accuracy SVM: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    
    return y_pred

def runKNN(X, y, paramters, nCV):
    #http://scikit-learn.org/dev/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    from sklearn.neighbors import KNeighborsClassifier
    clf = KNeighborsClassifier(n_neighbors=3)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV)   
    print "Accuracy KNN: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    
    return y_pred

def runDecisionTree(X, y, paramters, nCV):
    #http://scikit-learn.org/dev/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

    n_samples, n_features = X.shape
    half = int(n_samples / 2)

    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(random_state=0)
    y_pred = clf.fit(X[:half], y[:half]).predict(X[half:])

    scores = cross_validation.cross_val_score(clf, X, y, cv=nCV)   
    print "Accuracy DT: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() / 2)
    
    return y_pred

