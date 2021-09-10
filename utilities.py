import random
import config

#card values
suits = ["D","S","H","C"]
faces = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
values = [1,2,3,4,5,6,7,8,9,10,10,10,10]
#faces = ["K","A"]
#values = [10,1]

#build shoe

class shoe:
    cards = []
    runningCount = 0
    handCount = 0
        
    def __inint__(self,cards,runningCount,handCount):
        self.cards = cards
        self.runningCount = runningCount
        self.handCount = handCount

    def getCard(self):
        card = self.cards.pop()
        if card.value in (10,1):
            self.runningCount = self.runningCount - 1
        if card.value in (2,3,4,5,6):
            self.runningCount = self.runningCount + 1
        return card


class hand:
    bet = 0
    cards = []
    total = 0
    doubled = 0
    split = 0
    isSoft = 0
    
    def __init__(self,bet,cards,total,doubled,split,isSoft):
        self.bet = bet
        self.cards = cards
        self.total = total
        self.doubled = doubled
        self.split = split
        self.isSoft = isSoft
    
    def faces(self):
        faces = []
        for card in self.cards:  
            faces.append(card.face)
        return faces
        
    def values(self):
        values = []
        for card in self.cards:
            values.append(card.value)
        return values

    def handTotal(self):
        if len(self.cards) == 2 and 10 in self.values() and 1 in self.values():
            self.total = 21
        total = sum(self.values())
        if 1 in self.values() and total < 12:
            total = total + 10
            self.isSoft = 1
        else:
            self.isSoft = 0
        self.total = total

    def addCard(self,card):
        self.cards.append(card)
        self.handTotal()
        

class player:
    #set up player
    bankroll = config.bankroll
    betUnit = config.betUnit
    #TODO: implement bet spreads
    betMultiplier = 0
    
    hands = []
    
    def __init__(self,hands,bankroll,betUnit,betMultiplier):
        self.hands = hands
        self.bankroll = bankroll
        self.betUnit = betUnit
        self.betMultiplier = betMultiplier

#define a card
class card:
    def __init__(self,deck,suit,face,value):
        self.deck = deck
        self.suit = suit
        self.face = face
        self.value = value
    def __str__(self):
        return '{},{},{},{}'.format(self.deck,str(self.suit),str(self.face),str(self.value))
    def __repr__(self):
        return str(self)

class decisions:
    hit = 0
    stand = 1
    split = 2
    double = 3
    surrender = 4

def shuffle():
    cards = []
    
    for x in range(0,config.numDecks):
        for y in suits:
            index = 0
            for z in faces:
                cards.append(card(x,y,z,values[index]))
                index = index + 1
    random.shuffle(cards)
    return(cards)
