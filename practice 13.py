import random
import os

class ArithmeticTest:
    def __init__(self):
        self.levels = {
            1: {
                'description': 'simple operations with numbers 2-9',
                'generate_question': self.generate_simple_question
            },
            2: {
                'description': 'integral squares of 11-29',
                'generate_question': self.generate_square_question
            }
        }
        self.correct_answers = 0

    def run(self):
        level = self.select_level()
        for _ in range(5):
            question, correct_answer = self.levels[level]['generate_question']()
            self.ask_question(question, correct_answer)
        self.show_results(level)
        self.save_results(level)

    def select_level(self):
        while True:
            print("Which level do you want? Enter a number:")
            for num, info in self.levels.items():
                print(f"{num} - {info['description']}")
            try:
                level = int(input("> "))
                if level in self.levels:
                    return level
                print("Incorrect format.")
            except ValueError:
                print("Incorrect format.")

    def generate_simple_question(self):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        operation = random.choice(['+', '-', '*'])
        question = f"{a} {operation} {b}"
        correct_answer = eval(question)
        return question, correct_answer

    def generate_square_question(self):
        number = random.randint(11, 29)
        question = str(number)
        correct_answer = number ** 2
        return question, correct_answer

    def ask_question(self, question, correct_answer):
        while True:
            print(question)
            user_answer = input("> ")
            try:
                user_answer = int(user_answer)
                if user_answer == correct_answer:
                    print("Right!")
                    self.correct_answers += 1
                else:
                    print("Wrong!")
                break
            except ValueError:
                print("Incorrect format.")

    def show_results(self, level):
        print(f"Your mark is {self.correct_answers}/5.")

    def save_results(self, level):
        answer = input('Would you like to save your result to the file? Enter yes or no.\n> ').lower()
        if answer in ['yes', 'y']:
            name = input("What is your name?\n> ")
            result_line = f"{name}: {self.correct_answers}/5 in level {level} ({self.levels[level]['description']})."
            
            with open("results.txt", "a") as f:
                f.write(result_line + "\n")
            
            print('The results are saved in "results.txt".')

if __name__ == "__main__":
    test = ArithmeticTest()
    test.run()