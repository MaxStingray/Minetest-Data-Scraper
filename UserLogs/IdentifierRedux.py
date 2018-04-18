import datetime
import csv
import os
from datetime import datetime, date, time, timedelta
from PIL import Image
from vectors import Point, Vector
from collections import Counter

#implimentation of a stack
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

#actions class for defining a complete action
class CompleteAction:
     def __init__(self):
          self.date = ""
          self.time = time()
          self.verb = ""
          self.block = ""

          
#class for describing a play session
class PlaySession:
     def __init__(self):
          self.actionsInSession = []
          self.sessionDate = ""
          self.sessionStartTime = time()
          self.sessionEndTime = time()
          self.totalSessionTime = timedelta()
          self.sessionID = 0

from enum import Enum
class Archetypes(Enum):
     BUILDER = 1
     MINER = 2
     FARMER = 3
     UNKNOWN = 4

class Motivations(Enum):
     ACTION = 1
     SOCIAL = 2
     MASTERY = 3
     ACHIEVEMENT = 4
     IMMERSION = 5
     CREATIVE = 6
     UNKNOWN = 7

class Motivation:
     def __init__(self):
          self.chunks = []
          self.type = Motivations.UNKNOWN
          self.subType = Motivations.UNKNOWN

class Archetype:
     def __init__(self):
          self.chunks = []
          self.classification = Archetypes.UNKNOWN

class FinalClassification:
     def __init__(self):
          self.motivation = Motivations.UNKNOWN
          self.subMotivation = Motivations.UNKNOWN
          self.Archetype = Archetypes.UNKNOWN

#ensure a directory exists, and create one if it doesn't
def ensure_dir(filePath):
     directory = filePath
     print(directory)
     if not os.path.exists(directory):
          directory = os.mkdir(directory)
     return directory
        
#class for describing a 10 minute chunk within a session
class Chunk:
     def __init__(self):
          self.sessionID = 0
          self.actionsInChunk = []

#returns a percentage of a number
def percent(part,whole):
    return 100*float(part)/float(whole)

def percentageIncrease(first, second):
     diff = second - first
     increase = diff/first * 100
     return increase

#extract position vector from action line
def getVec(someString):
     vectorString = someString.split('(')[1].split(')')[0]
     x,y,z = vectorString.split(',')
     return Vector(x,y,z)

#add timedelta to time
def timePlus(time, timedelta):
     start = datetime(
          2000, 1, 1,
          hour = time.hour, minute = time.minute, second = time.second)
     end = start+timedelta
     return end.time()

#splits a string between two given strings
def splitString(stringToSplit, start, end):
     return stringToSplit.split(start)[1].split(end)[0]

#find the average of a given dataset
def findAverage(dataSet):
     avg = float(sum(dataSet))/len(dataSet)
     return avg

class Block:
     def __init__(self):
          self.name = ""
          self.attributes = []

#load the block attributes dictionary
def loadBlockDictionary():
     print("processing block dictionary...")
     blockDict = []
     separator = "###"
     dictFile = open("C:/Users/Josh/Documents/ServerLogs/blockProperties.txt", 'r', errors='ignore')
     linesInFile = dictFile.read().splitlines()
     i = 0
     j = i
     while(i<len(linesInFile)):
          if separator in linesInFile[i]:
               newBlock = Block()
               j = i+1
               while(j<len(linesInFile)):
                    if newBlock.name is "" and separator not in linesInFile[j]:
                         newBlock.name = linesInFile[j]
                         j = j+1
                    elif separator not in linesInFile[j]:
                         newBlock.attributes.append(linesInFile[j])
                         j = j+1
                    elif separator in linesInFile[j]:
                         blockDict.append(newBlock)
                         i = j
                         break
               if i+1 == len(linesInFile):
                    break
     print("done!")
     return blockDict
     
#parse file into play sessions (set of actions between login/logout time)
def parseIntoSessions(username, linesToParse):
     #list of parsed sessions to return
     print("breaking data into sessions...")
     parsedSessions = []
     loginStack = Stack()
     i = 0
     sessionCount = 1
     while(i < len(linesToParse)):
          stringToCheck = linesToParse[i]
          if(username + " joins game" in stringToCheck):
               newSession = PlaySession()
               newSession.sessionDate = stringToCheck[0:10]
               timeStamp = splitString(stringToCheck, ' ', ' ')
               hours,minutes,seconds = timeStamp[:-1].split(":")
               newSession.sessionStartTime = time(int(hours), int(minutes), int(seconds))
               loginStack.push(newSession.sessionStartTime)
               #start new counter to find logout time
               j = i
               while(j < len(linesToParse)):
                    stringToCheck = linesToParse[j]
                    if(username + " leaves game" in stringToCheck):
                         timeStamp = splitString(stringToCheck, ' ', ' ')
                         hours,minutes,seconds = timeStamp[:-1].split(":")
                         newSession.sessionEndTime = time(int(hours), int(minutes), int(seconds))
                         loginTime = newSession.sessionStartTime
                         thisDuration = datetime.combine(date.min, newSession.sessionEndTime) - datetime.combine(date.min, loginTime)
                         newSession.totalSessionTime += thisDuration
                         newSession.sessionID = sessionCount
                         parsedSessions.append(newSession)
                         sessionCount += 1
                         i = j
                         break
                    else:
                         if('ACTION[Server]' in stringToCheck and 'CHAT' not in stringToCheck
                            and 'List of players' not in stringToCheck):
                              newAction = CompleteAction()
                              newAction.date = stringToCheck[0:10]
                              newTimeStamp = splitString(stringToCheck, ' ', ' ')
                              hours,minutes,seconds = newTimeStamp[:-1].split(":")
                              newAction.time = time(int(hours), int(minutes), int(seconds))
                              newAction.time = datetime.combine(date.min, newAction.time)
                              newAction.verb = splitString(stringToCheck, username + ' ', ' ')
                              newAction.block = splitString(stringToCheck, newAction.verb, ' at')
                              if('LuaEntitySAO' in newAction.block):
                                   newAction.block = ' Monster'
                              if('chest' in newAction.block):
                                   newAction.block = ' Chest'
                              if('sign' in newAction.block):
                                   newAction.block = ' Sign'
                              #TODO: Get position vector with getVec, add to action
                              newSession.actionsInSession.append(newAction)
                         else:
                              pass
                         j += 1
          i += 1
     print("done!")
     return parsedSessions

#parse sessions into 10 minute chunks
def SessionsIntoChunks(username, parsedSessions):
     print("breaking sessions into chunks...")
     parsedChunks = []
     allCheckedActions = []
     chunkTime = timedelta(minutes = 10)
     for session in parsedSessions:
          if(session.totalSessionTime <= chunkTime):
               newChunk = Chunk()
               newChunk.sessionID = session.sessionID
               newChunk.actionsInChunk = session.actionsInSession
               parsedChunks.append(newChunk)
          else:
               sessionStart = session.sessionStartTime
               current = datetime.combine(date.min,sessionStart)
               numberOfChunks = int(round(session.totalSessionTime.seconds % 3600) / 60) / 10
               chunkIterator = 0
               while(chunkIterator <= numberOfChunks):
                    newChunk = Chunk()
                    #print("**********NEW CHUNK" + " #" + str(chunkIterator) + "**********")
                    endOfChunk = timePlus(current, chunkTime)
                    endOfChunk = datetime.combine(date.min, endOfChunk)
                    #print("start of chunk: " + str(current))
                    #print("end of chunk: " + str(endOfChunk))
                    for action in session.actionsInSession:
                         action.time = timePlus(action.time, timedelta(minutes = 0))
                         action.time = datetime.combine(date.min, action.time)
                         if(action.time >= current):
                              if(action.time <= endOfChunk):
                                   newChunk.actionsInChunk.append(action)
                                   allCheckedActions.append(action)
                    newChunk.sessionID = session.sessionID
                    parsedChunks.append(newChunk)
                    current = endOfChunk
                    chunkIterator += 1
     print("done!")                    
     return parsedChunks

#returns a normalised average of the given action type (eg. place, dig, etc)
def ReturnChunkMetrics(parsedChunks, actionType, username, writeToFile):
     chunkTotals = []
     chunkIDs = []
     chunkCounter = 1
     for chunk in parsedChunks:
          #print("*********CHECKING NEXT CHUNK**********")
          matchingActions = []
          chunkIDs.append(chunkCounter)
          actionCount = 0
          for action in chunk.actionsInChunk:
               if(action.verb == actionType):
                    #print(action.time, action.verb, action.block)
                    actionCount += 1
          totalForThisChunk = actionCount
          chunkTotals.append(totalForThisChunk)
          chunkCounter += 1
     averagePerChunk = findAverage(chunkTotals)
     if(writeToFile):
          csvData = [[actionType + " Actions in Chunk"],
                     chunkTotals]
          WriteCSV(csvData, actionType, username)
     return averagePerChunk

def ArchetypeClassification(chunks, username):
     archetypeAssumption = Archetypes.UNKNOWN
     #get the averages of each action type in the given chunks
     digAverage = ReturnChunkMetrics(chunks, "digs", username, False)
     placeAverage = ReturnChunkMetrics(chunks, "places", username, False)
     chestAverage = ReturnChunkMetrics(chunks, "moves", username, False)
     #initialise the min and max bounds of each classification
     unknownMin, unknownMax = 0, 29
     builderMin, builderMax = 60, 89
     farmerMin, farmerMax = 30, 59
     minerMin = 90
     #find the dig/place percentage increase
     increase = percentageIncrease(placeAverage, digAverage)
     print(str(increase))
     print("dig average = " + str(digAverage))
     print("place average = " + str(placeAverage))
     #check against the bounds
     if increase >= unknownMin and increase <= unknownMax:
          archetypeAssumption = Archetypes.UNKNOWN
     elif increase >= builderMin and increase <= builderMax:
          archetypeAssumption = Archetypes.BUILDER
     elif increase >= minerMin:
          archetypeAssumption = Archetypes.MINER
     elif increase < unknownMin:
          archetypeAssumption = Archetypes.BUILDER
     elif increase >= farmerMin and increase <= farmerMax:
          if(chestAverage > 2):
               archetypeAssumption = Archetypes.FARMER
          else:
               archetypeAssumption = Archetypes.BUILDER
     else:
          archetypeAssumption = Archetypes.UNKNOWN

     finalArchetype = Archetype()
     finalArchetype.chunks = chunks
     finalArchetype.classification = archetypeAssumption

     return finalArchetype

def ContextCheck(chunks, blockDictionary, archetype):
     finalMotivation = Motivation()
     #totals
     ActionTotal = 0
     SocialTotal = 0
     MasteryTotal = 0
     AchievementTotal = 0
     ImmersionTotal = 0
     CreativityTotal = 0
     FarmingTotal = 0
     BuildingTotal = 0
     MiningTotal = 0
     #TODO all this
     for chunk in chunks:
          for action in chunk.actionsInChunk:
               for block in blockDictionary:
                    if action.block in block.name:
                         for a in block.attributes:
                              if a == "Action":
                                   ActionTotal += 1
                              elif a == "Social":
                                   SocialTotal += 1
                              elif a == "Mastery":
                                   MasteryTotal += 1
                              elif a == "Achievement":
                                   AchievementTotal += 1
                              elif a == "Immersion":
                                   ImmersionTotal += 1
                              elif a == "Creativity":
                                   CreativityTotal += 1
                              elif a == "Farmer":
                                   FarmingTotal += 1
                              elif a == "Miner":
                                   MiningTotal += 1
                              elif a == "Builder":
                                   BuildingTotal +=1

     motivationTotals = [ActionTotal, SocialTotal, MasteryTotal, AchievementTotal, ImmersionTotal, CreativityTotal]
     highestMotivation = max(motivationTotals)

     if highestMotivation == ActionTotal:
          finalMotivation.type = Motivations.ACTION
     elif highestMotivation == SocialTotal:
          finalMotivation.type = Motivations.SOCIAL
     elif highestMotivation == MasteryTotal:
          finalMotivation.type = Motivations.MASTERY
     elif highestMotivation == AchievementTotal:
          finalMotivation.type = Motivations.ACHIEVEMENT
     elif highestMotivation == ImmersionTotal:
          finalMotivation.type = Motivations.IMMERSION
     elif highestMotivation == CreativityTotal:
          finalMotivation.type = Motivations.CREATIVE
     else:
          finalMotivation.type = Motivations.UNKNOWN

     motivationTotals.remove(highestMotivation)
     highestMotivation = max(motivationTotals)
     
     if highestMotivation == ActionTotal:
          finalMotivation.subType = Motivations.ACTION
     elif highestMotivation == SocialTotal:
          finalMotivation.subType = Motivations.SOCIAL
     elif highestMotivation == MasteryTotal:
          finalMotivation.subType = Motivations.MASTERY
     elif highestMotivation == AchievementTotal:
          finalMotivation.subType = Motivations.ACHIEVEMENT
     elif highestMotivation == ImmersionTotal:
          finalMotivation.subType = Motivations.IMMERSION
     elif highestMotivation == CreativityTotal:
          finalMotivation.subType = Motivations.CREATIVE
     else:
          finalMotivation.subType = Motivations.UNKNOWN
     
     print("action total: " + str(ActionTotal))
     print("social total: " + str(SocialTotal))
     print("mastery total: " + str(MasteryTotal))
     print("achievement total: " + str(AchievementTotal))
     print("immersion total: " + str(ImmersionTotal))
     print("creativity total: " + str(CreativityTotal))

     #calculate archetype percentages
     builderPercentage = percent(percent(BuildingTotal, 100), 60)
     if archetype == Archetypes.BUILDER:
          builderPercentage += 40
     minerPercentage = percent(percent(MiningTotal, 100), 60)
     if archetype == Archetypes.MINER:
          minerPercentage += 40
     farmerPercentage = percent(percent(FarmingTotal, 100), 60)
     if archetype == Archetypes.FARMER:
          farmerPercentage += 40

     archetypePercentages = [builderPercentage, minerPercentage, farmerPercentage]
     highestArchetype = max(archetypePercentages)

     finalClassification = FinalClassification()
     finalClassification.Motivation = finalMotivation.type
     finalClassification.SubMotivation = finalMotivation.subType
     
     if highestArchetype == builderPercentage:
          finalClassification.Archetype = Archetypes.BUILDER
     elif highestArchetype == minerPercentage:
          finalClassification.Archetype = Archetypes.MINER
     elif highestArchetype == farmerPercentage:
          finalClassification.Archetype = Archetypes.FARMER
     else:
          finalClassification.Archetype = Archetypes.UNKNOWN    
     print(finalClassification.Motivation)
     print(finalClassification.SubMotivation)
     print(finalClassification.Archetype)
     #return finalMotivation

#write the metrics to a csv file we can use to create graphs              
def WriteCSV(data, actionType, username):
     directory = ensure_dir(username + " metrics")
     newCSV = open(str(directory) + '/' + actionType + 'Metrics.csv', 'w')
     with newCSV:
          writer = csv.writer(newCSV)
          writer.writerows(data)
     print("csv file successfully created")

#process user input    
def ProcessUserInput(username, chunks, blockDict):
     actionTypes = ["digs","places","punches","punched by", "crafts",
               "moves","takes","right-clicks","activates","uses",
               "wrote", "or type <identify> to get classification"]
     print("enter the action type to calculate the average. Available types are: ")
     for a in actionTypes:
          print(a)
     actionType = input()
     print(actionType)
     if(actionType == "all"):
          for a in actionTypes:
               print(a + " average per chunk: " + str(int(round(ReturnChunkMetrics(chunks, a, username, True)))))
     elif(actionType == "identify"):
          i = 0
          chunksToIdentify = []
          while(i <= 48):
               if(chunks[i]):
                    chunksToIdentify.append(chunks[i])
               i += 1
          archetype = ArchetypeClassification(chunksToIdentify, username)
          print(str(archetype.classification))
          ContextCheck(chunksToIdentify, blockDict, archetype.classification)
     elif(actionType not in actionTypes):
          print("invalid action type, try again")
     else:
          print(actionType + " average per chunk: " +str(int(round(ReturnChunkMetrics(chunks, actionType, username, True)))))
     ProcessUserInput(username, chunks, blockDict)

#load the block dictionary
blockDict = loadBlockDictionary()

#get and process the given username
print('enter the username to identify (case sensitive)')
username = input()
#open the file
logToCheck = open("C:/Users/Josh/Documents/Serverlogs/UserLogs/ "+username+" .txt",'r', errors='ignore')
#read line by line
lines = logToCheck.read().splitlines()
allSessions = parseIntoSessions(username, lines)
print(str(len(allSessions)))
#print(len(allSessions))
allChunks = SessionsIntoChunks(username, allSessions)
print(str(len(allChunks)))

ProcessUserInput(username, allChunks, blockDict)
