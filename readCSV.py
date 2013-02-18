import csv
from DataSet import DataSet
import gzip
from datetime import datetime

'''check if two rows belong to the same user and during the same session (defined by default as a 30 min time'''
def checkAOLSession(previousRow, currentRow, timeBetweenInSeconds=60*30):
    # Check if both queries belong to the same user 
    if previousRow[0] == currentRow[0]:
        dtPrevious = datetime.strptime(previousRow[2], '%Y-%m-%d %H:%M:%S')
        dtCurrent = datetime.strptime(currentRow[2], '%Y-%m-%d %H:%M:%S')
        timeSpansInSeconds = (max(dtPrevious, dtCurrent) - min(dtPrevious, dtCurrent)).total_seconds()
        if timeSpansInSeconds <= timeBetweenInSeconds:
            return True
    return False

def readAolDataSet(filename):
    # Example: 1268    gallstones  2006-05-11 02:13:02 1   http://www.niddk.nih.gov

    data = []
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    
    else:
        csvfile = open(filename, 'rb')
    
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    if not reader:
        return
    
    #Data in the first line
    previousRow = reader.next()
    temp = DataSet(dttime=previousRow[2], sessionid=previousRow[0], category=None, publication=None, keywords=previousRow[1], rank=previousRow[3], clickurl=previousRow[4], previouskeywords=None)
    data.append(temp)             

    # The rest of the data
    for row in reader:
        if row:
            if checkAOLSession(previousRow, row):
                temp = DataSet(dttime=row[2], sessionid=row[0], category=None, publication=None, keywords=row[1], rank=row[3], clickurl=row[4], previouskeywords=previousRow[1])
            else:
                temp = DataSet(dttime=row[2], sessionid=row[0], category=None, publication=None, keywords=row[1], rank=row[3], clickurl=row[4], previouskeywords=None)
            data.append(temp)
            previousRow = row
    return data

#if file in DOS format, it is necessary to run dos2unix command before running this script
def readTripDataSet(filename):

    data = []
    
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    
    else:
        csvfile = open(filename, 'rb')

    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in reader:
        if row:
            #print ', '.join(row)
            if len(row) == 6:
               temp = DataSet(dttime=row[0], sessionid=row[1], category=row[2], publication=row[3], keywords=row[4], previouskeywords=row[5], rank=None, clickurl=None)
            else:
               temp = DataSet(dttime=row[0], sessionid=row[1], category=row[2], publication=row[3], keywords=row[4], previouskeywords=None, rank=None, clickurl=None)
            data.append(temp)             

    csvfile.close()
    return data
