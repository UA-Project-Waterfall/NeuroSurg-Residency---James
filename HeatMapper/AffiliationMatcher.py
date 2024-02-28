print("Installing prerequisites...")
import openpyxl, pyperclip
from collections import Counter
from pandas import read_excel
from pandas import concat
from pandas import DataFrame
from pathlib import Path
from tqdm import tqdm

#import nltk;
#nltk.download('all')
from nltk.tokenize import word_tokenize

def __main__():
    affArray = getAffiliationArray("AffiliationInfo.xlsx")
    affArray = [str(aff) for aff in affArray]
    
    print("Tokenizing...")
    affTokens = dict()
    allTokens = Counter()
    stopwords = []
    for affiliation in affArray:
        if affiliation not in affTokens:
             affTokens[affiliation] = Counter(word_tokenize(affiliation.lower()))
             allTokens += affTokens[affiliation]
    for token in allTokens:
        if allTokens[token] > len(affTokens)/2:
            stopwords += [token]
    for aff in affTokens:
        for token in stopwords: del affTokens[aff][token]
        
    print("Matching...")
    matchAffs = dict()
    matchTokens = dict()
    minMatchCosine = 0.7
    autoMatchCosine = 0.7
    for i in tqdm(range(0, len(affArray)), desc = "Matching"):
        affiliation = affArray[i]
        bestMatch = ""
        bestCosine = 0
        for checkAff in matchTokens:
            cosine = weightedCosine(affTokens[affiliation], matchTokens[checkAff])
            if cosine > bestCosine:
                bestCosine = cosine
                bestMatch = checkAff
        if bestCosine > minMatchCosine and bestCosine < autoMatchCosine:
            print("\n----------\nCosine: " + str(bestCosine) + "\n" + affiliation + "\n" + bestMatch + "\n----------\n")
            if input("Leave empty to match: ") != "": bestCosine = 0
        if bestCosine < minMatchCosine:
            matchTokens[affiliation] = affTokens[affiliation]
            matchAffs[affiliation] = affiliation  
        else:
            matchAffs[affiliation] = bestMatch
            matchTokens[bestMatch] += affTokens[affiliation]
    
    newAffs = [None] * len(affArray)
    for i in tqdm(range(0, len(affArray)), desc = "Rewriting"):
        newAffs[i] = matchAffs[affArray[i]].replace("\n", ";")
    pyperclip.copy("\r\n".join(newAffs))
    
def manualMatcher(dispAffs, dispAffTable, affiliation, allAffs):
    for i in range(0, min(5, len(dispAffTable))):
        print(str(i + 1) + " - " + "{0: <3}".format(dispAffTable[i][1])[:3] + " | " + str(dispAffTable[i][0])[:150])
    print("\n" + affiliation)
    ans = input("\nSelect affiliation: ")
        
    if ans == "defer":
        affTable = concat([affTable, affTable[i:i+1]]).reset_index(drop = True)
        print("Deferred for later...\n")
    else:
        if ans == "0" or "replace" in ans:
            newAff = input("New Affiliation: ")
            if newAff == "": newAff = affiliation
            dispAffs[newAff] = 1
            allAffs[newAff] = newAff
            if "replace" in ans:
                replaceAff = dispAffTable[int(ans[7:]) - 1][0]
                del dispAffs[replaceAff]
                for aff in allAffs.keys():
                    if allAffs[aff] == replaceAff:
                        allAffs[aff] = newAff
        else:
            allAffs[affiliation] = dispAffTable[int(ans) - 1][0]  
        print("Set to :" + allAffs[affiliation])
    print("\n-------------------------------------------------\n")

# source: https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
# source: https://stackoverflow.com/questions/15173225/calculate-cosine-similarity-given-2-sentence-strings
def weightedCosine(str1Tokens, str2Tokens):
    bothTokens = set(str1Tokens).intersection(str2Tokens)
    numerator = sum([str1Tokens[token] * str2Tokens[token] for token in bothTokens])

    squareTokens1 = sum([str1Tokens[token] ** 2 for token in list(str1Tokens)])
    squareTokens2 = sum([str2Tokens[token] ** 2 for token in list(str2Tokens)])
    denominator = (squareTokens1 * squareTokens2) ** 0.5

    return 0 if denominator == 0 else numerator / denominator
    
def simpleCosine(str1Tokens, str2Tokens):
    bothTokens = set(str1Tokens).intersection(str2Tokens)
    return 0 if len(bothTokens) == 0 else len(bothTokens)/ (len(str1Tokens) * len(str2Tokens)) ** 0.5

def getAffiliationArray(defName):
    confirm = False
    while not confirm:
        filePath = input("\nName of affiliations excel file: ")
        filePath = Path(defName if filePath == "" else filePath)
        if not filePath.is_absolute():
            filePath = Path.joinpath(Path(__file__).parent.resolve(), filePath)
        print("File selected: " + str(filePath))
        if(filePath.is_file()):
            if(input("Type 'y' to confirm (Press enter otherwise): ").lower() == "y"):
                try:
                    affTable = read_excel(filePath)
                    confirm = True
                except:
                    print("Could not open file. Please try again.")
        else:
            print("Could not find file. Please try again.")
    return list(affTable.iloc[:,1])

__main__()
'''
from pandas import read_excel
import openpyxl
filePath = "C:\\Users\\emban\\OneDrive\\Desktop\\test.xlsx"
affTable = read_excel(filePath)
'''