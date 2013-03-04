#TODO: Make eneHEAL, eneTYPE, eneNAME, and eneGEND changeable through external files
#TODO: Make plyHEAL changeable through external files

import random,time
eneHEAL = [100,100,100,100]
eneTYPE = [1,1,3,2]
eneNAME = ["Joseph the Rouge","Angelo the Sneak","George the Cultmaster","Kate the Necromancer"]
eneGEND = ["he","he","he","she"]

plyHEAL = 100
living = True
wonGame = False

while living and wonGame == False:
    print
    print "Your turn, Player."
    FILE = open("character/attacks.txt","r") #Grab from
    attacks = FILE.readlines() #Read lines
    FILE.close() #Close File
    print "Please choose one:"
    temp2 = attacks[0].strip()
    for temp in range(1,len(attacks)): temp2 += ", " + attacks[temp].strip() #Put list into one variable
    print temp2
    instruct = raw_input() #get input
    for temp in range(0,len(attacks)):
        if instruct.lower() == attacks[temp].strip(): temp2 = True #loop through possible answers and check if correct
    #if accepted and not accepted
    if temp2 == True: pass
    else: print "\"" + instruct + "\" is not valid!"; continue

    attack = instruct

    #This is the same as for the AI, but has edits.
    #removed SWITCH, affectPlayer is now inverted
    #Get attack info
    get = "plays/" + attack + ".txt" #Figures out which file to use
    FILE = open(get,"r") #Grab from
    instructions = FILE.readlines() #Read lines
    FILE.close() #Close File

    #Runs file's instructions
    affectPlayer = True #For player, this is if the attack is AoE
    genRandom = 0
    for temp2 in range(0,len(instructions)): #Read instructions
        instruct = instructions[temp2].strip() #Remove \n from line
        instruct = instruct.replace("genRANDOM",str(genRandom)) #Replace genRANDOM with the random number
            
        if instruct == "PLAYER": affectPlayer = False #If it affects the player
            
        #Checks if line is a number
        number = True
        try: int(instruct)
        except: number = False

        #Random number generation
        if instruct[:6]=="RANDOM": prt1=instruct[6:].split("|")[0];prt2=instruct[6:].split("|")[1];genRandom=random.randint(int(prt1),int(prt2))
        
            
        if number and affectPlayer: #if number and AoE
            print "Player used " + attack + "!"
            plyHEAL += int(instruct) #Changes player's health
            if instruct <= 0: print "Player gave " + str(instruct) + " health to all opponents!" #Prints out heal
            else: print "Player dealt " + str(abs(int(instruct))) + " damage to all opponents!" #Prints out damage
        elif number: #if number but now AoE
            print "Please choose one:"
            temp2 = False
            for temp in range(0,len(eneNAME)):
                if eneHEAL[temp] > 0:
                    if temp2 == False: temp2 = eneNAME[temp].split(" ", 1)[0]
                    else: temp2 += ", " + eneNAME[temp].split(" ", 1)[0] #Put list into one variable
            print temp2
            
            instruct2 = raw_input() #Get input
            for temp in range(0,len(eneNAME)):
                if instruct2.lower() == eneNAME[temp].split(" ", 1)[0].lower(): temp2 = True; temp3 = temp#loop through possible answers and check if correct
            #if accepted and not accepted
            if temp2 == True: pass
            else: print "\"" + instruct2 + "\" is not valid!"; break
            print
            print "Player used " + attack + "!"
            if instruct <= 0: print "Player gave " + str(instruct) + " health to " + eneNAME[temp3] + "!" #Prints out heal
            else: print "Player dealt " + str(abs(int(instruct))) + " damage to " + eneNAME[temp3] + "!" #Prints out damage
            eneHEAL[temp3] += int(instruct)
            if eneHEAL[temp3] <= 0: print eneNAME[temp3] + " has been been defeated by Player!"
            else: print eneNAME[temp3] + " now has " + str(eneHEAL[temp3]) + " health!"

    pass
    if temp2 == False: continue #If player's 'who to attack' was invalid
    #AI===========================================================
    
    for temp in range(0,len(eneTYPE)): #Get enemy's cards for turn
        if eneHEAL[temp] <= 0: continue
        time.sleep(0.75)
        print
        #Choose attack
        get = "eneTYPES/" + str(eneTYPE[temp]) + ".txt" #Figures out which file to use
        FILE = open(get,"r") #Grab from
        attacks = FILE.readlines() #Read lines
        FILE.close() #Close File
        attackNUM = random.randint(0,len(attacks)) #Chooses which attack to use
        if attackNUM == len(attacks): continue #ocassionally passes
        attack = attacks[attackNUM].strip() #attack = the attack it's going to use

        print eneNAME[temp]+" used "+str(attack).title()+"!" #Commentary

        #Get attack info
        get = "plays/" + attack + ".txt" #Figures out which file to use
        FILE = open(get,"r") #Grab from
        instructions = FILE.readlines() #Read lines
        FILE.close() #Close File

        #Runs file's instructions
        affectPlayer = False
        genRandom = 0
        for temp2 in range(0,len(instructions)): #Read instructions
            instruct = instructions[temp2].strip() #Remove \n from line
            instruct = instruct.replace("genRANDOM",str(genRandom)) #Replace genRANDOM with the random number
            
            if instruct == "PLAYER": affectPlayer = True #If it affects the player

            if instruct[:6]=="SWITCH": eneTYPE[temp] = instruct[6:] #Switch to a different enemy type
            
            #Checks if line is a number
            number = True
            try: int(instruct)
            except: number = False

            #Random number generation
            if instruct[:6]=="RANDOM": prt1=instruct[6:].split("|")[0];prt2=instruct[6:].split("|")[1];genRandom=random.randint(int(prt1),int(prt2))
        
            
            if number and affectPlayer:
                plyHEAL += int(instruct) #Changes player's health
                if instruct <= 0: print eneGEND[temp].title() + " gave " + str(instruct) + " health to Player!" #Prints out damage
                else: print eneGEND[temp].title() + " dealt " + str(abs(int(instruct))) + " damage to Player!" #Prints out damage

        if plyHEAL < 1: #Checks if alive
            living = False
            print "Player has been defeated by " + eneNAME[temp] + "."
            break
        else: print "Player now has "+str(plyHEAL)+" health!"

    #WIN CHECK=============================
    winCheck = True
    for temp in range(0,len(eneHEAL)):
        if eneHEAL[temp] > 0: winCheck = False
    if winCheck and living: wonGame = True
print "You win!"
raw_input()


