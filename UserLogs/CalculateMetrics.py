#for use by the identifier script. Calculates averages of all actions for comparison
class CalculateMetrics:
    from pathlib import Path

    placeTotal = []
    digTotal = []
    chatTotal = []
    punchTotal = []
    craftTotal = []
    storeTotal = []
    writeTotal = []
    useTotal = []
    interactTotal = []
    objInteractTotal = []
    damagedTotal = []
    
    directory = 'C:/Users/Josh/Desktop/SystemsGit/Minetest-Data-Scraper/UserLogs'

    files = []
    for pth in Path.cwd().iterdir():
        if(pth.suffix == '.txt'):
            files.append(pth)

    #you basically wanna do a huge chunk of the identifier script here
    #measure actions into the same categories then dump the averages someplace
    for filename in files:

        #initialise the collections
        placeActions = []
        digActions = []
        chatActions = []
        punchActions = []
        craftActions = []
        storeActions = []
        writeActions = []
        useActions = []
        interactActions = []
        objInteractActions = []
        damagedActions = []
        
        logToCheck = open(filename, 'r',errors ='ignore')
        lines = logToCheck.read().splitlines()
        length = len(lines)
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
            i+=1

        placeTotal.append(len(placeActions))
        digTotal.append(len(digActions))
        chatTotal.append(len(chatActions))
        punchTotal.append(len(punchActions))
        craftTotal.append(len(craftActions))
        storeTotal.append(len(storeActions))
        writeTotal.append(len(writeActions))
        useTotal.append(len(useActions))
        interactTotal.append(len(interactActions))
        objInteractTotal.append(len(objInteractActions))
        damagedTotal.append(len(damagedActions))

    def placeAvg:
        avg = float(sum(placeTotal))/len(placeTotal)
        return avg

    def digAvg:
        avg = float(sum(digTotal))/len(digTotal)
        return avg

    
            
    
    
        
    
