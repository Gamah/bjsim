import random
import strategies
import utilities
import config
import math

debug = 0
numShoes = config.numShoes

#set up dealer and players
players = []
for player in range(0,config.players):
    players.append(utilities.player([],config.bankroll,config.betUnit,0))
        
dealer = utilities.hand(0,[],0,0,0)
totalHands = 0
#set up shoe 
while  numShoes > 0:

    shoe = utilities.shoe()
    shoe.cards = utilities.shuffle()
    trueCount = 0
    if debug == 1:
        print("SHUFFLE!", str(numShoes) , "shoes left!")
    #play loop
    while len(shoe.cards) > config.deckPenetration * 52:
        
        #set up round for dealer and players
        for player in players:
            if trueCount > -1:
                if trueCount == 2:
                    player.betMultiplier = 4
                if trueCount == 3:
                    player.betMultiplier = 10
                if trueCount == 4:
                    player.betMultiplier = 20
                if trueCount > 4:
                    player.betMultiplier = 40
                else:
                    player.betMultiplier = 1
                player.hands.append(utilities.hand((player.betUnit * player.betMultiplier),[],0,0,0))
            
        
        #Deal cards
        x = 0
        while x < 2:
            for player in players:
                for hand in player.hands:
                    hand.cards.append(shoe.getCard())
                    hand.total = utilities.handTotal(hand.values())
            
            dealer.cards.append(shoe.getCard())
            dealer.total = utilities.handTotal(dealer.values())
            x = x + 1
        
        #TODO: Implement insurance
        if dealer.values()[1] == 1:
            #TODO: take insurance when TC is implemented.
            if utilities.handTotal(dealer.values()) == 21 and len(dealer.cards) == 2:
                if debug == 1:
                    print("Dealer BJ")
                for player in players:
                    for hand in player.hands:
                        if not(utilities.handTotal(hand.values()) == 21 and len(hand.cards) == 2 and hand.split == 0):
                            player.bankroll = player.bankroll - hand.bet
                        else:
                            if debug == 1:
                                print("Player " , players.index(player), " BJ Push!")
        if utilities.handTotal(dealer.values()) == 21 and len(dealer.cards) == 2:
            if debug == 1:
                print("Dealer backdoor BJ")
            for player in players:
                for hand in player.hands:
                    if not(utilities.handTotal(hand.values()) == 21 and len(hand.cards) == 2 and hand.split == 0):
                        player.bankroll = player.bankroll - hand.bet
                    else:
                        if debug == 1:
                            print("Player " , players.index(player), " BJ Push!")
        else:
            #Players turns
            for player in players:
                for hand in player.hands: 
                    canSplit = 1
                    if len(player.hands) == config.maxSplit:
                        canSplit = 0
                    if len(player.hands) == 2 and hand.cards[0] == 1:
                        canSplit = 0
                    decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                    while decision != utilities.decisions.stand:
                        if decision == utilities.decisions.hit:
                            hand.cards.append(shoe.getCard())
                            hand.total = utilities.handTotal(hand.values())
                            decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                        elif decision == utilities.decisions.split:
                            newHand = utilities.hand(player.betUnit * player.betMultiplier,[],0,0,1)
                            newHand.cards.append(hand.cards.pop())
                            player.hands.append(newHand)
                            hand.cards.append(shoe.getCard())
                            hand.split = 1
                            newHand.cards.append(shoe.getCard())
                            newHand.total = utilities.handTotal(newHand.values())
                            hand.total = utilities.handTotal(hand.values())
                            if hand.cards[0] == 1:
                                decision = utilities.decision.stand
                            else:
                                decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                        elif decision == utilities.decisions.double:
                            hand.bet = hand.bet + player.betUnit
                            hand.doubled = 1
                            hand.cards.append(shoe.getCard())
                            hand.total = utilities.handTotal(hand.values())
                            decision = utilities.decisions.stand
        
        
            #Dealer's turn
            #todo: implement H/S 17 
            dealerPlays = 0
            for player in players:
                    if len(player.hands) > 0:
                            dealerPlays = 1
            if dealerPlays == 1:
                while utilities.handTotal(dealer.values()) < 17:
                    dealer.cards.append(shoe.getCard())
                    dealer.total = utilities.handTotal(dealer.values())


            #Determine winners
            for player in players:
                for hand in player.hands:
                    #player BJ
                    if hand.total == 21 and dealer.total != 21:
                        player.bankroll = player.bankroll + hand.bet * 1.5
                    #player bust
                    elif hand.total > 21:
                        player.bankroll = player.bankroll - hand.bet
                    #player wins or dealer busts
                    elif hand.total < 22 and (hand.total > dealer.total or dealer.total > 21):
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
                    print("Player" , str(x) , ": " , str(hand.faces()),"Bet: ", hand.bet, "Total :" , hand.total, " Doubled: " , hand.doubled)
                x = x + 1
                print("Player ", players.index(player) , "Bankroll: " + str(player.bankroll))
            print("Running Count: ", str(shoe.runningCount))
            print("Card Remaining: ", str(len(shoe.cards)))
            print("True Count: ", str(trueCount))
            print("Hand Count: ", str(shoe.handCount))
            print("")

        #Discard the hands
        dealer = utilities.hand(0,[],0,0,0)
        for player in players:
            player.hands = []
        shoe.handCount = shoe.handCount + 1
        totalHands = totalHands + 1

        #calculate TC
        trueCount = math.floor(shoe.runningCount / int((len(shoe.cards) / 52 ) + 1))
        
    
    #end of shoe, clear the cards, reset it's params.
    shoe.cards = []
    shoe.runningCount = 0
    shoe.handCount = 0
    numShoes = numShoes - 1
print("Profit per shoe\r\n")
for player in players:
    x = x + 1
    print("Player ", players.index(player) , ": " + str(player.bankroll/config.numShoes))
    print("Total hands: " , totalHands)
