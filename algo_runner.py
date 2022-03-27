from multiprocessing import Pool
import random
from typing import List

from models import Response, Word
from algos import AlgoV1, AlgoV2, AlgoV3


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
    def __init__(self, algo_name: str = 'AlgoV1', top_n=1, n_times=100):
        self.algo_name = algo_name
        self.top_n = top_n
        self.n_times = n_times

        self.algo = eval(f"{self.algo_name}(top_n)")

        self.random_words = self._random_words(n_times)

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

    def simulate(self) -> float:
        random_words = self.random_words

        with Pool(processes=4) as P:
            guesses_counts = P.map(self._solve_one, random_words)

        avg_guesses = float(sum(guesses_counts)) / len(random_words)
        print(f'Simulate {self.n_times} games: average {avg_guesses} steps')
        return avg_guesses

    def _reset_algo(self):
        self.algo.responses = []

    def _random_words(self, n_times: int = 10) -> List[Word]:
        fh = open('wordle-answers-alphabetical.txt', 'r')
        all_words = [Word(list(line.strip())) for line in fh.readlines()]
        random.shuffle(all_words)
        return all_words[0:n_times]

    def _solve_one(self, answer_word: Word) -> int:
        print(f"solve: {answer_word}")
        guesses_count = 0
        self._reset_algo()

        while(guesses_count <= 6):
            guess_word = self.algo.guess_a_word()
            guesses_count += 1
            response = calculate_response(answer_word, guess_word)
            print(f"\t{guesses_count}th guess: {guess_word} => {response}")
            self.algo.add_response(response)

            if response.is_game_over():
                print(f"Solved in {guesses_count} Guesses\n")
                return guesses_count
            elif guesses_count == 6:
                print('Did not solve')
                return guesses_count


if __name__ == '__main__':
    # AlgoRunner(top_n=5).run_cli()

    print({algo_name: AlgoRunner(algo_name, n_times=200).simulate()
           for algo_name in ['AlgoV1', 'AlgoV2', 'AlgoV3']})
