import random
import strategies
import utilities
import config

debug = 1
numShoes = config.numShoes

#set up dealer and players
players = []
for player in range(0,config.players):
    players.append(utilities.player([],config.bankroll,config.betUnit,0))
        
dealer = utilities.hand(0,[],0,0,0)

#set up shoe 
while  numShoes > 0:

    shoe = utilities.shoe()
    shoe.cards = utilities.shuffle()
    print("SHUFFLE!", str(numShoes) , "shoes left!")
    #play loop
    while len(shoe.cards) > config.deckPenetration * 52:
        #set up round for dealer and players
        for player in players:
            player.hands.append(utilities.hand(player.betUnit,[],0,0,0))
        
        #Deal cards
        x = 0
        while x < 2:
            for player in players:
                player.hands[0].cards.append(shoe.getCard())
                player.hands[0].total = utilities.handTotal(player.hands[0].values())
            
            dealer.cards.append(shoe.getCard())
            dealer.total = utilities.handTotal(dealer.values())
            x = x + 1
        
        #TODO: Implement insurance
        if dealer.values()[1] == 1:
            #TODO: take insurance when TC is implemented.
            if utilities.handTotal(dealer.values()) == 21 and len(dealer.cards) == 2:
                print("Dealer BJ")
                for player in players:
                    for hand in player.hands:
                        if not(utilities.handTotal(hand.values()) == 21 and len(hand.cards) == 2 and hand.split == 0):
                            player.bankroll = player.bankroll - player.betUnit
                        else:
                            print("Player " , players.index(player), " BJ Push!")
                    player.hands = []
                dealer = utilities.hand(0,[],0,0,0)
        elif utilities.handTotal(dealer.values()) == 21 and len(dealer.cards) == 2:
            print("Dealer backdoor BJ")
            for player in players:
                for hand in player.hands:
                    if not(utilities.handTotal(hand.values()) == 21 and len(hand.cards) == 2 and hand.split == 0):
                        player.bankroll = player.bankroll - player.betUnit
                    else:
                        print("Player " , players.index(player), " BJ Push!")
                player.hands = []
            dealer = utilities.hand(0,[],0,0,0)
        else:
            #Players turns
            for player in players:
                for hand in player.hands: 
                    canSplit = 1
                    if len(player.hands) == config.maxSplit:
                        canSplit = 0
                    if len(player.hands) == 2 and hand.cards[0] == 1:
                        canSplit = 0
                    if utilities.handTotal(hand.values()) == 21 and len(hand.cards) == 2 and hand.split == 0:
                            player.bankroll = player.bankroll + (player.betUnit * 1.5)
                            player.hands.remove(hand)
                    decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                    while decision != utilities.decisions.stand:
                        if decision == utilities.decisions.hit:
                            hand.cards.append(shoe.getCard())
                            hand.total = utilities.handTotal(hand.values())
                            decision = strategies.basic(hand.values(),dealer.values(),canSplit)
                        elif decision == utilities.decisions.split:
                            newHand = utilities.hand(player.betUnit,[],0,0,1)
                            newHand.cards.append(hand.cards.pop())
                            player.hands.append(newHand)
                            hand.cards.append(shoe.getCard())
                            hand.split = 1
                            newHand.cards.append(shoe.getCard())
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
            else:
                dealer = utilities.hand(0,[],0,0,0)
                
            #Determine winners
            for player in players:
                for hand in player.hands:
                    #player bust
                    if hand.total > 21:
                        player.bankroll = player.bankroll - hand.bet
                    #player wins or dealer buts
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
                    print("Player" , str(x) , ": " , str(hand.faces()), "Total :" , hand.total, " Doubled: " , hand.doubled)
                x = x + 1
                print("Playser ", players.index(player) , "Bankroll: " + str(player.bankroll))
            
        #Discard the hands
        dealer = utilities.hand(0,[],0,0,0)
        for player in players:
            player.hands = []
        shoe.handCount = shoe.handCount + 1
        print("Running Count: ", str(shoe.runningCount))
        print("Hand Count: ", str(shoe.handCount))
        print("")
        
    shoe.cards = []
    shoe.runningCount = 0
    shoe.handCount = 0
    numShoes = numShoes - 1