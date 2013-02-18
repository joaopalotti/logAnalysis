
from datetime import datetime

class TripData:
    def __init__(self, dttime, sessionid, category, publication, keywords, previouskeywords):
        self.datatime = datetime.strptime(dttime, '%Y-%m-%d %H:%M:%S.%f')
        self.sessionid = sessionid
        self.category = category
        self.publication = publication
        self.keywords = keywords
        if previouskeywords == "Null" or previouskeywords == "NULL":
            self.previouskeywords = None
        else:
            self.previouskeywords = previouskeywords


