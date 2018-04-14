import os
from collections import Counter


def splitString(stringToSplit, start, end):
    return stringToSplit.split(start)[1].split(end)[0]

def readFile(filePath):
    fileToRead = open(filePath, 'r', errors ='ignore')
    lines = fileToRead.read().splitlines()
    actionLines = []
    actionTypes = ["digs","places","punches","punched by", "crafts",
               "moves","takes","right-clicks","activates","uses",
               "wrote"]
    for line in lines:
        for action in actionTypes:
            if action in line:
                actionLines.append(line)
    return identifyBlocks(actionLines)
    
def identifyBlocks(parsedLines):
    blockLines = []
    for line in parsedLines:
        username = ""
        try:
            username = splitString(line, 'ACTION[Server]: ', ' ')
            verb = splitString(line, username + " ", ' ')
            block = splitString(line, verb + " ", ' ')
            blockLines.append(block)
        except:
            print("invalid line found and discarded: " + line)
    return blockLines

print("block dictionary definition")

actionLines = readFile('C:/Users/Josh/Documents/ServerLogs/debug.txt')
uniqueBlockSet = set(actionLines)
uniqueBlockList = list(set(uniqueBlockSet))

blockCounter = Counter(actionLines)

for block in blockCounter:
    print('%s : %d' % (block, blockCounter[block]))

