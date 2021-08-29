import random
import config

#card values
suits = ["D","S","H","C"]
faces = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
values = [1,2,3,4,5,6,7,8,9,10,10,10,10]
#faces = ["K","A"]
#values = [10,1]

#build shoe
def getShoe():
    newShoe = []
    
    for x in range(0,config.numDecks):
        for y in suits:
            index = 0
            for z in faces:
                newShoe.append(card(x,y,z,values[index]))
                index = index + 1
    random.shuffle(newShoe)
    return(newShoe)


class hand:
    cards = []
    value = 0
    
    def faces():
        faces = []
        for card in cards:  
            faces.append(card.face)
        return faces
        
    def values():
        values = []
        for card in cards:
            values.append(card.value)
        return values
        

class player:
    hands = []
    

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

def handTotal(hand):
    if len(hand) == 2 and 10 in hand and 1 in hand:
        return 21
    total = sum(hand)
    if 1 in hand and total < 12:
        total = total + 10
    
    return total
