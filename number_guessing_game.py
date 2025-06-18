# number_guessing_game.py
# A simple number guessing game for beginners.
# Author: Jason d Broomes

import random

# Generate a random number between 1 and 10
secret_number = random.randint(1, 10)

# Ask the user to guess the number
guess = int(input("Guess a number between 1 and 10: "))

# Check if the guess is correct
if guess == secret_number:
    print("🎉 You guessed it! Great job!")
else:
    print(f"❌ Nope, the number was {secret_number}. Better luck next time!")
