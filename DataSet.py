from datetime import datetime
import re

class DataSet(object):
    
    def __init__(self, dttime, sessionid, category, publication, keywords, previouskeywords, rank, clickurl, usingTimestamp=False):
       
        trip = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})")
        aol = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})")
        hon = re.compile("\"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\"")

        if trip.match(dttime):
            self.datetime = datetime.strptime(dttime, '%Y-%m-%d %H:%M:%S.%f')
        elif aol.match(dttime):
            self.datetime = datetime.strptime(dttime, '%Y-%m-%d %H:%M:%S')
        elif hon.match(dttime):
            self.datetime = datetime.strptime(dttime, '"%Y-%m-%d %H:%M:%S"')
        elif usingTimestamp:
            self.datetime = datetime.fromtimestamp(float(dttime))
        else:
            print "ERROR: Invalid date format found!"
            self.datetime = None
            assert False

        #Sessionid in the tripdatabase and annonid in AOL
        self.sessionid = sessionid
        
        self.keywords = keywords
        
        self.category = category if category else None
        self.publication = publication if publication else None
        self.previouskeywords = None if not previouskeywords or previouskeywords  == "Null" or previouskeywords == "NULL" else previouskeywords
        self.rank = rank if rank else None
        self.clickurl = clickurl if clickurl else None
