from pprint import pprint
import random
import strategies
import utilities
import config

debug = 1

handCount = 0
runningCount = 0
trueCount = 0

shoe = utilities.getShoe()

def getCard():
    global runningCount
    card = shoe.pop()
    if card.value > 9:
        runningCount = runningCount - 1
    if card.value < 7:
        runningCount = runningCount + 1
    return card

#play loop
while len(shoe) > config.deckPenetration * 52:
    
    #set up round for dealer and players
    handCount = handCount + 1
    
    players = []
    for player in range(0,config.players):
        players.append(utilities.player([],config.bankroll,config.betUnit,0))
        
    for player in players:
        player.hands.append(utilities.hand([],0,0))
    
    
    dealer = utilities.hand([],0,0)
    
    #Deal cards
    x = 0
    while x < 2:
        
        for player in players:
            player.hands[0].cards.append(getCard())
            player.hands[0].total = utilities.handTotal(player.hands[0].values())
        
        dealer.cards.append(getCard())
        dealer.total = utilities.handTotal(dealer.values())
        
        x = x + 1
    
    #TODO: Implement insurance
    if dealer.values()[1] == 1:
        pass
    
    #Dealer blackjack check
    if utilities.handTotal(dealer.values()) == 21:
        pass
    
    
    #Players turns
    for player in players:
        decision = strategies.basic(player.hands[0].values(),dealer.values())
        while decision != utilities.decisions.stand:
            if decision in (utilities.decisions.hit,utilities.decisions.split):
                player.hands[0].cards.append(getCard())
                player.hands[0].total = utilities.handTotal(player.hands[0].values())
                decision = strategies.basic(player.hands[0].values(),dealer.values())
            elif decision == utilities.decisions.double:
                player.hands[0].doubled = 1
                player.hands[0].cards.append(getCard())
                player.hands[0].total = utilities.handTotal(player.hands[0].values())
                decision = utilities.decisions.stand
    
    
    
    #Dealer's turn
    #todo: implement H/S 17 
    while utilities.handTotal(dealer.values()) < 17:
        dealer.cards.append(getCard())
        dealer.total = utilities.handTotal(dealer.values())
    
    #Determine winners
    
    
    
    ##debug
    if debug == 1:
        print("Dealer   : " , str(dealer.faces()), "Total: " , dealer.total)
        x = 0
        for player in players:
            print("Player" , str(x) , ": " , str(player.hands[0].faces()), "Total :" , player.hands[0].total, " Doubled: " , player.hands[0].doubled)
            x = x + 1
        print("")
    
        