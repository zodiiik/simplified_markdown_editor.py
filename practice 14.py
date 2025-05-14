import random
import sys

class RockPaperScissors:
    def __init__(self):
        self.default_options = ['rock', 'paper', 'scissors']
        self.options = self.default_options
        self.user_name = ''
        self.user_score = 0
        self.ratings = {}

    def load_ratings(self):
        try:
            with open('rating.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split()
                    self.ratings[name] = int(score)
        except FileNotFoundError:
            self.ratings = {}

    def start_game(self):
        print("Enter your name: ", end='')
        self.user_name = input().strip()
        print(f"Hello, {self.user_name}")
        
        self.load_ratings()
        self.user_score = self.ratings.get(self.user_name, 0)
        
        print("Enter game options (comma-separated) or leave empty for default: ", end='')
        options_input = input().strip()
        if options_input:
            self.options = [opt.strip() for opt in options_input.split(',')]
        else:
            self.options = self.default_options
        
        print("Okay, let's start")
        self.game_loop()

    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return 'draw'
        
        index = self.options.index(user_choice)
        half_len = len(self.options) // 2
        losing_options = self.options[index+1:] + self.options[:index]
        losing_options = losing_options[:half_len]
        
        if computer_choice in losing_options:
            return 'win'
        else:
            return 'lose'

    def game_loop(self):
        while True:
            user_input = input("> ").strip().lower()
            
            if user_input == '!exit':
                print("Bye!")
                sys.exit()
            elif user_input == '!rating':
                print(f"Your rating: {self.user_score}")
            elif user_input in self.options:
                computer_choice = random.choice(self.options)
                result = self.determine_winner(user_input, computer_choice)
                
                if result == 'win':
                    print(f"Well done. The computer chose {computer_choice} and failed")
                    self.user_score += 100
                elif result == 'draw':
                    print(f"There is a draw ({computer_choice})")
                    self.user_score += 50
                else:
                    print(f"Sorry, but the computer chose {computer_choice}")
            else:
                print("Invalid input")

if __name__ == "__main__":
    game = RockPaperScissors()
    game.start_game()