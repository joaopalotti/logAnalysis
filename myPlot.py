from pylab import *
from collections import Counter
import math, sys

PATH_TO_SAVE="plots/"

def finalPlot(x, y, label_, format_="o", saveName=None, showIt=True, closeIt=True):
    plot( x, y, format_, label=label_)
    legend()

    if saveName:
        savefig(PATH_TO_SAVE + saveName)
    
    if showIt:
        show()
    
    if closeIt:
        close()


def plotXY(dataX, dataY, xlabelName, ylabelName, label1=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True):
    
    ylabel(ylabelName)
    xlabel(xlabelName)
    
    configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
    finalPlot(dataX, dataY, label1, "o", saveName, showIt, closeIt=lastOne)


def plotCounter(counter, xlabelName, ylabelName, label1=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True):

    ylabel(ylabelName)
    xlabel(xlabelName)
    
    configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)

    finalPlot(counter.keys(), counter.values(), label1, "o", saveName, showIt, closeIt=lastOne)


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
 
def plotFrequency(data1, xlabelName, label1=None, saveName=None, data2=None, label2=None, xStartRange=None, xEndRange=None, yStartRange=None, yEndRange=None, showIt=True, lastOne=True):

    dataInt = [ floor(v) for v in data1] 
    c1 =  Counter(dataInt)  
    
    ylabel("Frequency")
    xlabel(xlabelName)
    
    configureLimits(xStartRange, xEndRange, yStartRange, yEndRange)
   
    finalPlot(c1.keys(), c1.values(), label1, "o", saveName, showIt, closeIt=lastOne)
