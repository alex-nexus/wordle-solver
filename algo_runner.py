import random

from models import Response, Word
from algo_v1 import AlgoV1


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


class AlgoRunner:
    def __init__(self, algo_name: str = 'AlgoV1'):
        self.algo_name = algo_name
        if algo_name == 'AlgoV1':
            self.algo = AlgoV1()

    def run_cli(self, top_n: int = 1):
        while(True):
            guess_words = list(self.algo.guess_words())
            print(f"Recommendations out of {len(guess_words)}:")
            for i, word in enumerate(guess_words):
                print(f"\t{i+1}): {word}")

            choice = int(input(f'Choose (1-{len(guess_words)}):').strip())
            colors = list(input('Enter Wordle response:'))

            response = Response(guess_words[choice - 1], colors)
            if not response.is_valid():
                print("\tRESPONSE INVALID. Please try again\n")
            elif response.is_game_over():
                return print("Game Over! Congratulations!!")
            else:
                self.algo.add_response(response)

    # simulation

    def simulate(self, n_times: int = 10):
        i = 0
        total_guesses_count = 0
        for answer_word in self._random_words(n_times):
            i += 1
            print(f"{i}th game: {answer_word}")
            guesses_count = self._solve_one(answer_word)
            print(f"guesses_count:{guesses_count}")
            total_guesses_count += guesses_count

        avg_guesses = float(total_guesses_count) / i
        print(
            f'Simulate {n_times} games: {self.algo} takes {avg_guesses} steps')

    def _random_words(self, n_times: int = 10):
        fh = open('wordle-answers-alphabetical.txt', 'r')
        all_words = [Word(list(line.strip())) for line in fh.readlines()]
        random.shuffle(all_words)
        return all_words[0:n_times]

    def _solve_one(self, answer_word: Word):
        guesses_count = 0

        while(guesses_count <= 6):
            guess_word = list(self.algo.guess_words())[0]
            guesses_count += 1
            print(f"\t{guesses_count}th guess: guess_word: {guess_word}")
            response = calculate_response(answer_word, guess_word)
            print(f"\t\t=> response: {response}")
            self.algo.add_response(response)

            if response.is_game_over():
                print("Game Over! Congratulations!!")
                return guesses_count

        print('Did not solve')


if __name__ == '__main__':
    # AlgoRunner().run_cli(1)
    AlgoRunner().simulate(1)
