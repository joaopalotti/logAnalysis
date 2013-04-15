
### This module was created to filter the non english chars from the health on the net data.

import re


def isAllAlpha(text):
    text = re.sub("[\w\s]","", text)
    print text


def onlyRomanChars(s):
    try:
        s.encode("iso-8859-1")
        return True
    except UnicodeDecodeError:
        return False


filename="dataSets/honAll.csv"

with open(filename) as f:
    lines = f.readlines()


for line in lines:
    if onlyRomanChars(line):
        print line,

