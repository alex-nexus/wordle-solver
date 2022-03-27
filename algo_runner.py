import random
from typing import List

from models import Response, Word
from algos import AlgoV1, AlgoV2


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
    def __init__(self, algo_name: str = 'AlgoV1', top_n=1):
        self.algo_name = algo_name
        if self.algo_name == 'AlgoV1':
            self.algo = AlgoV1(top_n)

    def run_cli(self):
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
        print(f'Simulate {n_times} games: average {avg_guesses} steps')

    def _reset_algo(self):
        self.algo.responses = []

    def _random_words(self, n_times: int = 10) -> List[Word]:
        fh = open('wordle-answers-alphabetical.txt', 'r')
        all_words = [Word(list(line.strip())) for line in fh.readlines()]
        random.shuffle(all_words)
        return all_words[0:n_times]

    def _solve_one(self, answer_word: Word) -> int:
        guesses_count = 0
        self._reset_algo()

        while(guesses_count <= 6):
            guess_word = self.algo.guess_a_word()
            guesses_count += 1
            print(f"\t{guesses_count}th guess: guess_word: {guess_word}")
            response = calculate_response(answer_word, guess_word)
            print(f"\t\t=> response: {response}")
            self.algo.add_response(response)

            if response.is_game_over():
                print("Game Over! Congratulations!!")
                return guesses_count
            elif guesses_count == 6:
                print('Did not solve')
                return guesses_count


if __name__ == '__main__':
    # AlgoRunner(top_n=5).run_cli()
    AlgoRunner().simulate(100)
