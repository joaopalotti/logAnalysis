
from template import plotGraph
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('otherPages.pdf')
barwidth=0.18
PATH_TO_DATA="/home/palotti/Dropbox/tuwien/PhD/logs/logAnalysis/plots/"

import sys
print sys.argv, len(sys.argv)
if len(sys.argv) >= 2:
    PATH_TO_DATA = sys.argv[1]

#definition:
#plotGraph(barwidth, saveName=None, pp=None, colors=['c','g','b','r'], PATH_TO_DATA="/home/palotti/Dropbox/tuwien/PhD/logs/logAnalysis/plots/", globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*", Ylabel='Percentage of Occurences', Xlabel='Mesh Depth', N=None)

#plotQueriesPerSession("qps.pdf", pp)
#plotGraph(barwidth, saveName="qps.pdf", pp=pp, globString="queriesPerSession*.data", rebaseString="queriesPerSession(?P<base>\w*)", Ylabel="Percentage of Sessions", Xlabel="Session Length (queries)", mapType=int, N=10) 

#plotQuerySize("qs.pdf", pp)
#plotGraph(barwidth, saveName="qs.eps", pp=pp, ignoreString="Relative", globString="queriesSize*.data", rebaseString="queriesSize(?P<base>\w*)", Ylabel="Number of queries (%)", Xlabel="Terms per query", mapType=float, N=12, plotType="cdf", legendLocation=4, PATH_TO_DATA=PATH_TO_DATA) 

plotGraph(barwidth, saveName="cpq.eps", pp=pp, ignoreString="Relative", globString="wordSize*.data", rebaseString="wordSize(?P<base>\w*)", Ylabel="Number of queries (%)", Xlabel="Characters per query", mapType=float, N=50, plotType="cdf", legendLocation=4, PATH_TO_DATA=PATH_TO_DATA, deltaXTicks=5) 

#plotGraph(barwidth, saveName="time.eps", pp=pp, ignoreString="Relative", globString="timePerSession*.data", rebaseString="timePerSession(?P<base>\w*)", Ylabel="Number of Sessions (%)", Xlabel="Time Per Session (s)", mapType=float, roundX=True, N=3000, plotType="cdf", legendLocation=4, PATH_TO_DATA=PATH_TO_DATA, XStartsFrom=0, deltaXTicks = 500) 

#plotGraph(barwidth, saveName="qpsession.eps", pp=pp, ignoreString="Relative", globString="queriesPerSession*.data", rebaseString="queriesPerSession(?P<base>\w*)", Ylabel="Number of Sessions (%)", Xlabel="Queries Per Session", mapType=float, N=30, plotType="cdf", legendLocation=4, PATH_TO_DATA=PATH_TO_DATA, deltaXTicks = 5) 

#plotGraph(barwidth, saveName="qs.eps", pp=pp, ignoreString="Relative", globString="queriesSize*.data", rebaseString="queriesSize(?P<base>\w*)", Ylabel="Number of queries (%)", Xlabel="Terms per query", mapType=float, N=5, plotType="bar", legendLocation=1, PATH_TO_DATA=PATH_TO_DATA) 


#plotGraph(barwidth, saveName="qspc.eps", pp=pp, ignoreString="Relative", globString="wordSize*.data", rebaseString="wordSize(?P<base>\w*)", Ylabel="CDF of Number of queries (%)", Xlabel="Chars per query", mapType=float, N=50, plotType="cdf", legendLocation=4, PATH_TO_DATA=PATH_TO_DATA) 

#plotMesh
#plotGraph(barwidth, saveName="md.pdf", pp=pp, globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*)", Ylabel="Percentage of Occurences", Xlabel="Mesh Depth", mapType=int, N=10) 

#number of queries by number of users
#plotGraph(barwidth, saveName="qpu.pdf", pp=pp, globString="queriesPerUser*.data", rebaseString="queriesPerUser(?P<base>\w*)", Ylabel="Number Of Users ($\%$)", Xlabel="Number of Queries", mapType=int, N=10) 

#plotGraph(barwidth, saveName="qpuA.pdf", pp=pp, globString="queriesPerUser*.data", rebaseString="queriesPerUser(?P<base>\w*)", Ylabel="Number Of Users", Xlabel="Number of Queries", mapType=int, N=10, absolute=True) 


#plotGraph(saveName="rq.pdf", pp=pp, globString="queryRanking*.data", rebaseString="queryRanking(?P<base>\w*)", Ylabel="Frequency (%)", Xlabel="Rank of the clicked result", mapType=int, N=11) 

pp.close()
