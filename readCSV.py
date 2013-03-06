import csv
from DataSet import DataSet
from datetime import datetime
from time import time
import gzip

'''check if two rows belong to the same user and during the same session (defined by default as a 30 min time'''
def checkSession(previousRow, currentRow, timeBetweenInSeconds=60*30, dateFormat='%Y-%m-%d %H:%M:%S', idIndex=0, dateIndex=2, usingTimestamp=False):
    
    # Check if both queries belong to the same user 
    if previousRow[idIndex] == currentRow[idIndex]:
        if not usingTimestamp: 
            dtPrevious = datetime.strptime(previousRow[dateIndex], dateFormat)
            dtCurrent = datetime.strptime(currentRow[dateIndex], dateFormat)
            timeSpansInSeconds = (max(dtPrevious, dtCurrent) - min(dtPrevious, dtCurrent)).total_seconds()
            if timeSpansInSeconds <= timeBetweenInSeconds:
                return True
        else:
            dtPrevious, dtCurrent = float(previousRow[dateIndex]), float(currentRow[dateIndex])
            #Assuming the timestamps are in seconds:
            if ( abs(dtPrevious - dtCurrent ) ) <= timeBetweenInSeconds:
                return True
    return False

def readMyFormat(filename):
    print "Reading file: ", filename
    start = time()
     
    data = []
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    else:
        csvfile = open(filename, 'rb')

    reader = csv.reader(csvfile, delimiter=',', quotechar='"', escapechar="\\", doublequote=False)
    
    #Sort the data by user and datetime to construct sessions
    reader = sorted(reader, key= lambda k: (k[1], k[0]))  

    ## The concept of session should already be defined when this file was created. 
    for row in reader:
        if len(row[2]) == 0 or row[2] == None:
            continue

        temp = DataSet(dttime=row[0], userId=row[1], keywords=row[2], previouskeywords=row[3], mesh=row[4])
        data.append(temp)
    return data


def readGoldMiner(filename):
    
    print "Reading information for GoldMiner data. Filename: ", filename
    start = time()

    data = []
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    else:
        csvfile = open(filename, 'rb')
    
    reader = csv.reader(csvfile, delimiter='|')
    
    #Header - skip it
    #In the version 4 we dont need to skip the header -> reader.next()
    
    #Sort the data by user and datetime to construct sessions
    reader = sorted(reader, key= lambda k: (k[1], k[0]))  
    
    #Data in the first line
    previousRow = reader[0]
    
    # (0) timestamp (1) client (2) keywords
    # (3) images matched by concept search (using ontologies) (4) images matched by keyword (string) search
    # (5) total number of images returned (may be less than c + x;  it's the union of the two search result sets)
    temp = DataSet(dttime=previousRow[0], userId=previousRow[1], category=None, publication=None, keywords=previousRow[2], rank=None, clickurl=None, previouskeywords=None, usingTimestamp=True)
    data.append(temp)             
    
    for row in reader[1:]:
        if row:
            if checkSession(previousRow, row, idIndex=1, dateIndex=0, usingTimestamp=True):
                temp = DataSet(dttime=row[0], userId=row[1], category=None, publication=None, keywords=row[2], rank=None, clickurl=None, previouskeywords=previousRow[2], usingTimestamp=True)
            else:
                temp = DataSet(dttime=row[0], userId=row[1], category=None, publication=None, keywords=row[2], rank=None, clickurl=None, previouskeywords=None, usingTimestamp=True)
            data.append(temp)
            previousRow = row

    csvfile.close()
    print "GoldMiner data read in %.2f seconds" % float(time() - start)
    return data

'''
Read and process data from Health On the Net (HON) - basically:
id,date,engine,language,nb_terms,orig_query,query_id,session_id,source,user_id,loaded_file_id,ip_address_id,refere
'''
def readHONDataSet(filename):
    
    print "Reading information for HON data. Filename: ", filename
    start = time()
    
    data = []
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    
    else:
        csvfile = open(filename, 'rb')
    
    reader = csv.reader(csvfile, delimiter=',', quotechar="\"", escapechar='\\')
    
    #Sort the data by user and datetime to construct sessions
    reader = sorted(reader, key= lambda k: (k[11], k[1]))  

    #Data in the first line
    previousRow = reader[0]
    # (0) msql-id, (1) date, (2) engine, (3) language, (4) nb_terms, (5) orig_query, (6) query_id, (7) session_id, (8) source, (9) user_id, (10) loaded_file_id, (11) ip_address_id, (12) refere
    temp = DataSet(dttime=previousRow[1], userId=previousRow[11], category=None, publication=None, keywords=previousRow[5].strip("\""), rank=None, clickurl=None, previouskeywords=None)
    data.append(temp)             

    for row in reader[1:]:
        if row:
            if checkSession(previousRow, row, idIndex=11, dateIndex=1, dateFormat='%Y-%m-%d %H:%M:%S'):
                temp = DataSet(dttime=row[1], userId=row[11], category=None, publication=None, keywords=row[5], rank=None, clickurl=None, previouskeywords=previousRow[5].strip("\""))
            else:
                temp = DataSet(dttime=row[1], userId=row[11], category=None, publication=None, keywords=row[5], rank=None, clickurl=None, previouskeywords=None)
            data.append(temp)
            previousRow = row
    
    csvfile.close()
    print "HON data read in %.2f seconds" % float(time() - start)
    return data

'''
Read and process data like this:

1268    gallstones  2006-05-11 02:13:02 1   http://www.niddk.nih.gov
'''
def readAolDataSet(filename):
    
    print "Reading information for AOL data. Filename: ", filename
    start = time()

    data = []
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    
    else:
        csvfile = open(filename, 'rb')
    
    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    if not reader:
        return
    
    #Sort the data by user and datetime to construct sessions
    reader = sorted(reader, key= lambda k: (k[0], k[2]))  

    #Data in the first line
    previousRow = reader[0]
    temp = DataSet(dttime=previousRow[2], userId=previousRow[0], category=None, publication=None, keywords=previousRow[1], rank=previousRow[3], clickurl=previousRow[4], previouskeywords=None)
    data.append(temp)             

    # The rest of the data
    for row in reader[1:]:
        if row:
            if checkSession(previousRow, row):
                temp = DataSet(dttime=row[2], userId=row[0], category=None, publication=None, keywords=row[1], rank=row[3], clickurl=row[4], previouskeywords=previousRow[1])
            else:
                temp = DataSet(dttime=row[2], userId=row[0], category=None, publication=None, keywords=row[1], rank=row[3], clickurl=row[4], previouskeywords=None)
            data.append(temp)
            previousRow = row
    
    csvfile.close()
    print "AOL data read in %.2f seconds" % float(time() - start)
    return data

#if file in DOS format, it is necessary to run dos2unix command before running this script
def readTripDataSet(filename):
    
    print "Reading information for TRIP data. Filename: ", filename
    start = time()

    data = []
    
    if filename.endswith(".gz"):
        csvfile = gzip.open(filename, 'rb')
    
    else:
        csvfile = open(filename, 'rb')

    reader = csv.reader(csvfile, delimiter='\t', quotechar='|')

    #It is not necessary to sort the reader because we are trusting the information of previouskeywords.
    for row in reader:
        if row:
            #print ', '.join(row)
            if len(row) == 6:
               temp = DataSet(dttime=row[0], userId=row[1], category=row[2], publication=row[3], keywords=row[4], previouskeywords=row[5], rank=None, clickurl=None)
            else:
               temp = DataSet(dttime=row[0], userId=row[1], category=row[2], publication=row[3], keywords=row[4], previouskeywords=None, rank=None, clickurl=None)
            data.append(temp)             

    csvfile.close()
    
    print "TRIP data read in %.2f seconds" % float(time() - start)
    return data
