
class ResultMetrics:
    def __init__(self, acc, sf1, mf1, wf1):
        self.acc = acc
        self.sf1 = sf1
        self.mf1 = mf1
        self.wf1 = wf1

def calculateBaselines(y, y_greatest):
    from sklearn.metrics import f1_score, accuracy_score

    accBaseline = accuracy_score(y, y_greatest)
    print "Avg. ACC of the greatest dataset => %.3f" % (100.0 * accBaseline)

    f1 = f1_score(y, y_greatest, average=None)
    print "F1 Score --> ", f1, " size --> ", len(f1)

    sf1Baseline = f1_score(y, y_greatest) # TODO: maybe? , pos_label=greatestClass)
    print "Simple F1 -> %.3f" % (100.0 * sf1Baseline)

    mf1Baseline = f1.mean()
    print "Mean F1 -> %.3f" % (100.0 * mf1Baseline)

    from collections import Counter
    ns = Counter(y)
    wf1Baseline = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    print "Weighted F1 -> %.3f" % (100.0 * wf1Baseline)

    return ResultMetrics(accBaseline, sf1Baseline, mf1Baseline, wf1Baseline)


def preprocessing(X_noProcess, method):
    if X_noProcess == []:
        return []
    # http://scikit-learn.org/stable/modules/preprocessing.html
    from sklearn import preprocessing
    if method == "standard":
        X = preprocessing.StandardScaler().fit_transform(X_noProcess)
    elif method == "scale":
        X = preprocessing.scale(X_noProcess)
    elif method == "minmax":
        X = preprocessing.MinMaxScaler().fit_transform(X_noProcess)
    elif method == "normalize":
        X = preprocessing.normalize(X_noProcess, norm='l2')
    elif method == "nothing":
        X = X_noProcess
    else:
        print "INVALID PROCESSING METHOD!"
        from sys import exit
        exit(0)
    return X

def shuffleIndices(nSamples, nSeed):
    import random
    p = range(nSamples) 
    random.seed(nSeed)
    random.shuffle(p)
    return p

def vectorizeData(listOfDicts):
    from sklearn.feature_extraction import DictVectorizer
    vec = DictVectorizer()
    if listOfDicts == []:
        return vec, []
    X_noProcess = vec.fit_transform(listOfDicts).toarray()
    return vec, X_noProcess

def hasherData(listOfDicts):
    from sklearn.feature_extraction import FeatureHasher
    vec = FeatureHasher()
    X_noProcess = vec.transform(listOfDicts)
    print X_noProcess
    return vec, X_noProcess

def tfidfVectorizeData(listOfSentences, useHashTable=False, nFeatures=100):
    
    if useHashTable:
        from sklearn.feature_extraction.text import HashingVectorizer
        vec = HashingVectorizer(stop_words='english', non_negative=True, n_features=nFeatures)
        X_noProcess = vec.transform(listOfSentences).toarray()
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
        X_noProcess = vec.fit_transform(listOfSentences).toarray()

    return vec, X_noProcess

