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

#import the datetime modules for later 
import datetime
from datetime import datetime, date, time, timedelta
from PIL import Image
from vectors import Point, Vector

#returns a percentage of a number
def percent(part,whole):
    return 100*float(part)/float(whole)

#extract position vector from action line
def getVec(someString):
     vectorString = someString.split('(')[1].split(')')[0]
     x,y,z = vectorString.split(',')
     return Vector(x,y,z)

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
#check each line for actions and append if matching
i = 0
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
    elif("places" in stringToCheck):
        placeActions.append(stringToCheck)
    elif("CHAT" in stringToCheck):
        chatActions.append(stringToCheck)
    elif("punches" in stringToCheck):
        punchActions.append(stringToCheck)
    elif("crafts" in stringToCheck):
        craftActions.append(stringToCheck)
    elif("moves" in stringToCheck):
        storeActions.append(stringToCheck)
    elif("takes" in stringToCheck):
        storeActions.append(stringToCheck)
    elif("right-clicks" in stringToCheck):
        interactActions.append(stringToCheck)
    elif("activates" in stringToCheck):
        objInteractActions.append(stringToCheck)
    elif("uses" in stringToCheck):
        useActions.append(stringToCheck)
    elif("wrote" in stringToCheck):
        writeActions.append(stringToCheck)
    elif("punched by" in stringToCheck):
        punchActions.append(stringToCheck)
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
        #pop the login time and calculate the difference
        thisDuration = datetime.combine(date.min, logoutTime) - datetime.combine(date.min, loginStack.pop())
        #add to total playtime
        totalPlaytime += thisDuration
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
    
input()
