from __future__ import division
from collections import Counter
import math, sys

# comment if you cannot install pylab
#from pylab import *
#from matplotlib.backends.backend_pdf import PdfPages

PATH_TO_SAVE="plots/"

class plotter:
    def __init__(self, plottingInstalled=True):
        self.plottingInstalled = plottingInstalled
        if self.plottingInstalled:
            self.pp = PdfPages(PATH_TO_SAVE + 'multipage.pdf')
    
    def __del__(self):
        if self.plottingInstalled:
            self.pp.close()

    def __finalPlot(self, x, y, label_, format_="o", saveName=None, showIt=True, closeIt=True, loglogFormat=False):
        
        if loglogFormat:
            # Reduntant...
            loglog(x, y, format_, label=label_)
        else:
            plot( x, y, format_, label=label_)
    
        legend()

        if saveName and closeIt:
            savefig(PATH_TO_SAVE + saveName + ".png")
            self.pp.savefig()
            close()
        
        if showIt:
            show()
        
    def plotXY(self, dataX, dataY, xlabelName, ylabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, printValuesToFile=False, plottingInstalled=True):
        
        if printValuesToFile and label and saveName:
            with open(PATH_TO_SAVE + saveName + label + ".data", "w") as f:
                for x, y in zip(dataX, dataY):
                    f.write(str(x) + "," + str(y) + "\n")

        if plottingInstalled:
            self.__configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
            ylabel(ylabelName)
            xlabel(xlabelName)
            self.__finalPlot(dataX, dataY, label, "o", saveName, showIt, closeIt=lastOne)

    def plotCounter(self, counter, xlabelName, ylabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, printValuesToFile=False, plottingInstalled=True):

        if printValuesToFile and label and saveName:
            with open(PATH_TO_SAVE + saveName + label + ".data", "w") as f:
                for x, y in counter.iteritems():
                    f.write(str(x) + "," + str(y) + "\n")
        
        if plottingInstalled:
            ylabel(ylabelName)
            xlabel(xlabelName)
            self.__configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
            self.__finalPlot(counter.keys(), counter.values(), label, "o", saveName, showIt, closeIt=lastOne)

    def __configureLimits(self, xStartRange, xEndRange, yStartRange, yEndRange):

        if xStartRange is not None and xEndRange is not None:
            xlim(xStartRange, xEndRange)
        elif xStartRange is not None and xEndRange is None:
            xlim(xmin=xStartRange)
        elif xStartRange is None and xEndRange is not None:
            xlim(xmax=xEndRange)
        
        if yStartRange is not None and yEndRange is not None:
            ylim(yStartRange, yEndRange)
        elif yStartRange is not None and yEndRange is None:
            ylim(ymin=yStartRange)
        elif yStartRange is None and yEndRange is not None:
            ylim(ymax=yEndRange)
     
    def plotLogLogFrequency(self, data1, xlabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, relative=False, printValuesToFile=False, plottingInstalled=True):
        self.plotFrequency(data1, xlabelName, label, saveName, data2, label2, xStartRange, xEndRange, yStartRange, yEndRange, showIt, lastOne, relative, printValuesToFile, loglog=True, plottingInstalled=plottingInstalled)

    def plotFrequency(self, data1, xlabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, relative=False, printValuesToFile=False, loglog=False, plottingInstalled=True):

        if plottingInstalled:
            ylabel("Frequency")
            xlabel(xlabelName)
        
        dataInt = [ math.floor(v) for v in data1] 
        c1 =  Counter(dataInt)  

        if plottingInstalled and loglog:
            #print "Ploting log-log"
            ylabel("Frequency (log)")
            xscale('log')
            yscale('log')
        
        if relative:
            total = sum(c1.values())
            newC1 = dict()
            for k,v in dict(c1).iteritems():
                newC1[k] = (100 * v)/total
            c1 = newC1 
            if plottingInstalled:
                ylabel("Frequency (%)")
                self.__configureLimits(xStartRange, xEndRange, 0, 100)
        

        if printValuesToFile and label and saveName:
            with open(PATH_TO_SAVE + saveName + label + ".data", "w") as f:
                for x, y in c1.iteritems():
                    f.write(str(x) + "," + str(y) + "\n")
        
        if plottingInstalled:
            self.__configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
            self.__finalPlot(c1.keys(), c1.values(), label, "o", saveName, showIt, closeIt=lastOne, loglogFormat=loglog)
