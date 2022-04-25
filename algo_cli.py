from models import Response, Word
from algos import *


def calculate_response(answer_word: Word, guess_word: Word):
    response = Response(guess_word)

    for i, char in enumerate(guess_word.chars):
        if char == answer_word.chars[i]:
            response.colors.append('g')
        elif char in answer_word.chars:
            response.colors.append('y')
        else:
            response.colors.append('b')

    return response


class AlgoCli:
    def __init__(self, algo_name: str = 'AlgoV8', top_n=1, n_times=100):
        self.algo_name = algo_name
        self.top_n = top_n
        self.n_times = n_times

        self.algo = eval(f"{self.algo_name}(top_n)")

    def run_cli(self):
        while(True):
            guess_words = list(self.algo.guess_words())
            print(f"Recommendations out of {len(guess_words)}:")
            for i, word in enumerate(guess_words):
                print(f"\t{i+1}): {word}")

            choice = input(f'Choose (1-{len(guess_words)} or other):').strip()
            if choice == 'other':
                word = Word(list(input('Enter Wordle word:')))
                colors = list(input('Enter Wordle response:'))
                response = Response(word, colors)
            else:
                choice = int(choice)
                colors = list(input('Enter Wordle response:'))
                response = Response(guess_words[choice - 1], colors)

            if not response.is_valid():
                print("\tRESPONSE INVALID. Please try again\n")
            elif response.is_game_over():
                return print("Solved!")
            else:
                self.algo.add_response(response)


if __name__ == '__main__':
    AlgoCli(top_n=5).run_cli()
