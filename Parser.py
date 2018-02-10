import os

print("server debug file parser")

#open the file to parse. r = read, w = write, a = append
debugFile = open('C:/Users/Josh/Documents/ServerLogs/debug.txt', 'r', errors='ignore')
#create list of lines
lines = debugFile.read().splitlines()
#get the number of lines in the file
length = len(lines)
#iterate over each line of the collection
i = 0
uniqueNameList = []
while(i<length):
    stringToCheck = lines[i]
    if 'ACTION[Server]: ' in stringToCheck:#check only the action lines
        start = 'ACTION[Server]: '
        end = ' '
        if('joins game' not in stringToCheck):#filter out server actions
            if('WARNING' not in stringToCheck):
                username = " " + stringToCheck.split(start)[1].split(end)[0] + " "#get the username from the string
                if('|' not in username):#check for special characters. Should ban these.
                    if('protect' not in username):
                        if('Announcing' not in username):
                            if('CHAT' not in username):
                                if('facedir' not in username):
                                    if('Giving' not in username):
                                        if('Moving' not in username):
                                            if('Server' not in username):
                                                if('TOSERVER_CLIENT_READY' not in username):
                                                    if('Ð' not in username):
                                                        uniqueNameList.append(username)#add username to collection of usernames
    i=i+1
#now create a set of unique names
uniqueNameSet = set(uniqueNameList)
uniqueNameList = list(set(uniqueNameSet))
j = 0
#create a new text file for each user
while(j<len(uniqueNameList)):
    try:
        f = open("C:/Users/Josh/Documents/ServerLogs/UserLogs/"+uniqueNameList[j]+".txt","w+")#create the file
        print('creating file for: ' + uniqueNameList[j])
        i = 0
        while(i<length):#find each line attributed with the username and write to file
            stringToCheck = lines[i]
            if(uniqueNameList[j] in stringToCheck):
                f.write(lines[i] + '\r\n')
            if("<"+uniqueNameList[j].strip()+">" in stringToCheck):#separate statement for chat events
                f.write(lines[i] + '\r\n')
            i=i+1
        j=j+1
    except Exception as ex:
        raise ex
        print("invalid filename. Skipping...")
        i=i+1
        j=j+1

print("removing small files...")
thisLocation = 'C:\\Users\\Josh\\Documents\\ServerLogs\\UserLogs\\'
numDeleted = 0
#create collection of files
logs = []
#add .txt files only to the collection
for file in os.listdir(thisLocation):
    try:
        if file.endswith(".txt"):
            logs.append(thisLocation + file)
    except Exception as e:
        raise e
        print("no files found")
logsToRemove = []
removedCount = 0
for logToCheck in logs:
    lineCount = 0
    with open(logToCheck) as f:
        for line in f:
            lineCount += 1
        if lineCount <= 300:
            print("small file detected" + str(lineCount))
            removedCount += 1
            logsToRemove.append(logToCheck)

for f in logsToRemove:
    os.remove(f)

print(removedCount + " files deleted (too small)")
print('...Done')
debugFile.close()
