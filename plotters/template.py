#!/usr/bin/env python

from __future__ import division
import glob
import numpy as np
import matplotlib.pyplot as plt
import pylab as P
import re

def normalize(values, total):
    vs = []
    print "TOTAL = ", total
    print "INPUT = ", values
    for v in values:
        vs.append( v / total )
    print "OUTPUT = ", vs
    return vs

def plotGraph(barwidth=20, saveName=None, pp=None, ignoreString=None, colors=['r','b','g','c','m'], PATH_TO_DATA="/home/palotti/Dropbox/tuwien/PhD/logs/logAnalysis/plots/", globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*", Ylabel='Percentage of Occurences', Xlabel='Mesh Depth', mapType=int, N=None, absolute=False):

    files = glob.glob(PATH_TO_DATA + globString)

    width = barwidth    # the width of the bars
    maxX = -1
    maxY = -1
    
    gettingAllData = True if N is None else False
    allYs = {}
    
    for file in files:
        
        if ignoreString and ignoreString in file:
            print "Ignoring file ", file
            continue

        ys = []
        print file
        m = re.search(rebaseString,file)
        dataName = m.group(1)
        sumY = 0

        #print "DATANAME = ", dataName
        with open(file,"r") as f:
            yacc = 0

            for line in f.readlines():
                x, y = map(mapType, line.strip().split(","))

                maxX = x if x > maxX else maxX
                maxY = y if y > maxY else maxY
                
                sumY += y
                if N is not None and x >= N:
                    yacc += y
                else:
                    ys.append(y)
            
            # The values greater than N
            if yacc > 0:
                ys.append(yacc)
        
        if not absolute:
            ys = normalize(ys, sumY)
        allYs[dataName] = ys
        #print xs, ys

    N = maxX if N is None else N

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects = {}
    sumWidth = 0 
    xs = np.arange(1, N+1)

    cs = iter(colors)
    for name, data in allYs.iteritems():
        c = cs.next()
        
        # Used only for the khresmoi rank of queries plot
        #if name=="khr1":
        #    name = "Task1"
        #if name=="khr2":
        #    name = "Task2"
        #if name=="khr3":
        #    name = "Task3"
        #if name=="khr4":
        #    name = "Task4"
        #

        rects[name] = ax.bar(xs + sumWidth, data, width, color=c, label=name)
        ax.legend( [rects[name]] , [name], loc=1 )
        
        print "Using color ", c, " for data ", name
        sumWidth += width

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])

    ax.set_ylabel(Ylabel)
    ax.set_title(Xlabel)

    lstString = str(N) + "\n or more" if not gettingAllData else str(N)
    plt.xticks(xs+ (sumWidth/2), map(str,range(1,N) + [lstString] ) )
#plt.xticks(xs+width, ("1a","2b","3","4","5","6","7","8","9","10","11","12") )
    print xs+width


    ax.set_xlim(0.75, N + 1.0)
    if not absolute:
        ax.set_ylim(0,1)
    else:
        ax.set_ylim(0,maxY+0.5)
 
    if saveName is not None:
        plt.savefig(saveName, papertype='a4',orientation='portrait')
    else:
        plt.show()

    if pp:
        pp.savefig()
    
    plt.close()

if __name__ == "__main__":
    plotMeshDepth("md.pdf")

