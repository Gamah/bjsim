import random
import strategies
import utilities

debug = 1

#set up player
bankroll = 5000
betUnit = 5
betMultiplier = 0
handCount = 0
runningCount = 0
trueCount = 0

shoe = utilities.getShoe()



 
    
#play loop
while len(shoe) > 78:
    handCount = handCount + 1
    
    dealerFaces = []
    dealerValues = []
    playerFaces = []
    playerValues = []
    
    x = 0
    while x < 2:
        currentCard = shoe.pop()
        dealerFaces.append(currentCard.face)
        dealerValues.append(currentCard.value)
        ##TODO: can't see the down card yet...
        runningCount = utilities.adjustCount(currentCard.value,runningCount)
        
        ##todo: multiple players
        currentCard = shoe.pop()
        playerFaces.append(currentCard.face)
        playerValues.append(currentCard.value)
        runningCount = utilities.adjustCount(currentCard.value,runningCount)
        
        
        x = x +1
    
    #TODO:implement blackjacks
    
    
    #Player's turn
    ##TODO: implement splitting
    while strategies.basic(playerValues,dealerValues) != utilities.decisions.stand and utilities.handTotal(playerValues) < 21:
        currentCard = shoe.pop()
        playerFaces.append(currentCard.face)
        playerValues.append(currentCard.value)
        
        runningCount = adjustCount(currentCard.value,runningCount)
    
    
    ##todo: implement H/S 17 
    while utilities.handTotal(dealerValues) < 17 and utilities.handTotal(playerValues) < 22:
        currentCard = shoe.pop()
        dealerFaces.append(currentCard.face)
        dealerValues.append(currentCard.value)
        runningCount = adjustCount(currentCard.value,runningCount)
    
    #Determine winners
    if utilities.handTotal(playerValues) > 21:
        if debug == 1:
            print("Player bust")
        bankroll = bankroll - betUnit
    elif utilities.handTotal(dealerValues) > 21 and utilities.handTotal(playerValues) < 22:
        if debug == 1:
            print("Dealer Bust!")
        bankroll = bankroll + betUnit
    elif utilities.handTotal(dealerValues) > utilities.handTotal(playerValues):
        if debug == 1:
            print("Dealer wins")
        bankroll = bankroll - betUnit
    elif utilities.handTotal(playerValues) > utilities.handTotal(dealerValues):
        if debug == 1:
            print("Player wins!")
        bankroll = bankroll + betUnit
    elif utilities.handTotal(playerValues) == utilities.handTotal(dealerValues):
        if debug == 1:
            print("Hand push")
        bankroll = bankroll + betUnit
    
    
    ##debug
    if debug == 1:
        print(playerFaces, "Player: " + str(utilities.handTotal(playerValues)))
        print(dealerFaces, "Dealer: " + str(utilities.handTotal(dealerValues)))
        print("Hands played: " + str(handCount))
        print("RunningCount: " + str(runningCount))
        print("BankRoll: " + str(bankroll))
        print("Cards remaining: " + str(len(shoe)))
        print("")
