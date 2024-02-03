import nltk, openpyxl
from pandas import read_excel
from pandas import concat
from pandas import DataFrame
from pathlib import Path
import pyperclip
#nltk.download('all')
from nltk.corpus import stopwords 
engStops = stopwords.words('english')   #list of trivial words: articles, prepositions, etc.

from nltk.tokenize import word_tokenize 
from math import floor

def __main__():
    affTable = getAffiliationTable()
    uniqueAffs = dict()
    
    i = 0
    numChanges = 1
    while numChanges > 0:
        numChanges = 0
        for i in range(0, affTable.shape[0]):
            author = affTable.iat[i,0]
            affiliation = affTable.iat[i,1]
            for aff in list(uniqueAffs.keys()):
                uniqueAffs[aff] = matchCosine(str(aff), str(affiliation))
            dispAffTable = sorted(uniqueAffs.items(), key= lambda x:x[1], reverse = True)
            if len(dispAffTable) > 0 and dispAffTable[0][1] > 0.85:
                affTable.iat[i,1] = dispAffTable[0][0]
                numChanges += 1
            else:
                uniqueAffs[affiliation] = 1
    affTable.to_clipboard()
    
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
def matchCosine(str1, str2):
    str1Tokens = {token for token in word_tokenize(str1.lower()) if token not in engStops}
    str2Tokens = {token for token in word_tokenize(str2.lower()) if token not in engStops}
    
    allTokens = str1Tokens.union(str2Tokens)
    str1Matches = str2Matches = bothMatches = 0
    for token in allTokens:
        if token in str1Tokens:
            str1Matches += 1
            bothMatches += 0.6
        if token in str2Tokens:
            str2Matches += 1
            bothMatches += 0.6
        bothMatches = floor(bothMatches)
        
    return 0 if str1Matches * str2Matches == 0 else bothMatches / (str1Matches * str2Matches) ** 0.5

def getAffiliationTable():
    confirm = False
    while not confirm:
        filePath = Path(input("\nName of affiliations excel file: "))
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
    return affTable

__main__()
'''
from pandas import read_excel
import openpyxl
filePath = "C:\\Users\\emban\\OneDrive\\Desktop\\test.xlsx"
affTable = read_excel(filePath)
'''