from __future__ import division
from pylab import *
from collections import Counter
import math, sys

PATH_TO_SAVE="plots/"

def finalPlot(x, y, label_, format_="o", saveName=None, showIt=True, closeIt=True):
    plot( x, y, format_, label=label_)
    legend()

    if saveName and closeIt:
        savefig(PATH_TO_SAVE + saveName + ".png")
        close()
    
    if showIt:
        show()
    
def plotXY(dataX, dataY, xlabelName, ylabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, printValuesToFile=False):
    
    ylabel(ylabelName)
    xlabel(xlabelName)
    
    configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
    if printValuesToFile and label and saveName:
        with open(PATH_TO_SAVE + saveName + label + ".data", "w") as f:
            for x, y in zip(dataX, dataY):
                f.write(str(x) + "," + str(y) + "\n")

    finalPlot(dataX, dataY, label, "o", saveName, showIt, closeIt=lastOne)

def plotCounter(counter, xlabelName, ylabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, printValuesToFile=False):

    ylabel(ylabelName)
    xlabel(xlabelName)
    
    configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
    if printValuesToFile and label and saveName:
        with open(PATH_TO_SAVE + saveName + label + ".data", "w") as f:
            for x, y in counter.iteritems():
                f.write(str(x) + "," + str(y) + "\n")

    finalPlot(counter.keys(), counter.values(), label, "o", saveName, showIt, closeIt=lastOne)

def configureLimits(xStartRange, xEndRange, yStartRange, yEndRange):

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
 
def plotFrequency(data1, xlabelName, label=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True, relative=False, printValuesToFile=False):

    ylabel("Frequency")
    xlabel(xlabelName)
    
    dataInt = [ floor(v) for v in data1] 
    c1 =  Counter(dataInt)  
    
    if relative:
        total = sum(c1.values())
        newC1 = dict()
        for k,v in dict(c1).iteritems():
            newC1[k] = (100 * v)/total
        c1 = newC1 
        ylabel("Frequency (%)")
        configureLimits(xStartRange, xEndRange, 0, 100)
    
    configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)

    if printValuesToFile and label and saveName:
        with open(PATH_TO_SAVE + saveName + label + ".data", "w") as f:
            for x, y in c1.iteritems():
                f.write(str(x) + "," + str(y) + "\n")
    
    finalPlot(c1.keys(), c1.values(), label, "o", saveName, showIt, closeIt=lastOne)
