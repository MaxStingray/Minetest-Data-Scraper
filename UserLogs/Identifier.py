#returns a percentage of a number
def percent(part,whole):
    return 100*float(part)/float(whole)
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
#check each line for actions and increment actions if matching
i = 0
while(i<length):
    stringToCheck = lines[i]
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
input()
