import random
import strategies
import utilities
import config
import math
import argparse


parser = argparse.ArgumentParser(description='Simulate some blackjack.')
parser.add_argument('--debug', metavar='N', type=int, help='Print hand results',default=0)
args = parser.parse_args()

debug = args.debug

numShoes = config.numShoes

#set up dealer and players
players = []
for player in range(0,config.players):
    players.append(utilities.player([],config.bankroll,config.betUnit,0,player%2))
        
dealer = utilities.hand(0,[],0,0,0,0)

#set up shoe 
for shoe in range(numShoes):

    print("\r",str(numShoes), "shoes remain... ",end='')

    shoe = utilities.shoe()
    shoe.cards = utilities.shuffle()
    trueCount = 0
    if debug == 1:
        print("SHUFFLE!", str(numShoes) , "shoes left!")
    #play loop
    while len(shoe.cards) > config.deckPenetration * 52:
        
        #set up round for dealer and players
        for player in players:
            if trueCount > -2:
                if trueCount in (2,3,4,5):
                    player.betMultiplier = math.floor(trueCount * 4)
                    player.hands.append(utilities.hand((player.betUnit * player.betMultiplier),[],0,0,0,0))
                if trueCount > 5:
                    player.betMultiplier = 20
                    player.hands.append(utilities.hand((player.betUnit * player.betMultiplier),[],0,0,0,0))
                else:
                    player.betMultiplier = 1
                player.hands.append(utilities.hand((player.betUnit * player.betMultiplier),[],0,0,0,0))
            
        
        #Deal cards
        x = 0
        while x < 2:
            for player in players:
                for hand in player.hands:
                    hand.addCard(shoe.getCard())
            
            dealer.addCard(shoe.getCard())
            x = x + 1
        
        #TODO: Implement insurance
        if dealer.values()[1] == 1:
            #TODO: take insurance when TC is implemented.
            if dealer.total == 21 and len(dealer.cards) == 2:
                if debug == 1:
                    print("Dealer BJ")
                for player in players:
                    for hand in player.hands:
                        if not(hand.total == 21 and len(hand.cards) == 2 and hand.split == 0):
                            player.bankroll = player.bankroll - hand.bet
                        else:
                            if debug == 1:
                                print("Player " , players.index(player), " BJ Push!")
        if dealer.total == 21 and len(dealer.cards) == 2:
            if debug == 1:
                print("Dealer backdoor BJ")
            for player in players:
                for hand in player.hands:
                    if not(hand.total == 21 and len(hand.cards) == 2 and hand.split == 0):
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
                    if len(player.hands) == 2 and hand.cards[0] == 1 and config.rules.RSA != 1 and hand.split == 1:
                        canSplit = 0

                    canDouble = 1
                    #if hand is split and nDAS or first card is ace, no doubling...
                    #can only double 2 cards
                    if ((hand.split == 1 and (config.rules.DAS != 1 or hand.values()[0] == 1)) or len(hand.cards) != 2):
                        canDouble = 0
                    decision = strategies.play(hand,dealer,canSplit,canDouble,trueCount).do(player.strategy)
                    while decision != utilities.decisions.stand:
                        if decision == utilities.decisions.hit:
                            #can't hit split aces...
                            if hand.split == 1 and hand.values()[0] == 1:
                                decision = utilities.decisions.stand
                            else:
                                hand.addCard(shoe.getCard())
                                decision = strategies.play(hand,dealer,canSplit,canDouble,trueCount).do(player.strategy)
                        elif decision == utilities.decisions.split:
                            newHand = utilities.hand(player.betUnit * player.betMultiplier,[],0,0,1,0)
                            newHand.addCard(hand.cards.pop())
                            player.hands.append(newHand)
                            hand.addCard(shoe.getCard())
                            hand.split = 1
                            newHand.addCard(shoe.getCard())
                            if hand.values()[0] == 1:
                                canDouble = 0
                            if hand.values()[1] == 1 and hand.values()[0] == 1:
                                if config.rules.RSA != 1 or len(player.hands) == config.maxSplit:
                                    decision = utilities.decisions.stand
                                else:
                                    decision = utilities.decisions.split
                            else:
                                decision = strategies.play(hand,dealer,canSplit,canDouble,trueCount).do(player.strategy)
                        elif decision == utilities.decisions.double:
                            hand.bet = hand.bet + player.betUnit
                            hand.doubled = 1
                            hand.addCard(shoe.getCard())
                            decision = utilities.decisions.stand
        
        
            #Dealer's turn
            #todo: implement H/S 17 
            dealerPlays = 0
            for player in players:
                    if len(player.hands) > 0:
                            dealerPlays = 1
            if dealerPlays == 1:
                while dealer.total < 17 or (dealer.total == 17 and dealer.isSoft == 1 and config.rules.H17 == 1):
                    dealer.addCard(shoe.getCard())

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
        dealer = utilities.hand(0,[],0,0,0,0)
        for player in players:
            player.hands = []
        shoe.handCount = shoe.handCount + 1

        #calculate TC
        #TODO: floor isn't necessarily ideal, allow picking floor, round, truncate
        trueCount = math.floor(shoe.runningCount / (len(shoe.cards) / float(52) ))

    
    #end of shoe, clear the cards, reset it's params.
    shoe.cards = []
    shoe.runningCount = 0
    shoe.handCount = 0
    numShoes = numShoes - 1

print("\r\n")
for player in players:
    x = x + 1
    print("Player ", players.index(player) , "Bankroll: " + str(player.bankroll))