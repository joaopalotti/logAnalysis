#!/usr/bin/env python

from __future__ import division
import glob
import numpy as np
import matplotlib.pyplot as plt
import pylab as P
import re
import matplotlib as mpl

def mySort(a, b):
    if "aolNotHealth" in a:
        return 1
    if "aolHealth" in a: 
        return -1
    if "hon" in a and ("trip" in b or "goldminer" in b or "aolNotHealth" in b):
        return -1
    elif "hon" in a:
        return 1
    if "trip" in a and ("goldminer" in b or "aolNotHealth" in b):
        return -1
    elif "trip" in a:
        return 1
    if "goldminer" in a and "aolNotHealth" in b:
        return -1
    elif "goldminer" in a:
        return 1
    return 0
    

def normalize(values, total):
    vs = []
    print "TOTAL = ", total
    print "INPUT = ", values
    for v in values:
        vs.append( v / total )
    print "OUTPUT = ", vs
    return vs

def plotGraph(barwidth=20, saveName=None, pp=None, ignoreString=None, colors=['r','b','g','c','m'], PATH_TO_DATA="/home/palotti/Dropbox/tuwien/PhD/logs/logAnalysis/plots/", globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*", Ylabel='Percentage of Occurences', Xlabel='Mesh Depth', mapType=int, N=None, absolute=False, plotType="cdf", legendLocation=1):

    if absolute == True and plotType == "cdf":
        print "Please, user ABSOLUTE = False"
        sys.exit(0)

    #http://matplotlib.org/users/customizing.html
    mpl.rcParams['font.size'] = 16
    mpl.rcParams['figure.autolayout'] = True
    mpl.rcParams['lines.linewidth'] = 3

    files = glob.glob(PATH_TO_DATA + globString)

    width = barwidth    # the width of the bars
    maxX = -1
    maxY = -1
    
    gettingAllData = True if N is None else False
    allYs = {}
    
    #print "FILES ---> " , files
    #print "SORTED(FILES) ---> " , sorted(files, cmp=mySort)

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

    keyorder = ['aolHealth', 'hon', 'trip', 'goldminer', 'aolNotHealth']
    #allYs = sorted(allYs.items(), cmp=mySort)
    allYs = sorted(allYs.items(), key=lambda i:keyorder.index(i[0]))
    print allYs

    for name, data in allYs:
        c = cs.next()
        
        # Used only for the khresmoi rank of queries plot
        if name=="hon":
            name = "HON"
        elif name=="trip":
            name = "TRIP"
        elif name=="aolNotHealth":
            name = "AOL-NotHealth"
        elif name=="aolHealth":
            name = "AOL-Health"
        elif name=="goldminer":
            name = "GoldMiner"
        
        if plotType == "bar":
            rects[name] = ax.bar(xs + sumWidth, data, width, color=c, label=name)
        elif plotType == "line": 
            rects[name] = ax.plot(xs, data, color=c, label=name)
        elif plotType == "cdf": 
            dx = .01
            Y = np.array(data)

            # Normalize the data to a proper PDF
            Y /= (dx*Y).sum()

            # Compute the CDF
            CY = np.cumsum(Y*dx)

            #rects[name] = ax.plot(xs, data, color=c, label=name)
            rects[name] = ax.plot(xs, CY, color=c, label=name)

        print "Using color ", c, " for data ", name
        sumWidth += width

    handles, labels = ax.get_legend_handles_labels()
    
    #http://matplotlib.org/users/legend_guide.html
    if plotType == "cdf":
            legendLocation = 4
    ax.legend(handles[::1], labels[::1], loc=legendLocation)


    ax.set_ylabel(Ylabel) #, fontsize=15, fontweight="bold")
    ax.set_xlabel(Xlabel) #, fontsize=15, fontweight="bold")

    lstString = str(N) + "\n or more" if not gettingAllData else str(N)
    if plotType == "bar":
        plt.xticks(xs + (sumWidth/2), map(str,range(1,N) + [lstString] ) )
        ax.set_xlim(0.75, N + 1.0)

    elif plotType == "line":
        plt.xticks(xs, map(str,range(1,N) + [lstString]))
        ax.set_xlim(0.5, N + 0.5)

    elif plotType == "cdf":
        plt.xticks(xs, map(str,range(1,N) + [lstString]))
        ax.set_xlim(1, N)

    #plt.xticks(xs+width, ("1a","2b","3","4","5","6","7","8","9","10","11","12") )
    #print xs+width

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

