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
#returns a complete action object from an action string

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
     GRIEFER = 4

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
def ReturnChunkMetrics(parsedChunks, actionType, username):
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
     csvData = [[actionType + " Actions in Chunk"],
                chunkTotals]
     WriteCSV(csvData, actionType, username)
     return averagePerChunk

#write the metrics to a csv file we can use to create graphs              
def WriteCSV(data, actionType, username):
     #try:
     directory = ensure_dir(username + " metrics")
     newCSV = open(directory + '/' + actionType + 'Metrics.csv', 'w')
     with newCSV:
          writer = csv.writer(newCSV)
          writer.writerows(data)
     print("csv file successfully created")
     #except:
          #print("unable to write csv file (error)")

#process user input    
def ProcessUserInput(username, chunks):
     actionTypes = ["digs","places","punches","punched by", "crafts",
               "moves","takes","right-clicks","activates","uses",
               "wrote", "or type <all> to get each"]
     print("enter the action type to calculate the average. Available types are: ")
     for a in actionTypes:
          print(a)
     actionType = input()
     print(actionType)
     if(actionType == "all"):
          for a in actionTypes:
               print(a + " average per chunk: " + str(int(round(ReturnChunkMetrics(chunks, a, username)))))
     elif(actionType not in actionTypes):
          print("invalid action type, try again")
     else:
          print(actionType + " average per chunk: " +str(int(round(ReturnChunkMetrics(chunks, actionType, username)))))
     ProcessUserInput(username, chunks)
     
#get and process the given username
print('enter the username to identify (case sensitive)')
username = input()
#open the file
logToCheck = open("C:/Users/Josh/Documents/Serverlogs/UserLogs/ "+username+" .txt",'r', errors='ignore')
#read line by line
lines = logToCheck.read().splitlines()
allSessions = parseIntoSessions(username, lines)
#print(len(allSessions))
allChunks = SessionsIntoChunks(username, allSessions)

ProcessUserInput(username, allChunks)
