import random

awnser = random.randint(1,10)

guess = int(input("Guess a number between 1 and 10 "))

while awnser != guess:
    guess = int(input("Wrong guess again "))
else:
    print("That was the number!")