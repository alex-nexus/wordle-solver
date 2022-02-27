from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Word:
    chars: List[str]
    char_scores: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])

    def score(self) -> int:
        # the summation of each (char,pos) frequency
        return sum(self.char_scores)

    def __str__(self) -> str:
        return ('').join(self.chars)


@dataclass
class Response:
    word: Word
    colors: List[str]

    def is_word_qualified(self, word: Word) -> bool:
        for pos, (char, color) in enumerate(zip(self.word.chars, self.colors)):
            if color == 'b' and char in word.chars:
                return False

            if color == 'y' and (char not in word.chars or word.chars[pos] == char):
                return False

            if color == 'g' and word.chars[pos] != char:
                return False

        return True


class WordleSolver:
    words: List[Word] = field(default_factory=list)

    def __init__(self):
        fh = open('wordle_words.txt', 'r')
        self.words = [Word(list(line.strip())) for line in fh.readlines()]

    def __post_init__(self):
        self._score_words_by_char_frequency()
        self.words.sort(key=lambda word: word.score(), reverse=True)

    def start(self, top_n: int = 6):
        self.responses: List[Response] = []

        round = 0
        while(round <= 6):
            round += 1
            print(f"Round {round}: Recommended Guesses:")

            qualified_words = self._get_qualified_words()
            print(f"There are {len(qualified_words)} candidates")
            for i, word in enumerate(qualified_words[0:top_n]):
                print(f"{i+1}): {word}")

            choice = input(f'Choose your guess(1-{top_n}):')
            guess_word = qualified_words[int(choice) - 1]
            colors_input = input('Enter Wordle response:')
            if colors_input == 'ggggg':
                print("congratulations!!")
                return

            self.responses.append(Response(guess_word, list(colors_input)))

    def _score_words_by_char_frequency(self):
        char_pos_frequency: Dict[str, int] = defaultdict(int)
        for word in self.words:
            for pos, char in enumerate(word.chars):
                char_pos_frequency[f"{char},{pos}"] += 1

        for word in self.words:
            for pos, char in enumerate(word.chars):
                word.char_scores[pos] = char_pos_frequency[f"{char},{pos}"]

    def _get_qualified_words(self) -> List[Word]:
        def _is_word_qualified(word: Word) -> bool:
            return all([response.is_word_qualified(word) for response in self.responses])

        return list(filter(lambda word: _is_word_qualified(word), self.words))


if __name__ == '__main__':
    WordleSolver().start()
