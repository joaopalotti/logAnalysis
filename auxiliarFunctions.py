
#from nltk import word_tokenize, wordpunct_tokenize
from nltk.tokenize.punkt import PunktWordTokenizer

PATH_TO_AUX_FILES = "auxFiles/"

NLWords = ["would", "wouldn't", "wouldnt", "could", "couldn't", "couldnt", "should", "shouldn't", "shouldnt", "how", "when", "where", "which", "who", "whom", "can", "cannot", "why", "what", "we", "they", "i", "do", "does", "must", "ought"]


def createAcronymSet():
    acronymsSet = set()
    #http://en.wikipedia.org/wiki/List_of_acronyms_for_diseases_and_disorders
    #http://en.wikipedia.org/wiki/List_of_abbreviations_for_medical_organisations_and_personnel
    #http://en.wikipedia.org/wiki/Acronyms_in_healthcare
    #http://en.wikipedia.org/wiki/List_of_medical_abbreviations -- From A to Z

    for filename in [ "diseasesAcronyms.txt", "healthCareAcronyms.txt", "organizationAcronyms.txt", "medicalAbbreviations.txt" ]:
        with open(PATH_TO_AUX_FILES + filename,"r") as f:
            for line in f.readlines():
                acronymsSet.add( (line.split(",", 1)[0].strip()).lower() )
   
    # Remove very common words from acronyms:
    commonWordsSet = set(["and", "on", "map", "is", "car", "at", "san", "art", "from", "air", "la", "des", "en", "le", "les", "y", "e", "or", "vs", "help", "charge", "has", "l", "los", "non", "do", "las", "dr", "as", "be", "dos", "men", "con", "no", "who", "ppt", "us", "bad","all","msn","fish","pet","gas","camp","dvd","rv","ass","cat","god","sample","gift","sign","if","anna","was","don","cd","abc","t","s","ca","fl","va","inc","co","it","st","nc","top","ma","tips","soap","rice","stop","aid","mom","fast","his","cold","india","see","ten","rap","toe","add","bat","got","tee","bra","lab"])
    americanStates = set(["us", "al", "ak", "az", "ar","ca","co","ct","de","fl","ga","hi","ha","cl","cf","id","il","in","ia","ks","ka","ky","la","me","md","ma","mi","ms","mc","mn","mo","mt","ne","nb","nv","nh","nj","ny","nm","nc","nd","oh","ok","or","pa","ri","sc","sd","tx","tn","ut","vt","va","wa","wv",",wn","wi","wy","as","gu","mp","pr","vi","um","fm","mh","pw","aa","ae","ap","cm","cz","nb","pi","tt"])
    oneLetter=set(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    
    acronymsSet -= commonWordsSet
    acronymsSet -= americanStates
    acronymsSet -= oneLetter
    return acronymsSet

    
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

def simpleFilterStopWords(countingTokens):
    from operator import itemgetter
    tenMostCommonTerms = {}

    stopWords = set()
    #Using as reference: http://jmlr.csail.mit.edu/papers/volume5/lewis04a/a11-smart-stop-list/english.stop
    with open(PATH_TO_AUX_FILES + "stopWords.txt","r") as f:
        for line in f:
            stopWords.add(line.strip())
    
    for pair in countingTokens.most_common():
        if pair[0] not in stopWords:
            tenMostCommonTerms[pair[0]] = pair[1]
        
        if len(tenMostCommonTerms) == 15: # taking the 15 first terms instead of the top 10
            return sorted( tenMostCommonTerms.iteritems(), key=itemgetter(1) ) #sorting by value

    if len(tenMostCommonTerms) == 0:
        return {}
    return sorted(tenMostCommonTerms.iteritems(), key=itemgetter(1), reverse=True ) #sorting by value

def compareSets(set1, set2):
    #print "Comparing ", set1, " and ", set2
    #print "set1 == set2 --> " , set1 == set2
    #print "set1 > set2 --> " , set1 > set2
    #print "set1 < set2 --> " , set1 < set2
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

#TODO: checkar isso aqui
"""
    Some important semantic types (list: http://metamap.nlm.nih.gov/SemanticTypeMappings_2011AA.txt)
    http://www.nlm.nih.gov/research/umls/META3_current_semantic_types.html  ---> semantic trees

        -> Symptom              -> sosy (Sign or Symptom), lbtr (Laboratory or Test Result)
        
        -> Source                -> bact (Bacterium), virs (Virus), Fungs (fngs), Archaeon (arch)
        
        -> (Cause) Disease/Dysfunction  -> dsyn (Disease or Syndrome), mobd (Mental or Behavioral Dysfunction), neop (Neoplastic Process), patf (Pathologic Function)
        -> Cure                 -> clnd (Clinical Drug), amas (Amino Acid Sequence ?), antb (Antibiotic), aapp(Amino Acid, Peptide, or Protein?), phsu (Pharmacologic Substance), imft (Immunologic Factor - vaccine, e.g.), vita (Vitamin)

        -> Prevention?

        -> where     -> bpoc (Body Part, Organ, or Organ Component), bsoj (Body Space or Junction), tisu (tissue), bdsy (Body System), blor (Body Location or Region)

        ->>> Important and missing classification: inpo (Injury or Poisoning),  diap (Diagnostic Procedure), irda (Indicator, Reagent, or Diagnostic Aid), fndg (Finding), ftcn (Functional Concept), gngm (Gene or Genome), hcro (Health Care Related Organization), hlca (Health Care Activity), horm|Hormone, inch|Inorganic Chemical, lbpr|Laboratory Procedure
"""

def symptomTypes():
    return ["sosy","lbtr"] 

def sourceTypes():
    return ["bact", "virs", "fngs", "arch"] 

def causeTypes():
    return ["dsyn", "mobd", "neop","patf"]

def remedyTypes():
    return ["clnd", "amas", "antb","aapp","phsu","imft","vita"]

def whereTypes():
    return ["bpoc", "bsoj","tisu","bdsy","blor"]

def noMedicalTypes():
    return ["mnob","geoa","rnlw", "inpr", "idcn", "spco", "cnce", "orgt"]
    # mnob|Manufactured Object;  geoa|Geographic Area; inpr|Intellectual Product; qlco|Qualitative Concept; qnco|Quantitative Concept; ftcn|Functional Concept; idcn|Idea or Concept ; popg|Population Group; spco|Spatial Concept; cnce|Conceptual Entity; orgt|Organization

