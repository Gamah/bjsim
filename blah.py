import strategies
import utilities


playerHand = [5,5,1]

print(utilities.handTotal(playerHand))    
print(str(strategies.basic(playerHand,[2,10])))