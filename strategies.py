import utilities 
def basic(playerHand,dealerHand,canSplit):
    
    upCard = dealerHand.values()[1]
    playerValues = playerHand.values()
    
    #Always split Aces & 8's
    if len(playerValues) == 2 and (playerValues[0] == 1 and playerValues[1] == 1):
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            return(utilities.decisions.hit)
            
    if len(playerValues) == 2 and (playerValues[0] == 8 and playerValues[1] == 8):
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            if upCard in (2,3,4,5,6):
                return(utilities.decisions.stand) 
            if upCard in (7,8,9,10,1):
                return(utilities.decisions.hit)
        
    
    #Never Split 10's and 5's 
    #(no code here, just copying all of Colin's rules)
           
    #Split 2, 3 & 7 on 2 through 7
    if len(playerValues) == 2 and ((playerValues[0] == 2 and playerValues[1] == 2) or (playerValues[0] == 3 and playerValues[1] == 3)) and upCard in (2,3,4,5,6,7):
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            return(utilities.decisions.hit)
    
    if len(playerValues) == 2 and (playerValues[0] == 7 and playerValues[1] == 7) and upCard in (2,3,4,5,6,7):
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            if upCard in (2,3,4,5,6):
                return(utilities.decisions.stand) 
            if upCard in (7,8,9,10,1):
                return(utilities.decisions.hit)

    
    #Split 4's against 5 & 6
    if len(playerValues) == 2 and (playerValues[0] == 4 and playerValues[1] == 4) and upCard in [5,6]:
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            return(utilities.decisions.hit)
    
    #Split 6's on 2 through 6
    if len(playerValues) == 2 and (playerValues[0] == 6 and playerValues[1] == 6 and upCard in (2,3,4,5,6)):
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            if upCard in (2,3,4,5,6):
                return(utilities.decisions.stand) 
            if upCard in (7,8,9,10,1):
                return(utilities.decisions.hit)
    
    #Split 9's against 2 through 9 except 7
    if len(playerValues) == 2 and (playerValues[0] == 9 and playerValues[1] == 9 and upCard in (2,3,4,5,6,7,8,9) and upCard != 7):
        if canSplit == 1:
            return(utilities.decisions.split)
        else:
            return(utilities.decisions.stand)
    
    #Soft 21 and 20 always stand:
    if playerHand.isSoft == 1 and playerHand.total in [20,21]:
        return(utilities.decisions.stand)
     
    #Soft 19 doubles against 6 otherwise it stands
    if playerHand.isSoft == 1 and playerHand.total == 19:
        if upCard == 6:
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.stand)
        else:
            return(utilities.decisions.stand)
    #Soft 18 doubles against 2-6, stands against 7 and 8, hits against 9,10, Ace. If it can't double against 2-6 it stands, it stands.
    if playerHand.isSoft == 1 and playerHand.total == 18:
        if upCard in (2,3,4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:  
                return(utilities.decisions.stand)
        if upCard in (7,8):
            return(utilities.decisions.stand)
        if upCard in (9,10,1):
            return(utilities.decisions.hit)
            
    #Soft 17 doubles against 3-6, otherwise it hits
    if playerHand.isSoft == 1 and playerHand.total == 17:
        if upCard in (3,4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)    
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
    #Soft 16 and Soft 15 doubles against 4 through 6 otherwise it hits
    if playerHand.isSoft == 1 and playerHand.total in (16,15):
        if upCard in (4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
            
    #Soft 14 and soft 13 doubles against 5 and 6 otherwise it hits
    if playerHand.isSoft == 1 and playerHand.total in (14,13):
        if upCard in (5,6):
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
    if playerHand.isSoft == 0 and playerHand.total >= 17:
        return(utilities.decisions.stand)
    
    #Hard 13 through 16 will stand against 2-6, hit against 7-ace
    if playerHand.isSoft == 0 and playerHand.total in (13,14,15,16):
        if upCard in (2,3,4,5,6):
            return(utilities.decisions.stand) 
        if upCard in (7,8,9,10,1):
            return(utilities.decisions.hit)
            
    #Hard 12 will stand against 4-6, hit aganist everything else
    if playerHand.isSoft == 0 and playerHand.total == 12:
        if upCard in (4,5,6):
            return(utilities.decisions.stand)
        else:
            return(utilities.decisions.hit)
            
    #Hard 11 will always double
    if playerHand.isSoft == 0 and playerHand.total == 11:
        if len(playerValues) == 2:
            return(utilities.decisions.double)
        else:
            return(utilities.decisions.hit)
            
    #Hard 10 will double against 2-9
    if playerHand.isSoft == 0 and playerHand.total == 10:
        if upCard in (2,3,4,5,6,7,8,9):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
            
    #Hard 9 will double against 3-6
    if playerHand.isSoft == 0 and playerHand.total == 9:
        if upCard in (3,4,5,6):
            if len(playerValues) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.hit)
        else:
            return(utilities.decisions.hit)
        
    #Hard 8 and below will always hit
    if playerHand.isSoft == 0 and playerHand.total < 9:
        return(utilities.decisions.hit)
