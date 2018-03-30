#import the datetime modules for later
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

#structure for complete actions to make em readable
class CompleteAction:
     def __init__(self):
          self.action = ""
          self.verb = ""
          self.position = Vector(0,0,0)
          self.time = time()
          self.date = ""
     
#structure for describing a play session
class PlaySession:
     def __init__(self):
          self.start = time(0,0,0)
          self.numChunks = 0
          self.allActionsInChunk = []
          self.sessionDate = ""

     def setStart(self, startTime):
          self.start = startTime

     def getStart(self):
          return self.start

     def setChunks(self, totalChunks):
          self.numChunks = totalChunks

     def getChunks(self):
          return self.numChunks
     

#a 10 minute chunk and all actions within it
class Chunk:
     def __init__(self):
          self.actionsInChunk = []

     def addAction(self, action):
          self.actionsInChunk.append(action)

     def getActions(self):
          return self.actionsInChunk
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

def ChunkData(sessions, actions):
     print("breaking data into chunks...")
     completeChunks = []
     #loop through all play sessions
     for session in sessions:
          #get the start time of the session
          start = session.getStart()
          currentDate = session.sessionDate
          #set a "current" to keep track of current increment
          current = datetime.combine(date.min, start)
          #iterate through the number of chunks per session
          x = 0
          while(x < session.numChunks):
               #create a new chunk object for the session
               nextChunk = Chunk()
               #loop through all actions
               for action in actions:
                    if(action.date == currentDate):
                         #if timetstamp is between current and current + 10 min
                         endOfChunk = timePlus(current, timedelta(minutes = 10))
                         if(datetime.combine(date.min,action.time) >= current):
                              if(action.time <= endOfChunk):
                                   #add the action to the chunk object
                                   nextChunk.addAction(action)
                                   #add the finished chunk to the collection of chunks
                                   if(nextChunk not in completeChunks):
                                        completeChunks.append(nextChunk)
               #increment current to keep track
               current = datetime.combine(date.min,endOfChunk)
               x += 1
     print("Done!")
     return completeChunks
     


#get and process the given username
print('enter the username to identify (case sensitive)')
username = input()
#open the file
logToCheck = open("C:/Users/Josh/Documents/Serverlogs/UserLogs/ "+username+" .txt",'r', errors='ignore')
#read line by line
lines = logToCheck.read().splitlines()
#get the number of actions in the file
length = len(lines)
#initialise the action variables
placeActions = []
digActions = []
chatActions = []
punchActions = []
junkActions = []
craftActions = []
storeActions = []
writeActions = []
useActions = []
interactActions = []
objInteractActions = []
damagedActions = []
totalActions = []
#list for junk items (irrelevant data)
junk = []
numJunk = 0
#positional data for digging and placing
digPositions = []
placePositions = []
#create stack object
loginStack = Stack()
#separate the timestamp elements into strings
hours = ''
minutes = ''
seconds = ''
totalPlaytime = timedelta()
#the number of 10 minute chunks
#check each line for actions and append if matching
i = 0
#collection of all play sessions to find chunks
allSessions = []
while(i<length):
    stringToCheck = lines[i]
    #as the timestamp will always be between the first two spaces in the string, we can extract it like this
    try:
        newTimeStamp = stringToCheck.split(' ')[1].split(' ')[0]
    except:#just ignore whitespace lines for now (there are many)
        pass
     #append the action collections    
    if("digs" in stringToCheck):
        digActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif("places" in stringToCheck):
        placeActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif("CHAT" in stringToCheck):
        chatActions.append(stringToCheck)
    elif("punches" in stringToCheck):
        punchActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif("crafts" in stringToCheck):
        craftActions.append(stringToCheck)
    elif("moves" in stringToCheck):
        storeActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif("takes" in stringToCheck):
        storeActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif("right-clicks" in stringToCheck):
        interactActions.append(stringToCheck)
    elif("activates" in stringToCheck):
        objInteractActions.append(stringToCheck)
    elif("uses" in stringToCheck):
        useActions.append(stringToCheck)
    elif("wrote" in stringToCheck):
        writeActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif("punched by" in stringToCheck):
        punchActions.append(stringToCheck)
        totalActions.append(stringToCheck)
    elif(username + " joins game" in stringToCheck):
        #remove final colon and extract hours, minutes and seconds
        hours,minutes,seconds = newTimeStamp[:-1].split(":")
        #create timestamp we can do stuff with
        loginTime = time(int(hours), int(minutes), int(seconds))
        #push to the stack
        loginStack.push(loginTime)#push
    elif(username + " leaves game" in stringToCheck):
        #remove final colon and extract hours, minutes and seconds
        hours,minutes,seconds = newTimeStamp[:-1].split(":")
        #create timestamp we can do stuff with
        logoutTime = time(int(hours), int(minutes), int(seconds))
        loginTime = loginStack.pop()
        #pop the login time and calculate the difference
        thisDuration = datetime.combine(date.min, logoutTime) - datetime.combine(date.min, loginTime)
        #add to total playtime
        totalPlaytime += thisDuration
        #find number of 10 minute chunks in this period
        #set start time to 0
        totalPlaytimeForCalc = timedelta()
        #add the duration
        totalPlaytimeForCalc += thisDuration
        #calculate number of 10 minute periods, rounded to nearest integer
        numberOfTenMinuteChunks = int(round((totalPlaytimeForCalc.seconds % 3600) / 60) / 10)
        nextSession = PlaySession()
        nextSession.setStart(loginTime)
        nextSession.setChunks(numberOfTenMinuteChunks)
        nextSession.sessionDate = stringToCheck[0:10]
        #print("session start time: " + str(nextSession.getStart()) + " , " + "number of chunks: " + str(nextSession.getChunks()))
        allSessions.append(nextSession)
    else:
        junk.append(stringToCheck)
    i+=1
        
finalLength = (length - len(junk))


#find percentage values and print
print("place actions: " + str(len(placeActions)) + " (" + str(percent(len(placeActions),finalLength)) + " percent)")
print("dig actions: " + str(len(digActions))+ " (" + str(percent(len(digActions),finalLength)) + " percent)")
print("chat actions: " + str(len(chatActions))+ " (" + str(percent(len(chatActions),finalLength)) + " percent)")
print("punch actions: " + str(len(punchActions))+ " (" + str(percent(len(punchActions),finalLength)) + " percent)")
print("damaged by opponent: " + str(len(damagedActions))+ " (" + str(percent(len(damagedActions),finalLength)) + " percent)")
print("craft actions: " + str(len(craftActions))+ " (" + str(percent(len(craftActions),finalLength)) + " percent)")
print("storage actions: " + str(len(storeActions))+ " (" + str(percent(len(storeActions),finalLength)) + " percent)")
print("writing actions: " + str(len(writeActions))+ " (" + str(percent(len(writeActions),finalLength)) + " percent)")
print("player/npc interactions: " + str(len(interactActions))+ " (" + str(percent(len(interactActions),finalLength)) + " percent)")
print("object interactions: " + str(len(objInteractActions))+ " (" + str(percent(len(objInteractActions),finalLength)) + " percent)")
print("use actions: " + str(len(useActions))+ " (" + str(percent(len(useActions),finalLength)) + " percent)")
print("junk actions (discarded): " + str(len(junk)))
print("number of lines: " + str(length))
#display the total playTime
print("total playtime: " + str(totalPlaytime))


#let's make some graphs
startTime = timedelta()
#this gets total number of hours
totalHours = totalPlaytime.days * 24 + totalPlaytime.seconds/3600
#we want the number of ten minute periods
#get the total playtime in hours for visualisation
print("total hours: " + str(totalHours))
#round to next hour
print("rounded total hours: " + str(int(round(totalHours))))
#use the rounded hours as the graph x axis
actions = []
for action in totalActions:
     #get the string formatted timestamps and vectors
     try:
        verb = action.split(username + ' ')[1].split(' ')[0]
        newTimeStamp = action.split(' ')[1].split(' ')[0]
        newDate = action[0:10]
        newVectorStr = action.split('(')[1].split(')')[0]
        newBlock = action.split(verb)[1].split(' at')[0]
        if('LuaEntitySAO' in newBlock):
             newBlock = ' Monster'
        if('chest' in newBlock):
             newBlock = ' Chest'
        if('sign' in newBlock):
             newBlock = ' Sign'
     except:#just ignore whitespace lines for now (there are many)
        pass
     #grab the int components of each
     hours,minutes,seconds = newTimeStamp[:-1].split(":")
     x,y,z = newVectorStr.split(",")
     #convert to time type
     actionTime = time(int(hours), int(minutes), int(seconds))
     #convert to vector type
     actionPos = Vector(float(x),float(y),float(z))
     newAction = CompleteAction()
     newAction.verb = verb
     newAction.action = newBlock
     newAction.position = actionPos
     newAction.time = actionTime
     newAction.date = newDate
     actions.append(newAction)
#now we have a collection of precise timestamps and a maximum range for them
#as well as a collection of positions. Should be able to make graphs now.

chunkList = ChunkData(allSessions, actions)
totalbla = 0
chunkiterator = 0
for chunk in chunkList:
     print("chunk #" + str(chunkiterator))
     print(str(len(chunk.actionsInChunk)))
     chunkiterator += 1
     
#collection of all blocks interacted with by the player
interactedBlocks = []
for action in actions:
     interactedBlocks.append(action.action)

#calculate distance travelled
import numpy as np
i = 1
dist = 0
#for every action, find the distance between its position and the one preceeding it. Add to total distance
while(i < len(actions)):
     a = np.array((actions[i].position.x, actions[i].position.y, actions[i].position.z))
     b = np.array((actions[i - 1].position.x, actions[i - 1].position.y, actions[i - 1].position.z))
     dist += np.linalg.norm(a-b)
     i += 1

print("total distance travelled: " + str(int(round(dist))) + " blocks")

#use counter :D
blockCounter = Counter(interactedBlocks)

for block in blockCounter:
     print('%s : %d' % (block, blockCounter[block]))



#find action with highest count
#make first assumption as to archetype
input()
