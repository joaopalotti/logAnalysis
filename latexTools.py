import numpy, re

class latexPrinter:
    
    def __init__(self, documentName="latexOut.tex"):
        self.document = open(documentName, "w")
        header = self.createDocument()
        self.document.write( header )

    def __del__(self):
        if self.document:
            self.document.write(  "\n\\end{document}\n" )

    def createDocument(self):
        s = "\\documentclass[english]{article}\n"
        s += "\\usepackage[T1]{fontenc}\n"
        s += "\\usepackage[latin9]{inputenc}\n"
        s += "\\usepackage{babel}\n"
        s += "\\usepackage{booktabs}\n"
        s += "\\usepackage{etex}\n"
        s += "\\reserveinserts{18}\n"
        s += "\\usepackage{morefloats}\n"
        s += "\\begin{document}\n"
        return s

    """
        rows should have this format:
            [ [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5] ]
    """
    def addTable(self, rows, caption=None, nestedList=False, transpose=False):
        if not rows:
            return

        #Check if all rows have the same size
        #assert( len(set([ len(r) for r in rows] )) == 1)
        self.document.write("\\begin{table}[ht]\n")
        #self.document.write("\\begin{center}\n")
        self.document.write("\\hspace{-3cm}\n")
             
        if transpose:
            cols = 'c|' * len(rows)
        else:
            cols = 'c|' * len(rows[0])
        self.document.write("\\begin{tabular}{|" + cols + "}\n")
        
        self.document.write("\\toprule\n")
        
        if transpose:
            rows = [list(i) for i in zip(*rows)]

        header = True
        for row in rows:
            self.document.write( self.__escapeChars(str(row[0])) )
            for element in row[1:]:
                if type(element) in [float, int, numpy.float64]:
                    self.document.write(" & %.2f" % element)
                else:
                    self.document.write(" & " + self.__escapeChars(element))
            self.document.write(" \\\\ \n")

            if header:
                header = False
                self.document.write("\\midrule\n")
            else:
                self.document.write("\\hline\n")


        #self.document.write("\\bottomrule\n")
        
        self.document.write("\\end{tabular}\n")
        if caption:
            self.document.write("\\caption{" + caption + "}\n")
        #self.document.write("\\end{center}\n")
        self.document.write("\\end{table}\n")

    def __escapeChars(self, s):
        return re.sub("#","\#", re.sub("%", "\%", s))
