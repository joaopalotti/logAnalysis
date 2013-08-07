

def preprocessing(X_noProcess, method):
    # http://scikit-learn.org/stable/modules/preprocessing.html
    from sklearn import preprocessing
    if method == "scale":
        X = preprocessing.scale(X_noProcess)
    elif method == "minmax":
        X = preprocessing.MinMaxScaler().fit_transform(X_noProcess)
    elif method == "normalize":
        X = preprocessing.normalize(X_noProcess, norm='l2')
    elif method == "nothing":
        X = X_noProcess
    return X

def shuffleData(X, y, nSeed, nSamples):
    p = range(nSamples) 
    random.seed(nSeed)
    random.shuffle(p)
    return X[p], y[p]

def vectorizeData(listOfDicts):
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    X_noProcess = vec.fit_transform(listOfDicts).toarray()
    return vec, X_noProcess

