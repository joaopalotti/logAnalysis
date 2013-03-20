
from template import plotGraph
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('otherPages.pdf')

#definition:
#plotGraph(saveName=None, pp=None, colors=['c','g','b','r'], PATH_TO_DATA="/home/palotti/Dropbox/tuwien/PhD/logs/logAnalysis/plots/", globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*", Ylabel='Percentage of Occurences', Xlabel='Mesh Depth', N=None):

#plotQueriesPerSession("qps.pdf", pp)
plotGraph(saveName="qps.pdf", pp=pp, globString="queriesPerSession*.data", rebaseString="queriesPerSession(?P<base>\w*)", Ylabel="Percentage of Sessions", Xlabel="Session Length (queries)", mapType=int, N=1) 

#plotQuerySize("qs.pdf", pp)
plotGraph(saveName="qs.pdf", pp=pp, ignoreString="Relative", globString="queriesSize*.data", rebaseString="queriesSize(?P<base>\w*)", Ylabel="Percentage of each size", Xlabel="Size in number of words in a query", mapType=float, N=1) 

#plotMesh
plotGraph(saveName="md.pdf", pp=pp, globString="meshDepth*.data", rebaseString="meshDepth(?P<base>\w*)", Ylabel="Percentage of Occurences", Xlabel="Mesh Depth", mapType=int, N=None) 

pp.close()
