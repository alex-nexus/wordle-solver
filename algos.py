from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, List

from models import Word, Response


@dataclass
class AlgoBase:
    top_n: int = 1
    responses: List[Response] = field(default_factory=list)

    def __post_init__(self):
        fh = open('wordle-answers-alphabetical.txt', 'r')
        self.words = [Word(list(line.strip())) for line in fh.readlines()]
        self.rank_words()

    def add_response(self, response: Response):
        self.responses.append(response)

    def __str__(self) -> str:
        return str(self.__class__)

    @property
    def on_nth_guess(self) -> int:
        return len(self.responses) + 1


@dataclass
class AlgoV1(AlgoBase):
    def rank_words(self):
        char_pos_to_counts = defaultdict(int)

        # iterate the entire word list and calcuate char+pos_frequency
        for word in self.words:
            for pos, char in enumerate(word.chars):
                char_pos_to_counts[f"{char}:{pos}"] += 1

        # sum each word's score
        for word in self.words:
            char_to_pos = {char: pos for pos, char in enumerate(word.chars)}
            for char, pos in char_to_pos.items():
                word.score += char_pos_to_counts[f"{char}:{pos}"]

        self.words.sort(key=lambda word: word.score, reverse=True)  # optional

    def guess_a_word(self) -> Word:
        return self.guess_words()[0]

    def guess_words(self) -> List[Word]:
        def _is_word_qualified(response: Response, word: Word) -> bool:
            for pos, (char, color) in enumerate(zip(response.word.chars, response.colors)):
                if color == 'b' and char in word.chars:
                    return False

                if color == 'y' and (char not in word.chars or word.chars[pos] == char):
                    return False

                if color == 'g' and word.chars[pos] != char:
                    return False

            return True

        def _does_word_pass_all_responses(word: Word) -> bool:
            return all([_is_word_qualified(response, word)
                        for response in self.responses])

        words = list(
            filter(lambda word: _does_word_pass_all_responses(word), self.words))

        return words[0:self.top_n]


@dataclass
class AlgoV2(AlgoV1):
    def guess_a_word(self) -> Word:
        if self.on_nth_guess == 1:
            return Word(list('slice'))
        elif self.on_nth_guess == 2:
            return Word(list('train'))
        else:
            return self.guess_words()[0]


@dataclass
class AlgoV3(AlgoV1):
    def guess_words(self) -> List[Word]:
        def _is_word_qualified(response: Response, word: Word) -> bool:
            for pos, (char, color) in enumerate(zip(response.word.chars, response.colors)):
                if color == 'b' and char in word.chars:
                    return False

                if color == 'y' and (char not in word.chars or word.chars[pos] == char):
                    return False

                if self.on_nth_guess >= 1:
                    if color == 'g' and word.chars[pos] != char:
                        return False

            return True

        def _does_word_pass_all_responses(word: Word) -> bool:
            return all([_is_word_qualified(response, word)
                        for response in self.responses])

        words = list(
            filter(lambda word: _does_word_pass_all_responses(word), self.words))

        return words[0:self.top_n]
