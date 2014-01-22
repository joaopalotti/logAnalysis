import pandas as pd
import numpy as np

PATH="../logAnalysisDataSets/"

# Get data
colnames = ["date", "userid", "keywords", "pkeywords", "mesh", "semantics", "chvs", "layterm", "expterm", "misspelled", "combo", "sources", "pos", "concepts"]
hon = pd.read_csv("hon/hon1.gz", compression="gzip", names=colnames)
trip = pd.read_csv("hon/trip1.gz", compression="gzip", names=colnames)


# Create list of words used by each user
honuk = hon.groupby("userid").apply(lambda u:list(u["keywords"]))
tripuk = trip.groupby("userid").apply(lambda u:list(u["keywords"]))

# concatenation of y's and x's (HON -> 0, TRIP -> 1)
y = np.concatenate((np.zeros(honuk.shape[0]), np.ones(tripuk.shape[0])))
uks = pd.concat((honuk, tripuk))

from sklearn.cross_validation import KFold
kf = KFold(y.shape[0], n_folds=5)

from nltk import word_tokenize
for train_index, test_index in kf:
    y_train, y_test = y[train_index], y[test_index]
    train_voc = [token for sublist in uks[train_index] for query in sublist for token in word_tokenize(query)]
    test_voc = [token for sublist in uks[test_index] for query in sublist for token in word_tokenize(query)]

