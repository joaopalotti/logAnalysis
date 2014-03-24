from datetime import datetime
from collections import defaultdict
import re
import sys
import csv

class DataSet(object):
    """
    This class represents one single row in the data logs, it means one single query made by one user. 
    Among the defined fields there are the userid, keywords used in the query, semantic concepts found, etc.
    """

    # CHVFound -> number of concepts that are in the CHV list
    # hasCHV -> if any of the concepts found are exactly as the CHV suggests
    def __init__(self, dttime, userId, keywords, previouskeywords=None, category=None, publication=None, rank=None, clickurl=None, mesh=None,\
                 semanticTypes=None, usingTimestamp=False, CHVFound=0, hasCHV=False, hasUMLS=False, hasCHVMisspelled=False, comboScore=0,\
                 sourceList=None, postags=None, concepts=None, semanticConcepts=None): 
      
        withMs = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})")
        withMsAndQuote = re.compile("\"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})\"")
        withScs = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})")
        withScsAndQuote = re.compile("\"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\"")

        if dttime:
            if withMs.match(dttime):
                self.datetime = datetime.strptime(dttime, '%Y-%m-%d %H:%M:%S.%f')
            elif withMsAndQuote.match(dttime):
                self.datetime = datetime.strptime(dttime, '"%Y-%m-%d %H:%M:%S.%f"')
            elif withScs.match(dttime):
                self.datetime = datetime.strptime(dttime, '%Y-%m-%d %H:%M:%S')
            elif withScsAndQuote.match(dttime):
                self.datetime = datetime.strptime(dttime, '"%Y-%m-%d %H:%M:%S"')
            elif usingTimestamp:
                self.datetime = datetime.fromtimestamp(float(dttime))
            else:
                print ("ERROR: Invalid date format found! : ", dttime)
                self.datetime = datetime.fromtimestamp(float(0))
                #assert False
        else:
            self.datetime = datetime.fromtimestamp(float(0))
            #assert False

        #userId in the tripdatabase and annonid in AOL
        self.userId = userId
        
        # remove final backslash char that screws the CSV reader
        self.keywords = keywords.rstrip("\\")
        
        # if there is any previous keyword, it removes the final backslash char that screws the CSV reader
        self.previouskeywords = None if not previouskeywords or previouskeywords  == "Null" or previouskeywords == "NULL" else previouskeywords.rstrip("\\")
        
        self.rank = rank if rank else None
        self.clickurl = clickurl if clickurl else None
        self.mesh = mesh.strip().split(";") if mesh else None
        self.semanticTypes = semanticTypes.strip().split(";") if semanticTypes else None

        #These fiels are never used. For now they are not recorded and they will be removed in a future version
        #self.category = category if category else None
        #self.publication = publication if publication else None
        
        if self.semanticTypes is not None:
            if any(s for s in self.semanticTypes if len(s) != 4 ) == True:
                print self.semanticTypes
                assert False

        self.CHVFound = int(CHVFound)
        self.hasCHV = (hasCHV == "True")
        self.hasUMLS = (hasUMLS == "True")
        self.hasCHVMisspelled = (hasCHVMisspelled == "True")
        self.comboScore = float(comboScore)

        self.postags = postags # None is the default
        if postags:
            self.postags = [ p for p in postags.split(";") if p ]
        self.sourceList = sourceList # None is the default
        if sourceList:
            self.sourceList = [ s for s in sourceList.split(";") if s ]
        self.concepts = concepts # None is the default
        if concepts:
            self.concepts = [ c for c in concepts.split(";") if c ]
    
        self.mapSemanticConcepts = self.generateMapOfSemanticTypes(semanticConcepts)
    
    def generateMapOfSemanticTypes(self, row):
        """
        Map each of the concepts found to a semantic type:
            Ex. "test|inpr;lbpr;ftcn|gg|geoa|1+|qnco;clas|food intolerance|sosy|"
            This will generate this dictionary:
                inpr -> 'test'
                sosy -> 'food intolerance'
                ...
        """
        if not row:
            return None
        return_dict = defaultdict(list)
        fields = row.split("|")[0:-1] #Excludes the empty space at the and of the string
        for (keyword, stype) in ((fields[i], fields[i+1]) for i in range(0, len(fields), 2)):
            for t in stype.split(";"):
                return_dict[t].append(keyword)
        return return_dict

    def printMe(self, out=sys.stdout):
        writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
        # Should add here any important information and modify the corresponding readCSV
        mesh = ';'.join(self.mesh) if self.mesh else ''
        semanticTypes = ';'.join(self.semanticTypes) if self.semanticTypes else ''

        writer.writerow( [str(self.datetime), self.userId, self.keywords, self.previouskeywords, mesh, semanticTypes,\
                            self.CHVFound, self.hasCHV, self.hasUMLS, self.hasCHVMisspelled, self.comboScore])

    def vectorizeMe(self):
        mesh = ';'.join(self.mesh) if self.mesh else ''
        semanticTypes = ';'.join(self.semanticTypes) if self.semanticTypes else ''
        previous = self.previouskeywords if self.previouskeywords else ''
        
        return [str(self.datetime), str(self.userId), self.keywords, previous, mesh, semanticTypes, str(self.CHVFound), str(self.hasCHV), str(self.hasUMLS), str(self.hasCHVMisspelled), str(self.comboScore)] 
        
    def __str__(self):
        vec = self.vectorizeMe()
        vec[2] = "".join(vec[2])
        vec[3] = "".join(vec[3])
        return ",".join(vec)

    def identical(self, otherDS):
        return self.datetime == otherDS.datetime and self.userId == otherDS.userId and self.keywords == otherDS.keywords and self.previouskeywords == otherDS.previouskeywords and self.mesh == otherDS.mesh and self.semanticTypes == otherDS.semanticTypes and self.CHVFound == otherDS.CHVFound and self.hasCHV == otherDS.hasCHV and self.hasUMLS == otherDS.hasUMLS and self.hasCHVMisspelled == otherDS.hasCHVMisspelled and self.comboScore == otherDS.comboScore
