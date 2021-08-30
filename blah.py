import strategies
import utilities


test = [1,2,3,4,5,6]

for number in test:
    if number > 3:
        test.append(9)
print(test)

playerHand = [2,4,2,2]

print(utilities.handTotal(playerHand))    
print(str(strategies.basic(playerHand,[2,10])))