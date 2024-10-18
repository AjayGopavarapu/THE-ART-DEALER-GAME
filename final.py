#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import os

# Define basic card symbols and values
card_symbols = {
    "spades": chr(0x2660),
    "hearts": chr(0x2665),
    "clubs": chr(0x2663),
    "diamonds": chr(0x2666)
}
symbols = [
    card_symbols["spades"],
    card_symbols["hearts"],
    card_symbols["clubs"],
    card_symbols["diamonds"]
]
card_nums = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# Define card values and prime numbers for Grades 3-5 and 6-8
card_values = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}
prime_nums = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
black_jack = ["J" + card_symbols["spades"], "J" + card_symbols["clubs"]]  # Jack of Spades and Jack of Clubs

# Define a mapping between suit names and symbols for easier input
suit_mapping = {
    "Spades": card_symbols["spades"],
    "Hearts": card_symbols["hearts"],
    "Clubs": card_symbols["clubs"],
    "Diamonds": card_symbols["diamonds"]
}

# Reverse mapping to make output more user-friendly
reverse_suit_mapping = {v: k for k, v in suit_mapping.items()}

# Function for the game logo with card shapes
def logo():
    print("=" * 50)
    print(" " * 12 + card_symbols["hearts"] + " " * 2 + "ART DEALER GAME" + " " * 2 + card_symbols["spades"])
    print("=" * 50)
    print(" " * 7 + card_symbols["diamonds"] + " Welcome to the Art Dealer Game! " + card_symbols["clubs"])
    print("Get ready to guess which paintings the dealer is interested in!")
    print("=" * 50)
    print(f"{card_symbols['spades']} {card_symbols['hearts']} {card_symbols['clubs']} {card_symbols['diamonds']}\n")

# Function to show balloons and flowers when the player wins
def show_celebration():
    print("\nCongratulations! You guessed correctly!")
    print("\U0001F388" * 5 + " \U0001F490" * 3)
    print("Balloons and flowers everywhere! You are the winner!")
    print("\U0001F388" * 5 + " \U0001F490" * 3 + "\n")

# Function to show sad emojis when the player loses
def show_sadness():
    print("\nSorry, that's the wrong guess!")
    print("\U0001F641" * 3 + " Better luck next time! " + "\U0001F641" * 3)
    print()

# Function to clear the screen (for hiding the dealer's pattern in multiplayer)
def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

# Function to generate random cards with suit names
def generate_card():
    number = random.choice(list(card_values.keys()))
    suit = random.choice(list(suit_mapping.values()))
    return number + suit

# Function for K-2 level
def play_k2():
    print("Welcome to the K-2 Art Dealer Game!")

    # Simple patterns for K-2: all red, all queens, etc.
    patterns = [
        "All Red Cards",
        "All Black Cards",
        "All Hearts",
        "All Queens"
    ]
    dealer_pattern = random.choice(patterns)

    print(f"The dealer is looking for a pattern. Try to guess it!")

    for i in range(3):
        guess = input(f"Guess #{i+1}: Choose a pattern from {patterns} or type 'quit' to exit: ").strip().title()

        if guess == 'Quit':
            print("You chose to quit. Thanks for playing!")
            return

        if guess == dealer_pattern:
            show_celebration()  # Winning message with balloons and flowers
            return
        else:
            print("Incorrect guess.")

    print(f"Sorry, the correct pattern was {dealer_pattern}.")
    show_sadness()  # Losing message with sad emojis

# Function for Grades 3-5
def play_35():
    print("Welcome to the Grades 3-5 Art Dealer Game!")

    # More complex patterns for Grades 3-5
    patterns = [
        "All Prime Numbers",
        "Cards Adding to 9",
        "An Ace and a Black Jack"
    ]
    dealer_pattern = random.choice(patterns)

    print(f"The dealer is looking for a pattern. Try to guess it!")

    # Generate random cards for the user to choose from
    deck = [generate_card() for _ in range(4)]

    # Display deck with suit names
    human_readable_deck = [f"{card[:-1]} {reverse_suit_mapping[card[-1]]}" for card in deck]
    print(f"Your cards to choose from: {human_readable_deck}")

    selected_cards = []
    for i in range(3):
        while True:
            guess = input(f"Select card #{i+1} from {human_readable_deck} (e.g., '4 Spades'): ").strip().title()

            # Translate user input back into the format we use internally (e.g., "4 Spades" to "4♠")
            try:
                number, suit = guess.split()
                suit_symbol = suit_mapping[suit]
                card = number + suit_symbol
            except (ValueError, KeyError):
                print("Invalid selection. Please enter the card as 'Number Suit' (e.g., '4 Spades').")
                continue

            if card in deck:
                selected_cards.append(card)
                deck.remove(card)
                human_readable_deck.remove(guess)
                break
            else:
                print(f"Invalid selection. Please choose a card from {human_readable_deck}.")

    # Now check if the selected cards match the dealer's pattern
    if dealer_pattern == "All Prime Numbers":
        if all(card[:-1] in {"2", "3", "5", "7"} for card in selected_cards):
            show_celebration()  # Winning message
        else:
            print("Sorry, your selected cards do not match the prime number pattern.")
            show_sadness()  # Losing message

    elif dealer_pattern == "Cards Adding to 9":
        total_value = sum(card_values[card[:-1]] for card in selected_cards)
        if total_value == 9:
            show_celebration()  # Winning message
        else:
            print(f"Sorry, the total value of your selected cards is {total_value}, which does not add up to 9.")
            show_sadness()  # Losing message

    elif dealer_pattern == "An Ace and a Black Jack":
        if any(card[:-1] == "A" for card in selected_cards) and any(card in black_jack for card in selected_cards):
            show_celebration()  # Winning message
        else:
            print(f"Sorry, you did not select an Ace and a Black Jack.")
            show_sadness()  # Losing message

# Functions for Grades 6-8
def check_full_house(selected_cards):
    """Check if the cards form a Full House (3 of one rank, 2 of another)."""
    card_ranks = [card[:-1] for card in selected_cards]
    rank_count = {rank: card_ranks.count(rank) for rank in card_ranks}
    return sorted(rank_count.values()) == [2, 3]

def check_all_spades(selected_cards):
    """Check if all the cards are Spades."""
    return all(card.endswith("♠") for card in selected_cards)

def check_prime_sum(selected_cards):
    """Check if the total value of the cards adds up to a prime number."""
    total_value = sum(card_values[card[:-1]] for card in selected_cards)
    return total_value in prime_nums

def play_68():
    print("Welcome to the Grades 6-8 Art Dealer Game!")

    # Choose game mode: Single-Player or Multiplayer
    while True:
        mode = input("Select game mode:\n1. Single-Player\n2. Multiplayer\nEnter 1 or 2: ").strip()
        if mode == "1" or mode.lower() == "single-player":
            single_player = True
            break
        elif mode == "2" or mode.lower() == "multiplayer":
            single_player = False
            break
        else:
            print("Invalid selection. Please enter 1 for Single-Player or 2 for Multiplayer.")

    # More complex patterns for Grades 6-8
    patterns = [
        "A Full House",
        "All Cards Are Spades",
        "Cards Adding to a Prime Number"
    ]

    if single_player:
        dealer_pattern = random.choice(patterns)
    else:
        # Multiplayer: Player 1 selects the pattern
        print("\nPlayer 1: Choose a pattern for Player 2 to guess from the following list:")
        for idx, pattern in enumerate(patterns, 1):
            print(f"{idx}. {pattern}")
        while True:
            try:
                choice = int(input("Enter the number corresponding to your chosen pattern: ").strip())
                if 1 <= choice <= len(patterns):
                    dealer_pattern = patterns[choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(patterns)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Clear the screen to hide the dealer's pattern from Player 2
        clear_screen()
        print("Player 2: It's your turn to guess the pattern!\n")

    print(f"The dealer is looking for a pattern. Try to guess it!")

    # Generate random cards for the user to choose from (Single-Player) or prepare deck (Multiplayer)
    if single_player:
        deck = [generate_card() for _ in range(5)]  # 5 cards for Grades 6-8
    else:
        # In Multiplayer, allow Player 1 to select the cards to present
        print("Player 1: Please lay out 5 cards for Player 2 to choose from.")
        deck = []
        human_readable_deck = []
        for i in range(5):
            while True:
                number = input(f"Enter card #{i+1} number/face (A, 2-10, J, Q, K): ").strip().upper()
                if number not in card_nums:
                    print("Invalid card number/face. Please try again.")
                    continue
                suit = input(f"Enter card #{i+1} suit (Spades, Hearts, Clubs, Diamonds): ").strip().title()
                if suit not in suit_mapping:
                    print("Invalid suit. Please try again.")
                    continue
                card = number + suit_mapping[suit]
                deck.append(card)
                human_readable_deck.append(f"{number} {suit}")
                break
        print(f"Player 2: Your cards to choose from: {human_readable_deck}")
    if single_player:
        # Display deck with suit names
        human_readable_deck = [f"{card[:-1]} {reverse_suit_mapping[card[-1]]}" for card in deck]
        print(f"Your cards to choose from: {human_readable_deck}")

    selected_cards = []
    num_cards = 5
    if not single_player:
        num_cards = 5  # For multiplayer, always 5 cards

    for i in range(num_cards):
        while True:
            guess = input(f"Select card #{i+1} from {human_readable_deck} (e.g., '4 Spades'): ").strip().title()

            # Translate user input back into the format we use internally (e.g., "4 Spades" to "4♠")
            try:
                number, suit = guess.split()
                suit_symbol = suit_mapping[suit]
                card = number + suit_symbol
            except (ValueError, KeyError):
                print("Invalid selection. Please enter the card as 'Number Suit' (e.g., '4 Spades').")
                continue

            if card in deck:
                selected_cards.append(card)
                deck.remove(card)
                human_readable_deck.remove(guess)
                break
            else:
                print(f"Invalid selection. Please choose a card from {human_readable_deck}.")

    # Now check if the selected cards match the dealer's pattern
    if dealer_pattern == "A Full House":
        if check_full_house(selected_cards):
            show_celebration()  # Winning message
        else:
            print("Sorry, your selected cards do not form a Full House.")
            show_sadness()  # Losing message

    elif dealer_pattern == "All Cards Are Spades":
        if check_all_spades(selected_cards):
            show_celebration()  # Winning message
        else:
            print("Sorry, your selected cards are not all Spades.")
            show_sadness()  # Losing message

    elif dealer_pattern == "Cards Adding to a Prime Number":
        if check_prime_sum(selected_cards):
            show_celebration()  # Winning message
        else:
            total_value = sum(card_values[card[:-1]] for card in selected_cards)
            print(f"Sorry, the total value of your selected cards is {total_value}, which does not add up to a prime number.")
            show_sadness()  # Losing message

# Function to select grade level
def select_grade_level():
    print("Select the grade level:")
    print("1. K-2")
    print("2. Grades 3-5")
    print("3. Grades 6-8")

    choice = input("Enter the corresponding number for the grade level: ").strip()
    if choice == "1":
        return "K-2"
    elif choice == "2":
        return "Grades 3-5"
    elif choice == "3":
        return "Grades 6-8"
    else:
        print("Invalid selection, defaulting to K-2.")
        return "K-2"

# Main function
def main():
    logo()  # Display the logo
    while True:
        # Select the grade level
        grade_level = select_grade_level()
        print(f"Starting game at level: {grade_level}")

        if grade_level == "K-2":
            play_k2()
        elif grade_level == "Grades 3-5":
            play_35()
        elif grade_level == "Grades 6-8":
            play_68()

        # Ask if they want to play again
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing!")
            break

# Call main function
if __name__ == "__main__":
    main()


# In[ ]:




