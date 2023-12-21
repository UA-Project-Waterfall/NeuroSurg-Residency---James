import os
import csv

class PubmedReader:
    '''This class is a replacement for the file class, which sucks...
        jk it's not that bad'''
    lines = []
    index = length = 0
    def __init__(self, fileName):
        with open(fileName, 'r', encoding = 'utf-8') as file:
            self.lines = file.readlines()
        realIndex = -1;
        for line in self.lines:
            if line[:6] == "      ":
                self.lines[realIndex][1] += " " + line[6:].strip()
            else:
                realIndex += 1
                self.lines[realIndex] = [line[:6], line[6:].strip()]
        self.length = realIndex + 1
        self.lines = self.lines[:realIndex + 1]

    def moveTo(self, index):
        if index >= 0 and index < self.length: self.index = index; return True
        return False
        
    def atEnd(self): return self.index >= self.length - 1
    def atStart(self): return self.index <= 0
    def next(self, offset = 1):
        self.index += offset
        if self.index >= self.length: self.index = self.length - 1; return offset > 1
        return True
    def prev(self, offset = 1):
        self.index -= offset
        if self.index < 0: self.index = 0; return offset > 1
        return True

    def lineID(self, index = -1): return self.lines[index if index >= 0 else self.index][0]
    def lineInfo(self, index = -1): return self.lines[index if index >= 0 else self.index][1]

    def scanForID(self, lineIDs):
        ''' lineID can be a single string or list of strings '''
        for index in range(self.index, self.length):
            if self.lineID(index) in lineIDs and self.lineID(index) != "": return index;
        return -1;
    
    def moveToID(self, lineID):
        return self.moveTo(self.scanForID(lineID))

def updateInfo(pmIter, lineIDs, mappings, resultArray):
    '''lineIDs must be in order with the file
        mappings should be same length as lineIDs'''
    for i in range(0, len(lineIDs)):
       pmIter.moveToID(lineIDs[i])
       resultArray[mappings[i]] = pmIter.lineInfo()

def extractInstitutions(pmIter):
    institutions = []
    fauIndex = pmIter.scanForID(["FAU - "])
    adIndex = pmIter.scanForID(["AD  - "])
    if adIndex >= 0 and adIndex < fauIndex:
        pmIter.moveTo(adIndex)
        while pmIter.lineID() == "AD  - ":
            institutions += [pmIter.lineInfo()]
            pmIter.next()
    return institutions if len(institutions) > 0 else [""]

fileDir = os.path.join(os.getcwd(), "Export Files")
fileList = os.listdir(fileDir)

table = [["Author Name", "Authorship position", "Total number of authors", "Title", "PMID",
          "Journal", "NS Journal", "NS pub", "Year", "Affiliation", "Last Author", "Last Author Affiliation"]]

for fileIndex in range(len(fileList)):
    fileName = fileList[fileIndex]
    author = fileName[:-4].strip()
    parenIndex = author.find("(")
    authorKeys = [author[:parenIndex-1].strip()] if parenIndex >= 0 else [author]
    authorKeys += author[parenIndex + 1 : -1].split(",") if parenIndex >= 0 else []
    pmReader = PubmedReader(os.path.join(fileDir, fileName))

    while(pmReader.moveToID(["PMID- "])):
        paperIndex = len(table)
        table += [[""]*len(table[0])];
        updateInfo(pmReader, ["PMID- ", "DP  - ", "TI  - "], [4, 8, 3], table[paperIndex])

        table[paperIndex][2] = 0
        pmReader.moveToID(["JT  - ", "FAU - "])
        maxMatches = 0
        savedFauIndex = currFauIndex = pmReader.index
        while pmReader.lineID() != "JT  - ":
            table[paperIndex][2] += 1
            currFauIndex = pmReader.index
            author = pmReader.lineInfo()
            if(authorKeys[0] in author):
                numMatches = sum([key in author for key in authorKeys])    #counts number of matches
                if(numMatches > maxMatches):
                    table[paperIndex][1] = table[paperIndex][2]
                    table[paperIndex][0] = author
                    maxMatches = numMatches
                    savedFauIndex = currFauIndex
            pmReader.next()
            pmReader.moveToID(["JT  - ", "FAU - "])
        table[paperIndex][5] = pmReader.lineInfo()
        pmReader.moveTo(savedFauIndex + 1)
        institutions = extractInstitutions(pmReader)
        table[paperIndex][9] = institutions[0]
        if(len(institutions) > 1):
            for i in range(1, len(institutions)):
                table += [[""]*len(table[0])]
                table[paperIndex + i][9] = institutions[i]

    table += [[""]*len(table[0])];

with open(os.path.join(os.getcwd(), "compiled.csv"), "w", newline = "", encoding = 'utf-8') as file:
    writer = csv.writer(file, delimiter = ',')
    for line in table:
        writer.writerow(line)