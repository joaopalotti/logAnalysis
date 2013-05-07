
from template import plotGraph
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('otherPages.pdf')
barwidth=0.18

#definition:
#plotGraph(barwidth, saveName=None, pp=None, colors=['c','g','b','r'], PATH_TO_DATA="/home/palotti/Dropbox/tuwien/PhD/logs/logAnalysis/plots/", globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*", Ylabel='Percentage of Occurences', Xlabel='Mesh Depth', N=None)

#plotQueriesPerSession("qps.pdf", pp)
plotGraph(barwidth, saveName="qps.pdf", pp=pp, globString="queriesPerSession*.data", rebaseString="queriesPerSession(?P<base>\w*)", Ylabel="Percentage of Sessions", Xlabel="Session Length (queries)", mapType=int, N=10) 

#plotQuerySize("qs.pdf", pp)
plotGraph(barwidth, saveName="qs.eps", pp=pp, ignoreString="Relative", globString="queriesSize*.data", rebaseString="queriesSize(?P<base>\w*)", Ylabel="Number of queries (%)", Xlabel="Terms per query", mapType=float, N=5, barPlot=False) 

#plotMesh
plotGraph(barwidth, saveName="md.pdf", pp=pp, globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*)", Ylabel="Percentage of Occurences", Xlabel="Mesh Depth", mapType=int, N=10) 

#number of queries by number of users
plotGraph(barwidth, saveName="qpu.pdf", pp=pp, globString="queriesPerUser*.data", rebaseString="queriesPerUser(?P<base>\w*)", Ylabel="Number Of Users ($\%$)", Xlabel="Number of Queries", mapType=int, N=10) 

plotGraph(barwidth, saveName="qpuA.pdf", pp=pp, globString="queriesPerUser*.data", rebaseString="queriesPerUser(?P<base>\w*)", Ylabel="Number Of Users", Xlabel="Number of Queries", mapType=int, N=10, absolute=True) 


#plotGraph(saveName="rq.pdf", pp=pp, globString="queryRanking*.data", rebaseString="queryRanking(?P<base>\w*)", Ylabel="Frequency (%)", Xlabel="Rank of the clicked result", mapType=int, N=11) 

pp.close()
