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

    def is_wordle_word(self):
        if len(self.chars) != 5:
            return False

        for char in self.chars:
            if char.isdigit() or char in self.DISALLOWED_CHARS:
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

            if flag == 'B':
                if char in word.chars:
                    return False

            if flag == 'Y':
                if char not in word.chars:
                    return False

                if word.chars[pos] == char:
                    return False

            if flag == 'G':
                if word.chars[pos] != char:
                    return False

        return True


@dataclass
class WordleSolver:
    ALL_WORDS_FILE = 'files/all_words.txt'
    WORDLE_WORDS_FILE = 'files/wordle_words.txt'
    CHAR_FREQUENCY_FILE = 'files/char_pos_frequency.txt'

    wordle_words: List[Word] = field(default_factory=list)
    char_pos_frequency: Dict[str, int] = field(default_factory=dict)

    responses: List[Response] = field(default_factory=list)

    def __post_init__(self):
        self._process_all_words_file()
        self._score_wordle_words()
        self._sort_wordle_words()  # sort by total scores

    def start(self, top_n: int = 10):
        round = 0
        while(round <= 6):
            round += 1
            print(f"Round {round}: Recommended Guesses:")

            top_words = self._guess_top_words(top_n)
            for i, word in enumerate(top_words):
                print(f"{i+1}): {word}")

            guess_index = input(f'Enter your guess(1-{len(top_words)}):')
            guess_word = top_words[int(guess_index) - 1]
            response_input = input('Enter Wordle response:')
            self.responses.append(Response(guess_word, response_input))

    # private

    # preprocessing

    def _process_all_words_file(self):
        rf = open(self.ALL_WORDS_FILE, 'r')
        lines = rf.readlines()
        for line in lines:
            word = Word(line)
            if word.is_wordle_word():
                self.wordle_words.append(word)
                self._count_char_frequency(word)

    def _score_wordle_words(self):
        for word in self.wordle_words:
            for pos, char in enumerate(word.chars):
                word.char_scores[pos] = self.char_pos_frequency[f"{char},{pos}"]

    def _sort_wordle_words(self):
        self.wordle_words = sorted(
            self.wordle_words, key=lambda word: word.score, reverse=True)

    def _count_char_frequency(self, word: Word):
        for pos, char in enumerate(word.chars):
            if self.char_pos_frequency.get(f"{char},{pos}") is None:
                self.char_pos_frequency[f"{char},{pos}"] = 0

            self.char_pos_frequency[f"{char},{pos}"] += 1

    # game
    def _guess_top_words(self, top_n=10) -> List[Word]:
        count = 0
        guess_words: List[Word] = []

        for word in self.wordle_words:
            if count >= top_n:
                return guess_words

            # print(f"{word} / {self.is_word_qualified(word)}")
            if self.is_word_qualified(word):
                count += 1
                guess_words.append(word)

        return guess_words

    def is_word_qualified(self, word: Word) -> bool:
        for response in self.responses:
            if not response.is_word_qualified(word):
                return False
        return True


solver = WordleSolver()
solver.start(10)
