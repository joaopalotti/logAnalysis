
#from nltk import word_tokenize, wordpunct_tokenize
from nltk.tokenize.punkt import PunktWordTokenizer

PATH_TO_AUX_FILES = "auxFiles/"

def tokenize(keywordList):
    # split query into words and eliminate blank spaces
    
    #return [ w.strip().lower() for w in keywordList.split(" ") if w.strip() ]
    #return [ w.strip().lower() for w in nltk.wordpunct_tokenize(keywordList) if w.strip() ]
    return [ w.strip().lower() for w in PunktWordTokenizer().tokenize(keywordList) if w.strip() ]
    
def tokenizeAllData(data):
    
    for member in data:
        member.keywords = tokenize(member.keywords)
        if member.previouskeywords:
            member.previouskeywords = tokenize(member.previouskeywords)
    return data

def filterStopWords(data):
    
    stopWords = set()
    #Using as reference: http://jmlr.csail.mit.edu/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
    with open(PATH_TO_AUX_FILES + "stopWords.txt","r") as f:
        for line in f:
            stopWords.add(line.strip())

    for member in data:
        noStopWords = [ keyword for keyword in member.keywords if keyword not in stopWords]
        member.keywords = noStopWords[:]
        if member.previouskeywords:
            noStopWords = [ keyword for keyword in member.previouskeywords if keyword not in stopWords]
            member.previouskeywords = noStopWords[:]

    return data

def compareSets(set1, set2):
    #print "Comparing ", set1, " and ", set2
    #numberOfExpansions, numberOfShrinkage, numberOfReformulations, numberOfRepetitions
    if set1 == set2:
        return 0,0,0,1
    elif set1 > set2:
        return 0,1,0,0
    elif set1 < set2:
        return 1,0,0,0
    else: 
        return 0,0,1,0
 

def preProcessData(data, removeStopWords):
    data = tokenizeAllData(data)
    
    if removeStopWords:
        data = filterStopWords(data)
    
    #Sort Data by id/datetime, just to be sure
    data = sorted(data, key= lambda member: (member.userId, member.datetime))

    return data


