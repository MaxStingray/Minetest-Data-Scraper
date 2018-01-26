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
numPlace = 0
numDig = 0
numChat = 0
numPunch = 0
numJunk = 0
numCraft = 0
numStore = 0
numWrite = 0
numUse = 0
numInteract = 0
numObjInteract = 0
numDamaged = 0
#check each line for actions and increment actions if matching
i = 0
while(i<length):
    stringToCheck = lines[i]
    if("digs" in stringToCheck):
        numDig+=1
    elif("places" in stringToCheck):
        numPlace+=1
    elif("CHAT" in stringToCheck):
        numChat+=1
    elif("punches" in stringToCheck):
        numPunch+=1
    elif("crafts" in stringToCheck):
        numCraft+=1
    elif("moves" in stringToCheck):
        numStore+=1
    elif("takes" in stringToCheck):
        numStore+=1
    elif("right-clicks" in stringToCheck):
        numInteract+=1
    elif("activates" in stringToCheck):
        numObjInteract+=1
    elif("uses" in stringToCheck):
        numUse+=1
    elif("wrote" in stringToCheck):
        numWrite+=1
    elif("punched by" in stringToCheck):
        numDamaged+=1
    else:
        print(stringToCheck)
        numJunk+=1
    i+=1
#find percentage values and print
print("place actions: " + str(numPlace) + " (" + str(percent(numPlace,length)) + " percent)")
print("dig actions: " + str(numDig)+ " (" + str(percent(numDig,length)) + " percent)")
print("chat actions: " + str(numChat)+ " (" + str(percent(numChat,length)) + " percent)")
print("punch actions: " + str(numPunch)+ " (" + str(percent(numPunch,length)) + " percent)")
print("damaged by opponent: " + str(numDamaged)+ " (" + str(percent(numDamaged,length)) + " percent)")
print("craft actions: " + str(numCraft)+ " (" + str(percent(numCraft,length)) + " percent)")
print("storage actions: " + str(numStore)+ " (" + str(percent(numStore,length)) + " percent)")
print("writing actions: " + str(numWrite)+ " (" + str(percent(numWrite,length)) + " percent)")
print("player/npc interactions: " + str(numInteract)+ " (" + str(percent(numInteract,length)) + " percent)")
print("object interactions: " + str(numObjInteract)+ " (" + str(percent(numObjInteract,length)) + " percent)")
print("use actions: " + str(numUse)+ " (" + str(percent(numUse,length)) + " percent)")
print("junk actions (discard): " + str(numJunk)+ " (" + str(percent(numJunk,length)) + " percent)")
input()
