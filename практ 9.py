import random

def get_pencils():
    while True:
        pencils = input("How many pencils would you like to use:\n")
        if not pencils.isdigit():
            print("The number of pencils should be numeric")
            continue
        pencils = int(pencils)
        if pencils <= 0:
            print("The number of pencils should be positive")
            continue
        return pencils

def get_first_player():
    while True:
        player = input("Who will be the first (John, Jack):\n")
        if player not in ("John", "Jack"):
            print("Choose between 'John' and 'Jack'")
            continue
        return player

def bot_move(pencils):
    if pencils % 4 == 0:
        return 3
    elif pencils % 4 == 3:
        return 2
    elif pencils % 4 == 2:
        return 1
    else:
        return random.randint(1, min(3, pencils))

def get_player_move(pencils):
    while True:
        move = input("John's turn:\n" if current_player == "John" else "")
        if not move.isdigit():
            print("Possible values: '1', '2' or '3'")
            continue
        move = int(move)
        if move not in (1, 2, 3):
            print("Possible values: '1', '2' or '3'")
            continue
        if move > pencils:
            print("Too many pencils were taken")
            continue
        return move

def play_game():
    pencils = get_pencils()
    current_player = get_first_player()
    
    while pencils > 0:
        print("|" * pencils)
        if current_player == "John":
            move = get_player_move(pencils)
        else:
            move = bot_move(pencils)
            print(move)
        
        pencils -= move
        if pencils == 0:
            print(f"{current_player} won!")
            break
        current_player = "Jack" if current_player == "John" else "John"

if __name__ == "__main__":
    play_game()