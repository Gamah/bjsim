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

   
players = []
for player in range(0,config.players):
    players.append(utilities.player([],config.bankroll,config.betUnit,0))
        
dealer = utilities.hand(0,[],0,0)
 
 
#play loop
while len(shoe) > config.deckPenetration * 52:
    
    #set up round for dealer and players
    handCount = handCount + 1
 
    for player in players:
        player.hands.append(utilities.hand(player.betUnit,[],0,0))
    
    
   
    
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
        for hand in player.hands: 
            canSplit = 1
            if len(player.hands) == config.maxSplit:
                canSplit = 0
                print("dang")
            decision = strategies.basic(hand.values(),dealer.values(),canSplit)
            while decision != utilities.decisions.stand:
                if decision == utilities.decisions.hit:
                    hand.cards.append(getCard())
                    hand.total = utilities.handTotal(hand.values())
                    decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                elif decision == utilities.decisions.split:
                    newHand = utilities.hand(player.betUnit,[],0,0)
                    newHand.cards.append(hand.cards.pop())
                    player.hands.append(newHand)
                    hand.cards.append(shoe.pop())
                    newHand.cards.append(shoe.pop())
                    hand.total = utilities.handTotal(hand.values())
                    decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                elif decision == utilities.decisions.double:
                    hand.bet = hand.bet + player.betUnit
                    hand.doubled = 1
                    hand.cards.append(getCard())
                    hand.total = utilities.handTotal(hand.values())
                    
                    decision = utilities.decisions.stand
    
    
    
    #Dealer's turn
    #todo: implement H/S 17 
    while utilities.handTotal(dealer.values()) < 17:
        dealer.cards.append(getCard())
        dealer.total = utilities.handTotal(dealer.values())
    
    
    #Determine winners
    for player in players:
        for hand in player.hands:
            #player bust
            if hand.total > 21:
                player.bankroll = player.bankroll - hand.bet
            #player wins or dealer buts
            elif hand.total < 22 and (hand.total > dealer.total or dealer.total > 22):
                player.bankroll = player.bankroll + hand.bet
            #push
            elif hand.total < 22 and hand.total == dealer.total:
                pass
            #dealer beats player
            elif hand.total < 22 and hand.total < dealer.total and dealer.total < 22:
                player.bankroll = player.bankroll - hand.bet
    
    
    ##debug
    if debug == 1:
        print("Dealer   : " , str(dealer.faces()), "Total: " , dealer.total)
        x = 0
        for player in players:
            for hand in player.hands:
                print("Player" , str(x) , ": " , str(hand.faces()), "Total :" , hand.total, " Doubled: " , hand.doubled)
            x = x + 1
            print("Bankroll: " + str(player.bankroll))
        print("")
    
    #Discard the hands
    dealer = utilities.hand(0,[],0,0)
    for player in players:
        player.hands = []
