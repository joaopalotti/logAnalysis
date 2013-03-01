import numpy as np

def generateStatsVector(values):
    return npStatistics(values)

class npStatistics:

    def __init__(self, values):
        self.min    = np.nanmin(values)
        self.max    = np.nanmax(values)
        self.mean   = np.mean(values)
        self.median = np.median(values)
        self.std    = np.std(values) 


    

