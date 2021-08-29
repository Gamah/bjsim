import utilities 
def basic(playerValues,dealerValues):
    
    softHand = 0
    dealerUpCard = dealerValues[1]
    
    if (1 in playerValues and utilities.handTotal(playerValues) < 17) or (1 in playerValues and len(playerValues) == 2):
        softHand = 1
        
    #Always split Aces & 8's
    if len(playerValues) == 2 and ((playerValues[0] == 8 and playerValues[1] == 8) or (playerValues[0] == 1 and playerValues[1] == 1)):
        return("S")
    
    #Never Split 10's and 5's 
    #(no code here, just copying all of Colin's rules)
   
    #Split 2, 3 & 7 on 2 through 7
    if len(playerValues) == 2 and ((playerValues[0] == 2 and playerValues[1] == 2) or (playerValues[0] == 3 and playerValues[1] == 3) or (playerValues[0] == 7 and playerValues[1] == 7)) and dealerUpCard in (2,3,4,5,6,7):
        return(utilities.decisions.split)
    
    #Split 4's against 5 & 6
    if len(playerValues) == 2 and (playerValues[0] == 4 and playerValues[1] == 4) and dealerUpCard in [5,6]:
        return(utilities.decisions.split)
    
    #Split 6's on 2 through 6
    if len(playerValues) == 2 and (playerValues[0] == 6 and playerValues[1] == 6 and dealerUpCard in (2,3,4,5,6)):
        return(utilities.decisions.split)
    
    #Split 9's against 2 through 9 except 7
    if len(playerValues) == 2 and (playerValues[0] == 9 and playerValues[1] == 9 and dealerValues[1] in (2,3,4,5,6,7,8,9) and dealerValues[1] != 7):
        return(utilities.decisions.split)
    
    #Soft 21 and 20 always stand:
    if softHand == 1 and utilities.handTotal(playerValues) in [20,21]:
        return(utilities.decisions.stand)
     
    #Soft 19 doubles against 6 otherwise it stands
    if softHand == 1 and utilities.handTotal(playerValues) == 19:
        if dealerValues[1] == 6:
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.stand)
        else:
            return(utilities.decisions.stand)
    #Soft 18 doubles against 2-6, stands against 7 and 8, hits against 9,10, Ace. If it can't double against 2-6 it stands, it stands.
    if softHand == 1 and utilities.handTotal(playerValues) == 18:
        if dealerValues[1] in (2,3,4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:  
                return(utilities.decisions.stand)
        if dealerValues[1] in (7,8):
            return(utilities.decisions.stand)
        if dealerValues[1] in (9,10,1):
            return(utilities.decisions.hit)
            
    #Soft 17 doubles against 3-6, otherwise it hits
    if softHand == 1 and utilities.handTotal(playerValues) == 17:
        if dealerValues[1] in (3,4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)    
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
    #Soft 16 and Soft 15 doubles against 4 through 6 otherwise it hits
    if softHand == 1 and utilities.handTotal(playerValues) in (16,15):
        if dealerValues[1] in (4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
            
    #Soft 14 and soft 13 doubles against 5 and 6 otherwise it hits
    if softHand == 1 and utilities.handTotal(playerValues) in (14,13):
        if dealerValues[1] in (5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
            
    #Surrender 16 against 9 - Ace
    #TODO: Add surrender
    
    #Surrender 15 against a 10
    #TODO: Add surrender
    
    #Hard 17 and above will always stand
    if softHand == 0 and utilities.handTotal(playerValues) >= 17:
        return(utilities.decisions.stand)
    
    #Hard 13 through 16 will stand against 2-6, hit against 7-ace
    if softHand == 0 and utilities.handTotal(playerValues) in (13,14,15,16):
        if dealerValues[1] in (2,3,4,5,6):
            return(utilities.decisions.stand) 
        if dealerValues[1] in (7,8,9,10,1):
            return(utilities.decisions.hit)
            
    #Hard 12 will stand against 4-6, hit aganist everything else
    if softHand == 0 and utilities.handTotal(playerValues) == 12:
        if dealerValues[1] in (4,5,6):
            return(utilities.decisions.stand)
        else:
            return(utilities.decisions.hit)
            
    #Hard 11 will always double
    if softHand == 0 and utilities.handTotal(playerValues) == 11:
        if len(playerValues) == 2:
            return(utilities.decisions.double)
        else:
            return(utilities.decisions.hit)
            
    #Hard 10 will double against 2-9
    if softHand == 0 and utilities.handTotal(playerValues) == 10:
        if dealerValues[1] in (2,3,4,5,6,7,8,9):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
        else:
            return(utilities.decisions.hit)
            
    #Hard 9 will double against 3-6
    if softHand == 0 and utilities.handTotal(playerValues) == 9:
        if dealerValues[1] in (3,4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
        else:
            return(utilities.decisions.hit)
    #Hard 8 and below will always hit
    if softHand == 0 and utilities.handTotal(playerValues) < 9:
        return(utilities.decisions.hit)

def dealer(dealerValues):
    
    softHand = 0
    
    if len(dealerValues) == 2 and 1 in dealerValues:
        softHand = 1