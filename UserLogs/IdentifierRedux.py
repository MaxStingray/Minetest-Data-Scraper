import datetime
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

def parseIntoSessions(username, linesToParse):
     #list of parsed sessions to return
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
                         #pop the login time and calculate the difference
                         thisDuration = datetime.combine(date.min, newSession.sessionEndTime) - datetime.combine(date.min, loginTime)
                         #add to session playtime
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
                              newAction.verb = splitString(stringToCheck, username + ' ', ' ')
                              newAction.block = splitString(stringToCheck, newAction.verb, ' at')
                              if('LuaEntitySAO' in newAction.block):
                                   newAction.block = ' Monster'
                              if('chest' in newAction.block):
                                   newAction.block = ' Chest'
                              if('sign' in newAction.block):
                                   newAction.block = ' Sign'
                              newSession.actionsInSession.append(newAction)
                         else:
                              pass
                         j += 1
          i += 1
     return parsedSessions
     
def SessionsIntoChunks(username, parsedSessions):
     parsedChunks = []
     chunkTime = timedelta(minutes = 10)
     for session in parsedSessions:
          newChunk = Chunk()
          if(session.totalSessionTime <= chunkTime):
               newChunk.sessionID = session.sessionID
               newChunk.actionsInChunk = session.actionsInSession
               parsedChunks.append(newChunk)
          else:
               sessionStart = session.sessionStartTime
               current = datetime.combine(date.min,sessionStart)
               numberOfChunks = int(round(session.totalSessionTime.seconds % 3600) / 60) / 10
               chunkIterator = 0
               while(chunkIterator <= numberOfChunks):
                    print("beginning of loop: " + str(chunkIterator), str(numberOfChunks))
                    endOfChunk = timePlus(current, chunkTime)
                    print("end of current chunk: " + str(endOfChunk))
                    #print(str(endOfChunk))
                    for action in session.actionsInSession:
                         if(datetime.combine(date.min, action.time) >= current):
                                   if(action.time <= endOfChunk):
                                        newChunk.actionsInChunk.append(action)          
                    newChunk.sessionID = session.sessionID
                         #print(str(len(newChunk.actionsInChunk)))
                    
                    parsedChunks.append(newChunk)
                    print("************NEW CHUNK************")
                    print("end of loop (appending): " + str(chunkIterator), str(numberOfChunks))
                    current = timePlus(current, chunkTime)
                    current = datetime.combine(date.min, current)
                    print("current at end of loop: " + str(current))
                    #print(str(current))
                    chunkIterator += 1
                    print("chunk itr end: " + str(chunkIterator))
                         
     return parsedChunks
#get and process the given username
print('enter the username to identify (case sensitive)')
username = input()
#open the file
logToCheck = open("C:/Users/Josh/Documents/Serverlogs/UserLogs/ "+username+" .txt",'r', errors='ignore')
#read line by line
lines = logToCheck.read().splitlines()
allSessions = parseIntoSessions(username, lines)
print(len(allSessions))
allChunks = SessionsIntoChunks(username, allSessions)

for chunk in allChunks:
     for action in chunk.actionsInChunk:
          print(str(action.time))

          
