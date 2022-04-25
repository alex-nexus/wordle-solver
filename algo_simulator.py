from multiprocessing import Pool
import random
from typing import List

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


class AlgoSimulator:
    def __init__(self, algo_name: str = 'AlgoV3', top_n=1, n_times=100):
        self.algo_name = algo_name
        self.top_n = top_n
        self.n_times = n_times

        self.algo = eval(f"{self.algo_name}(top_n)")
        self.random_words = self._random_words(n_times)

    def simulate(self) -> float:
        random_words = self.random_words

        with Pool(processes=1) as P:
            guesses_counts = P.map(self._solve_one, random_words)

        avg_guesses = float(sum(guesses_counts)) / len(random_words)
        print(f'Simulate {self.n_times} games: average {avg_guesses} steps')
        return avg_guesses

    def _random_words(self, n_times: int = 10) -> List[Word]:
        fh = open('wordle-answers-alphabetical.txt', 'r')
        all_words = [Word(list(line.strip())) for line in fh.readlines()]
        random.shuffle(all_words)
        return all_words[0:n_times]

    def _solve_one(self, answer_word: Word) -> int:
        print(f"Solve: {answer_word}")
        guesses_count = 0
        self._reset_algo()

        while(guesses_count <= 6):
            guess_word = self.algo.guess_a_word()
            guesses_count += 1
            response = calculate_response(answer_word, guess_word)
            self.algo.add_response(response)

            if response.is_game_over():
                print(f"Solved {answer_word} in {guesses_count} Guesses\n")
                return guesses_count
            elif guesses_count == 6:
                print(f'Did not solve {answer_word}')
                return guesses_count

    def _reset_algo(self):
        self.algo.responses = []


if __name__ == '__main__':
    print({algo_name: AlgoSimulator(algo_name, n_times=1000).simulate()
           for algo_name in ['AlgoV8', 'AlgoV3']})
