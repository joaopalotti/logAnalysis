import pickle, sys
import random
import numpy as np
from optparse import OptionParser
from collections import Counter, defaultdict
#Classifiers
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
#Auxiliars
from sklearn.feature_extraction import DictVectorizer
#My classes
from classifiers import classify, classifyIncremental, makeReport, makeIncrementalReport
from createFeatureVector import userClass
from sklearn.metrics import f1_score, accuracy_score

### HOW TO USE:
# python runClassifiers.py -h
# python runClassifiers.pt --preprocessing=[normalize|scale|minmax|nothing] [forceBalance|-1] [proportional|-1] [minNumberOfQueries] [nseed]"

nJobs = 2
nCV = 10
CSVM = 10000
percentageIntervals = [0,10,20,30,40,50,60,70,80,90,100]
classifyParameters = {"KNN-K": 100, "ERT-n_estimators": 10, "SVM-cacheSize": 1000, "SVM-kernel": "linear", "SVM-C": CSVM} 

#ld1, listOfListOfQueries1, ll1 = transformeInDict(regularUserFV, n, proportional)
def transformeInDict(userDict, n=-1, proportional=-1):
    listOfDicts = list()
    listOfLastQueries = list() # the last query has the "accumlated value for a user"
    listOfLabels = list()

    allUserIds = sorted([u for u in userDict])

    p = range(len(allUserIds))
    random.shuffle(p)
    if proportional:
        n = int( int(proportional)/100.0 * len(allUserIds) )

    #for v, (key, user) in zip(range(len(p)), userDict.iteritems()):
    for v, userId in zip(p, allUserIds):
        if n >= 0 and v >= n:
            continue 

        listOfQueries = userDict[userId]

        listOfLastQueries.append(listOfQueries[-1].toDict())
        listOfDicts.append(listOfQueries)
        listOfLabels.append(listOfQueries[0].label)

    #Returning a list of list of queries of a single user and list of labels
    return listOfLastQueries, listOfDicts, listOfLabels

def plotResult(clf, intervals, accs, f1s, wf1s, mf1s, accBaseline, f1Baseline, wf1Baseline, mf1Baseline):
    import pylab as pl
    pl.clf()
    pl.plot(intervals, accs, 'ro', label='Acc training')
    pl.plot([intervals[0],intervals[-1]], [accBaseline,accBaseline], 'r-', label='Acc baseline')
    
    pl.plot(intervals, f1s, 'bo', label='sF1 training')
    pl.plot([intervals[0],intervals[-1]], [f1Baseline,f1Baseline], 'b-', label='sF1 baseline')

    pl.plot(intervals, mf1s, 'co', label='mF1 training')
    pl.plot([intervals[0],intervals[-1]], [mf1Baseline,mf1Baseline], 'c-', label='mF1 baseline')
    
    pl.plot(intervals, wf1s, 'go', label='wF1 training')
    pl.plot([intervals[0],intervals[-1]], [wf1Baseline,wf1Baseline], 'g-', label='wF1 baseline')

    pl.xlabel('Training Percentage')
    pl.ylabel('Metric')
    pl.ylim([0.0, 1.00])
    pl.xlim([intervals[0], intervals[-1]])
    pl.title('Incremental Training for %s' % clf)
    pl.legend(loc="lower left")
    #pl.show()
    pl.savefig(str(clf).split("(")[0] + ".png")

def applyPreProcessing(data, preProcessing):
    from sklearn import preprocessing
    if preProcessing == "scale":
        X = preprocessing.scale(data)
    elif preProcessing == "minmax":
        X = preprocessing.MinMaxScaler().fit_transform(data)
    elif preProcessing == "normalize":
        X = preprocessing.normalize(data, norm='l2')
    elif preProcessing == "nothing":
        X = data
    return X

def getSubLists(l, method, values, vec, preProcessing):
    result = defaultdict(list)

    for subList in l:
        for i, v in zip(range(len(values)), values):
            if method == "integral":
                result[i].append(subList[v].toDict())
                #print i, v, subList[v].toDict()
            if method == "percentage":
                result[i].append(subList[int((len(subList) - 1) * (v/100.0))].toDict())
                #print len(subList), v, int(len(subList) * (v/100.0) )

    return [applyPreProcessing(vec.fit_transform(result[l]).toarray(), preProcessing) for l in result]

def runClassify(preProcessing, forceBalance, proportional, minNumberOfQueries, nseed, useIntegral):
   
    medicalUserDataSet = "medicalUser-%d.pk" % (minNumberOfQueries)
    regularUserDataSet = "regularUser-%d.pk" % (minNumberOfQueries)
    
    healthUserDataSet = "healthUser-%d.pk"   % (minNumberOfQueries)
    notHealthUserDataSet = "notHealthUser-%d.pk" % (minNumberOfQueries)

    print "using seed -> ", nseed

    print preProcessing
    if forceBalance > 0:
        print "Forcing only %s examples for each dataset" % (forceBalance)

    if proportional > 0:
        print "Using proportional representation. %s percente of the base." % (proportional)
    
    if forceBalance > 0 and proportional > 0:
        print "ERROR! YOU SHOULD CHOOSE OR FORCEBALANCE OR PROPORTIONAL DATA!"

    ####
    ### Load Datasets
    ##
    #
    print "Loading the datasets..."
    with open(regularUserDataSet, 'rb') as input:
    #with open(notHealthUserDataSet, 'rb') as input:
        regularUserFV = pickle.load(input)
    
    with open(medicalUserDataSet, 'rb') as input:
    #with open(healthUserDataSet, 'rb') as input:
        medicalUserFV = pickle.load(input)
    print "Loaded"

    n = -1
    if int(forceBalance) > 0:
        n = int(forceBalance)

    print "Transforming datasets into Dictionaries..."
    ld1, listOfListOfQueries1, ll1 = transformeInDict(regularUserFV, n, proportional)
    ld2, listOfListOfqueries2, ll2 = transformeInDict(medicalUserFV, n, proportional)
    print "Transformed"
    
    listOfFinalState = ld1 + ld2
    listOfLabels = ll1 + ll2
    listOfListsOfQueries = listOfListOfQueries1 + listOfListOfqueries2
    
    y = np.array( listOfLabels )
    listOfListsOfQueries = np.array(listOfListsOfQueries)
    
    greatestClass = 0 if len(ll1) > len(ll2) else 1
    y_greatest =  np.array((len(ll1) + len(ll2)) * [greatestClass] )

    print "Using %d regular users -- class %s" % (len(ld1), ll1[0])
    print "Using %d medical users -- class %s" % (len(ld2), ll2[0])
    
    accBaseline = accuracy_score(y, y_greatest)
    print "Avg. ACC of the greatest dataset => %.3f" % (100.0 * accBaseline)

    f1 = f1_score( y, y_greatest, average=None)
    print "F1 Score --> ", (f1) , " size --> ", len(f1)
    
    sf1Baseline = f1_score( y, y_greatest)
    print "Simple F1 -> %.3f" % (sf1Baseline)
    
    mf1Baseline = f1.mean()
    print "Mean F1 -> %.3f" % (mf1Baseline)
    
    ns = Counter(y)
    wf1Baseline = ( f1[0] * ns[0] + f1[1] * ns[1] ) / (ns[0] + ns[1])
    print "Weighted F1 -> ", wf1Baseline

    print "Vectorizing dictionaries..."
    vec = DictVectorizer()
    X_noProcess = vec.fit_transform(listOfFinalState).toarray()
    print vec.get_feature_names()
    print "Vectorized"
    
    # http://scikit-learn.org/stable/modules/preprocessing.html
    X = applyPreProcessing(X_noProcess, preProcessing)
   
    if useIntegral:
        integralList = getSubLists(listOfListsOfQueries, "integral", range(0,5), vec, preProcessing)
    else:
        percentageList = getSubLists(listOfListsOfQueries, "percentage", percentageIntervals, vec, preProcessing)

    n_samples, n_features = X.shape    
    ####
    ### Shuffer samples
    ##
    #
    print "Shuffling the data..."
    # Shuffle samples
    p = range(n_samples) 
    random.seed(nseed)
    random.shuffle(p)

    nCV = 5
    print "Shuffled"

    ####
    ### Run classifiers
    ##
    #
    clfs = [GaussianNB(), ExtraTreesClassifier(random_state=0, compute_importances=True, n_jobs=nJobs, n_estimators=classifyParameters["ERT-n_estimators"]), KNeighborsClassifier(n_neighbors=classifyParameters["KNN-K"]), DecisionTreeClassifier(random_state=0, compute_importances=True), LogisticRegression(), SVC(kernel=classifyParameters["SVM-kernel"], cache_size=classifyParameters["SVM-cacheSize"], C=classifyParameters["SVM-C"]) ]

    print "Running classifiers..."
    for clf in clfs:
        if useIntegral:
            y_nbInc = classifyIncremental(clf, X, integralList, y, nCV, nJobs)
        else:
            y_nbInc = classifyIncremental(clf, X, percentageList, y, nCV, nJobs)

        print 20 * '=', " Results ", 20 * '='
        accs, f1s, wf1s, mf1 = makeIncrementalReport(X, y, y_nbInc, accBaseline, sf1Baseline, wf1Baseline, mf1Baseline)
        
        if useIntegral:
            plotResult(clf, range(0,5), accs, f1s, wf1s, mf1, accBaseline, sf1Baseline, wf1Baseline, mf1Baseline)
        else:
            plotResult(clf, percentageIntervals, accs, f1s, wf1s, mf1, accBaseline, sf1Baseline, wf1Baseline, mf1Baseline)

    print "Done"

if __name__ == "__main__":
    
    op = OptionParser(version="%prog 2")
    op.add_option("--preprocessing", "-p", action="store", type="string", dest="preProcessing", help="Preprocessing option [normalize|scale|minmax|nothing] --  [default: %default]", metavar="OPT", default="normalize")
    op.add_option("--forceBalance", "-b", action="store", type="int", dest="forceBalance", help="Force balance keeping only X instances of each class.", metavar="X", default=-1)
    op.add_option("--proportional", "-g", action="store", type="int", dest="proportional", help="Force proportion of the data to X%.", metavar="X", default=-1)
    op.add_option("--minNumberOfQueries", "-m", action="store", type="int", dest="minNumberOfQueries", help="Define the min. number of queries (X) necessary to use a user for classification.  [default: %default]", metavar="X", default=5)
    op.add_option("--nseed", "-s", action="store", type="int", dest="nseed", help="Seed used for random processing during classification.  [default: %default]", metavar="X", default=29)
    op.add_option("--integral", "-i", action="store_true", dest="integral", help="Integral intervals instead of percentages. [default: %default]", default=False)

    (opts, args) = op.parse_args()
    if len(args) > 0:
        print "This program does not receive parameters this way: use -h to see the options."
        sys.exit(0)
    
    print "Using preprocessing: ", opts.preProcessing
    runClassify(opts.preProcessing, opts.forceBalance, opts.proportional, opts.minNumberOfQueries, opts.nseed, opts.integral)

