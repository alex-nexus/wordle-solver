from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List

WORDLE_WORDS_FILE = 'wordle_words.txt'


def is_wordle_word(line: str):
    chars = [c for c in line.strip().lower()]
    if len(chars) != 5:
        return False
    for char in chars:
        if char.isdigit() or char in ('-', ",", '.', "'", "/"):
            return False

    return True


@dataclass
class Word:
    DISALLOWED_CHARS = ('-', ",", '.', "'", "/")

    chars: List[str]
    char_scores: List[int]

    def __init__(self, word_input: str):
        self.chars = [c for c in word_input.strip().lower()]
        self.char_scores = [0, 0, 0, 0, 0]

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
    word: Word
    flags_str: str

    def is_word_qualified(self, word: Word) -> bool:
        for pos, (char, flag) in enumerate(zip(self.word.chars, list(self.flags_str))):
            if flag == 'b' and char in word.chars:
                return False

            if flag == 'y' and (char not in word.chars or word.chars[pos] == char):
                return False

            if flag == 'g' and word.chars[pos] != char:
                return False

        return True


@dataclass
class WordleSolver:
    wordle_words: List[Word] = field(default_factory=list)

    def __init__(self):
        self._load_wordle_words()
        char_pos_frequency = self._analyze_char_frequency()
        self._score_words(char_pos_frequency)
        self._sort_words_by_score()  # sort by total scores

    def start(self, top_n: int = 10):
        self.responses: List[Response] = []

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
    def _load_wordle_words(self):
        fh = open(WORDLE_WORDS_FILE, 'r')
        self.wordle_words = [Word(line) for line in fh.readlines()]

    def _analyze_char_frequency(self) -> Dict[str, int]:
        char_pos_frequency: Dict[str, int] = defaultdict(int)
        for word in self.wordle_words:
            for pos, char in enumerate(word.chars):
                char_pos_frequency[f"{char},{pos}"] += 1
        return char_pos_frequency

    def _score_words(self, char_pos_frequency: Dict[str, int]):
        for word in self.wordle_words:
            for pos, char in enumerate(word.chars):
                word.char_scores[pos] = char_pos_frequency[f"{char},{pos}"]

    def _sort_words_by_score(self):
        self.wordle_words.sort(key=lambda word: word.score,  reverse=True)

    # game
    def _qualified_words(self) -> List[Word]:
        return [word for word in self.wordle_words
                if self._is_word_qualified(word)]

    def _is_word_qualified(self, word: Word) -> bool:
        return all([response.is_word_qualified(word) for response in self.responses])


if __name__ == '__main__':
    solver = WordleSolver()
    solver.start(5)
