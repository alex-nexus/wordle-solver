from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Word:
    DISALLOWED_CHARS = ('-', ",", '.', "'", "/")

    chars: List[str]
    char_scores: List[int]

    def __init__(self, word_input: str):
        self.chars = [c for c in word_input.strip().lower()]
        self.char_scores = [0, 0, 0, 0, 0]

    @staticmethod
    def is_wordle_word(line: str):
        chars = [c for c in line.strip().lower()]
        if len(chars) != 5:
            return False
        for char in chars:
            if char.isdigit() or char in ('-', ",", '.', "'", "/"):
                return False

        return True

    @property
    def score(self) -> int:
        # uniq the char so repeated chars don't get double scored
        char_to_scores = {char: score
                          for char, score in zip(self.chars, self.char_scores)}
        return sum(char_to_scores.values())

    def __str__(self) -> str:
        return ('').join(self.chars)


@dataclass
class Response:
    RESPONSE_FLAGS = ['B', 'Y', 'G']

    guess_word: Word
    flags: List[str]

    def __init__(self, word: Word, flag_input: str):
        self.guess_word = word
        self.flags = [flag for flag in flag_input.strip().upper()]

    def is_word_qualified(self, word: Word) -> bool:
        for pos, tuple in enumerate(zip(self.guess_word.chars, self.flags)):
            char, flag = tuple

            if flag == 'B' and char in word.chars:
                return False

            if flag == 'Y' and (char not in word.chars or word.chars[pos] == char):
                return False

            if flag == 'G' and word.chars[pos] != char:
                return False

        return True


@dataclass
class WordleSolver:
    ALL_WORDS_FILE = 'wordle_words.txt'

    def __init__(self):
        self.wordle_words: List[Word] = []
        self.char_pos_frequency: Dict[str, int] = defaultdict(int)
        self.responses: List[Response] = []

        self._process_all_words_file()
        self._analyze_char_frequency()
        self._score_wordle_words()
        self._sort_wordle_words()  # sort by total scores

    def start(self, top_n: int = 10):
        round = 0
        while(round <= 6):
            round += 1
            print(f"Round {round}: Recommended Guesses:")

            qualified_words = self._qualified_words()
            print(f"There are {len(qualified_words)} candidates")
            for i, word in enumerate(qualified_words[0:top_n]):
                print(f"{i+1}): {word}")

            guess_index = input(f'Enter your guess(1-{top_n}):')
            guess_word = qualified_words[int(guess_index) - 1]
            response_input = input('Enter Wordle response:')
            self.responses.append(Response(guess_word, response_input))

    # preprocessing
    def _process_all_words_file(self):
        fh = open(self.ALL_WORDS_FILE, 'r')
        self.wordle_words = [Word(line) for line in fh.readlines()
                             if Word.is_wordle_word(line)]

    def _analyze_char_frequency(self):
        for word in self.wordle_words:
            for pos, char in enumerate(word.chars):
                self.char_pos_frequency[f"{char},{pos}"] += 1

    def _score_wordle_words(self):
        for word in self.wordle_words:
            for pos, char in enumerate(word.chars):
                word.char_scores[pos] = self.char_pos_frequency[f"{char},{pos}"]

    def _sort_wordle_words(self):
        self.wordle_words = sorted(
            self.wordle_words, key=lambda word: word.score, reverse=True)

    # game
    def _qualified_words(self) -> List[Word]:
        return [word for word in self.wordle_words
                if self._is_word_qualified(word)]

    def _is_word_qualified(self, word: Word) -> bool:
        for response in self.responses:
            if not response.is_word_qualified(word):
                return False
        return True


if __name__ == '__main__':
    solver = WordleSolver()
    solver.start(5)
