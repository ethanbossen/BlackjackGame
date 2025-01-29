import random
import time  # Import the time module for delays

class Dealer:
    def __init__(self, trait):
        self.trait = trait
        self.deck = self.initialize_deck()
        self.hand = []
        self.dialog_options = []

    def initialize_deck(self):
        """Create a standard 52-card deck."""
        if self.trait == 'standard':
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
            return [f"{rank} of {suit}" for suit in suits for rank in ranks]
        if self.trait == 'cunning':
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            ranks = ['4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
            return [f"{rank} of {suit}" for suit in suits for rank in ranks]

    def card_value(self, card):
        """Return the value of a card."""
        rank = card.split(' ')[0]
        if rank in ['Jack', 'Queen', 'King']:
            return 10
        elif rank == 'Ace':
            return 11
        else:
            return int(rank)

    def hand_value(self, hand):
        """Calculate the total value of a hand."""
        value = sum(self.card_value(card) for card in hand)
        # Adjust for Aces (if total > 21, treat Aces as 1 instead of 11)
        num_aces = sum(1 for card in hand if 'Ace' in card)
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def deal(self, player):
        """Deal cards to the dealer and player."""
        if len(self.deck) < 4:
            print("Not enough cards left to deal.")
            return

        random.shuffle(self.deck)
        if self.trait == 'standard':
            self.hand = [self.deck.pop(0), self.deck.pop(0)]
            player.hand = [self.deck.pop(0), self.deck.pop(0)]
        if self.trait == 'cunning':
            types = ["Hearts", "Diamonds", "Clubs", "Spades"]
            self.hand = [self.deck.pop(0), f"Jack of {types[(random.randint(0, 2))]}"]

        print(f"Dealer shows: {self.hand[0]}")
        print(f"Player has: {player.hand[0]} and {player.hand[1]}")

class Player:
    def __init__(self, cash=100):
        self.hand = []
        self.cash = cash

    def make_move(self, dealer):
        """Player chooses to 'hit' or 'stand'."""
        while True:
            move = input("Hit or Stand? (H/S): ").strip().lower()
            if move == 'h':
                self.hand.append(dealer.deck.pop(0))
                print(f"Player hits: {self.hand[-1]}")
                if dealer.hand_value(self.hand) > 21:
                    print(f"Player hand value: {dealer.hand_value(self.hand)} (Busted!)")
                    return 'bust'
            elif move == 's':
                print(f"Player stands with a hand value of: {dealer.hand_value(self.hand)}")
                return 'stand'
            else:
                print("Invalid input. Please enter 'H' to hit or 'S' to stand.")

class Game:
    def __init__(self):
        self.dealer = Dealer("cunning")
        self.player = Player()
        self.keep_playing = True

    def place_bet(self):
        """Prompt the player to place a bet."""
        while True:
            try:
                bet = int(input(f"Your cash: ${self.player.cash}. Place your bet: $"))
                if bet <= 0:
                    print("Bet must be greater than 0.")
                elif bet > self.player.cash:
                    print("You don't have enough cash for that bet.")
                else:
                    return bet
            except ValueError:
                print("Invalid input. Please enter a valid bet amount.")

    def play_round(self):
        """Start a round of Blackjack."""
        bet = self.place_bet()

        self.dealer.deal(self.player)

        # Player's turn
        result = self.player.make_move(self.dealer)
        if result == 'bust':
            print(f"Dealer wins! Player busted.")
            self.player.cash -= bet
            return

        # Dealer's turn
        dealer_value = self.dealer.hand_value(self.dealer.hand)
        while dealer_value < 17:  # Dealer hits until they have at least 17
            print("Dealer is deciding...")
            time.sleep(1)  # Add suspense
            self.dealer.hand.append(self.dealer.deck.pop(0))
            print(f"Dealer hits: {self.dealer.hand[-1]}")
            dealer_value = self.dealer.hand_value(self.dealer.hand)
            print(f"Dealer hand value: {dealer_value}")
            time.sleep(1)  # Add suspense

        print(f"Dealer stands with a hand value of: {dealer_value}")

        # Determine the winner
        player_value = self.dealer.hand_value(self.player.hand)
        print(f"Player hand value: {player_value}")

        if dealer_value > 21:
            print("Dealer busted! Player wins!")
            self.player.cash += bet
        elif player_value > dealer_value:
            print("Player wins!")
            self.player.cash += bet
        elif player_value < dealer_value:
            print("Dealer wins!")
            self.player.cash -= bet
        else:
            print("It's a tie!")

    def play(self):
        """Run the game loop until the player decides to quit or runs out of money."""
        while self.player.cash > 0 and self.keep_playing:
            print("\nNew round!")
            self.play_round()
            if self.player.cash > 0:
                play_again = input("Do you want to play another round? (Y/N): ").strip().lower()
                if play_again != 'y':
                    self.play = False
                    print("Thanks for playing!")
                    exit(0)
            else:
                print("You are out of money! Game over.")

# Start the game
game = Game()
game.play()