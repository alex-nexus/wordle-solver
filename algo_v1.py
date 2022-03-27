from collections import defaultdict
from typing import Iterable

from models import Word, Response


class AlgoV1:
    def __init__(self, top_n: int = 1):
        self.top_n = top_n

        self.responses = []

        fh = open('wordle-answers-alphabetical.txt', 'r')
        self.words = [Word(list(line.strip())) for line in fh.readlines()]
        self._score_words_by_char_pos_frequency()
        self.words.sort(key=lambda word: word.score, reverse=True)  # optional

    def guess_words(self) -> Iterable[Word]:
        def _is_word_qualified(word: Word) -> bool:
            return all([r.is_word_qualified(word) for r in self.responses])

        words = list(filter(lambda word: _is_word_qualified(word), self.words))
        return words[0:self.top_n]

    def _score_words_by_char_pos_frequency(self):
        char_pos_to_counts = defaultdict(int)

        for word in self.words:
            for pos, char in enumerate(word.chars):
                char_pos_to_counts[f"{char}:{pos}"] += 1

        for word in self.words:
            char_to_pos = {char: pos for pos, char in enumerate(word.chars)}
            for char, pos in char_to_pos.items():
                word.score += char_pos_to_counts[f"{char}:{pos}"]

    def add_response(self, response: Response):
        self.responses.append(response)

    def __str__(self) -> str:
        return 'AlgoV1'
