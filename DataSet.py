from datetime import datetime
import re, sys, csv

class DataSet(object):
    
    def __init__(self, dttime, userId, keywords, previouskeywords=None, category=None, publication=None, rank=None, clickurl=None, mesh=None, semanticTypes=None, usingTimestamp=False):
      
        withMs = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})")
        withMsAndQuote = re.compile("\"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})\"")
        withScs = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})")
        withScsAndQuote = re.compile("\"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\"")

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
            print "ERROR: Invalid date format found! : ", dttime
            self.datetime = None
            assert False

        #userId in the tripdatabase and annonid in AOL
        self.userId = userId
        
        # remove final char that screws the CSV reader
        self.keywords = keywords.rstrip("\\")
        
        self.category = category if category else None
        self.publication = publication if publication else None
        self.previouskeywords = None if not previouskeywords or previouskeywords  == "Null" or previouskeywords == "NULL" else previouskeywords
        self.rank = rank if rank else None
        self.clickurl = clickurl if clickurl else None
        self.mesh = mesh.strip().split(";") if mesh else None
        self.semanticTypes = semanticTypes.strip().split(";") if semanticTypes else None

        #print "UserId = ", self.userId, " time =", self.datetime, " keywords = ", self.keywords
        
    def printMe(self, out=sys.stdout, converting=False):
        writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL, quotechar ='"', escapechar='\\', doublequote=False)
        # Should add here any important information and modify the corresponding readCSV
        if converting:
            # Not printing the mesh and semanticTypes when converting -> the myApi2.java should not receive this fields
            writer.writerow( [ str(self.datetime) ,  self.userId, self.keywords, self.previouskeywords]) 
        else:
            writer.writerow( [ str(self.datetime) ,  self.userId, self.keywords, self.previouskeywords, self.mesh, self.semanticTypes ])

        
