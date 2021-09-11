import utilities 

class play():
    
    def __init__(self,playerHand,dealerHand,canSplit,trueCount):
        self.playerHand = playerHand
        self.dealerHand = dealerHand
        self.canSplit = canSplit
        self.trueCount = trueCount

    def upCard(self):
        return self.dealerHand.values()[1]

    def playerValues(self):
        return self.playerHand.values()
    
    def basic(self):
    
        #Always split Aces & 8's
        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 1 and self.playerValues()[1] == 1):
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                return(utilities.decisions.hit)

        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 8 and self.playerValues()[1] == 8):
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                if self.upCard() in (2,3,4,5,6):
                    return(utilities.decisions.stand) 
                if self.upCard() in (7,8,9,10,1):
                    return(utilities.decisions.hit)


        #Never Split 10's and 5's 
        #(no code here, just copying all of Colin's rules)

        #Split 2, 3 & 7 on 2 through 7
        if len(self.playerValues()) == 2 and ((self.playerValues()[0] == 2 and self.playerValues()[1] == 2) or (self.playerValues()[0] == 3 and self.playerValues()[1] == 3)) and self.upCard() in (2,3,4,5,6,7):
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                return(utilities.decisions.hit)

        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 7 and self.playerValues()[1] == 7) and self.upCard() in (2,3,4,5,6,7):
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                if self.upCard() in (2,3,4,5,6):
                    return(utilities.decisions.stand) 
                if self.upCard() in (7,8,9,10,1):
                    return(utilities.decisions.hit)


        #Split 4's against 5 & 6
        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 4 and self.playerValues()[1] == 4) and self.upCard() in [5,6]:
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                return(utilities.decisions.hit)

        #Split 6's on 2 through 6
        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 6 and self.playerValues()[1] == 6 and self.upCard() in (2,3,4,5,6)):
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                if self.upCard() in (2,3,4,5,6):
                    return(utilities.decisions.stand) 
                if self.upCard() in (7,8,9,10,1):
                    return(utilities.decisions.hit)

        #Split 9's against 2 through 9 except 7
        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 9 and self.playerValues()[1] == 9 and self.upCard() in (2,3,4,5,6,7,8,9) and self.upCard() != 7):
            if self.canSplit == 1:
                return(utilities.decisions.split)
            else:
                return(utilities.decisions.stand)

        #Soft 21 and 20 always stand:
        if self.playerHand.isSoft == 1 and self.playerHand.total in [20,21]:
            return(utilities.decisions.stand)

        #Soft 19 doubles against 6 otherwise it stands
        if self.playerHand.isSoft == 1 and self.playerHand.total == 19:
            if self.upCard() == 6:
                if len(self.playerValues()) == 2:
                    return(utilities.decisions.double)
                else:
                    return(utilities.decisions.stand)
            else:
                return(utilities.decisions.stand)
        #Soft 18 doubles against 2-6, stands against 7 and 8, hits against 9,10, Ace. If it can't double against 2-6 it stands, it stands.
        if self.playerHand.isSoft == 1 and self.playerHand.total == 18:
            if self.upCard() in (2,3,4,5,6):
                if len(self.playerValues()) == 2:
                    return(utilities.decisions.double)
                else:  
                    return(utilities.decisions.stand)
            if self.upCard() in (7,8):
                return(utilities.decisions.stand)
            if self.upCard() in (9,10,1):
                return(utilities.decisions.hit)

        #Soft 17 doubles against 3-6, otherwise it hits
        if self.playerHand.isSoft == 1 and self.playerHand.total == 17:
            if self.upCard() in (3,4,5,6):
                if len(self.playerValues()) == 2:
                    return(utilities.decisions.double)    
                else:
                    return(utilities.decisions.hit)
            else:
                return(utilities.decisions.hit)
        #Soft 16 and Soft 15 doubles against 4 through 6 otherwise it hits
        if self.playerHand.isSoft == 1 and self.playerHand.total in (16,15):
            if self.upCard() in (4,5,6):
                if len(self.playerValues()) == 2:
                    return(utilities.decisions.double)
                else:
                    return(utilities.decisions.hit)
            else:
                return(utilities.decisions.hit)

        #Soft 14 and soft 13 doubles against 5 and 6 otherwise it hits
        if self.playerHand.isSoft == 1 and self.playerHand.total in (14,13):
            if self.upCard() in (5,6):
                if len(self.playerValues()) == 2:
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
        if self.playerHand.isSoft == 0 and self.playerHand.total >= 17:
            return(utilities.decisions.stand)

        #Hard 13 through 16 will stand against 2-6, hit against 7-ace
        if self.playerHand.isSoft == 0 and self.playerHand.total in (13,14,15,16):
            if self.upCard() in (2,3,4,5,6):
                return(utilities.decisions.stand) 
            if self.upCard() in (7,8,9,10,1):
                return(utilities.decisions.hit)

        #Hard 12 will stand against 4-6, hit aganist everything else
        if self.playerHand.isSoft == 0 and self.playerHand.total == 12:
            if self.upCard() in (4,5,6):
                return(utilities.decisions.stand)
            else:
                return(utilities.decisions.hit)

        #Hard 11 will always double
        if self.playerHand.isSoft == 0 and self.playerHand.total == 11:
            if len(self.playerValues()) == 2:
                return(utilities.decisions.double)
            else:
                return(utilities.decisions.hit)

        #Hard 10 will double against 2-9
        if self.playerHand.isSoft == 0 and self.playerHand.total == 10:
            if self.upCard() in (2,3,4,5,6,7,8,9):
                if len(self.playerValues()) == 2:
                    return(utilities.decisions.double)
                else:
                    return(utilities.decisions.hit)
            else:
                return(utilities.decisions.hit)

        #Hard 9 will double against 3-6
        if self.playerHand.isSoft == 0 and self.playerHand.total == 9:
            if self.upCard() in (3,4,5,6):
                if len(self.playerValues()) == 2:
                    return(utilities.decisions.double)
                else:
                    return(utilities.decisions.hit)
            else:
                return(utilities.decisions.hit)

        #Hard 8 and below will always hit
        if self.playerHand.isSoft == 0 and self.playerHand.total < 9:
            return(utilities.decisions.hit)
    


    def S17Dev(self):
        #split 10's on dealer six for truecount 4, dealer 5 for truecount 5, dealer 4 for truecount 6
        if len(self.playerValues()) == 2 and (self.playerValues()[0] == 10 and self.playerValues()[1] == 10):
            if self.canSplit == 1:
                if self.upCard == 6 and self.trueCount >= 4:
                    return(utilities.decisions.split)
                if self.upCard == 5 and self.trueCount >= 5:
                    return(utilities.decisions.split)
                if self.upCard == 4 and self.trueCount >= 6:
                    return(utilities.decisions.split)
            else:
                return(self.basic())

        #TODO: implement DAS rule

        #double soft 19 on dealer 5 and 6 for truecount 1, dealer 4 for truecount 3
        if self.playerHand.isSoft == 1 and self.playerHand.total == 19:
            if self.upCard in(5,6) and self.trueCount >= 1:
                return(utilities.decisions.double)
            if self.upCard == 4 and self.trueCount >= 3:
                return(utilities.decisions.double)
            else:
                return(self.basic())
        
        #stand hard 16 on any positive run
        # ning count against a 10, dealer 9 for truecount 4
        if self.playerHand.isSoft == 0 and self.playerHand.total == 16:
            if self.trueCount >= 0 and self.upCard() == 10:
                return(utilities.decisions.stand)
            if self.trueCount >= 4 and self.upCard() == 9:
                return(utilities.decisions.stand)
            else:
                return(self.basic())

        #stand hard 15 on dealer 10 for for truecount 4
        if self.playerHand.isSoft == 0 and self.playerHand.total == 15:
            if self.trueCount >= 4 and self.upCard() == 10:
                return(utilities.decisions.stand)
            else:
                return(self.basic())

        #stand hard 13 on dealer 2 for for truecount -1
        if self.playerHand.isSoft == 0 and self.playerHand.total == 13:
            if self.trueCount <= -1 and self.upCard() == 2:
                return(utilities.decisions.stand)
            else:
                return(self.basic())

        #stand hard 12 on dealer 2 for for truecount 3, dealer 3 for truecount 2, dealer 4 for any negative count
        if self.playerHand.isSoft == 0 and self.playerHand.total == 12:
            if self.trueCount >= 3 and self.upCard() == 2:
                return(utilities.decisions.stand)
            if self.trueCount >= 2 and self.upCard() == 3:
                return(utilities.decisions.stand)
            if self.trueCount <= -1 and self.upCard() == 4:
                return(utilities.decisions.stand)
            else:
                return(self.basic())

        #hit 11 on dealer ace for truecount 1
        if self.playerHand.total == 11:
            if self.trueCount >= 1 and self.upCard() == 1:
                return(utilities.decisions.hit)
            else:
                return(self.basic())

        #hit 10 on dealer ace and 10 for truecount 4
        if self.playerHand.total == 10:
            if self.trueCount >= 4 and self.upCard() == 1:
                return(utilities.decisions.hit)
            else:
                return(self.basic())

        #double 9 on dealer 2 for truecount 1, and dealer 7 for truecount 3
        if self.playerHand.total == 9:
            if self.trueCount >= 1 and self.upCard() == 2:
                return(utilities.decisions.double)
            if self.trueCount >= 3 and self.upCard() == 7:
                return(utilities.decisions.double)
            else:
                return(self.basic())
        
        #double 8 on dealer 6 for truecount 2
        if self.playerHand.total == 8:
            if self.trueCount >= 2 and self.upCard() == 6:
                return(utilities.decisions.double)
            else:
                return(self.basic())

        return(self.basic())