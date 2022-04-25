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
        self.words = self.rank_words(self.words)
        print(self.words[0:100])

    def add_response(self, response: Response):
        self.responses.append(response)

    def __str__(self) -> str:
        return str(self.__class__)

    @property
    def on_nth_guess(self) -> int:
        return len(self.responses) + 1


@dataclass
class AlgoV3(AlgoBase):
    def filter_disqualified_words(self, persist=False):
        def _is_word_qualified(response: Response, word: Word) -> bool:
            # currently if the answer has 2 of the same letters, if we guess
            # 1 letter right, wordle will return g or y for 1 letter but
            # return b for the other color
            for pos, (char, color) in enumerate(zip(response.word.chars, response.colors)):
                if color == 'b' and char in word.chars:
                    return False

                if color == 'y' and (char not in word.chars or word.chars[pos] == char):
                    return False

                # if self.on_nth_guess >= 3:  # tested better than 2 and 4
                if color == 'g' and word.chars[pos] != char:
                    return False

            return True

        def _does_word_pass_all_responses(word: Word) -> bool:
            return all([_is_word_qualified(response, word)
                        for response in self.responses])

        qualified_words = list(
            filter(lambda word: _does_word_pass_all_responses(word), self.words))

        if persist:
            self.words = qualified_words

        return qualified_words

    def rank_words(self, words: List[Word]):
        char_pos_to_counts = defaultdict(int)

        # iterate the entire word list and calcuate char+pos_frequency
        for word in words:
            for pos, char in enumerate(word.chars):
                char_pos_to_counts[f"{char}:{pos}"] += 1

        # sum each word's score
        for word in words:
            char_to_pos = {char: pos for pos, char in enumerate(word.chars)}
            for char, pos in char_to_pos.items():
                word.score += char_pos_to_counts[f"{char}:{pos}"]

        words.sort(key=lambda word: word.score, reverse=True)  # optional
        return words

    def guess_a_word(self) -> Word:
        return self.guess_words()[0]

    def guess_words(self) -> List[Word]:
        words = self.filter_disqualified_words(False)
        words = self.rank_words(words)
        print(f"qualified candidateds: {len(words)}")
        return words[0:self.top_n]

# algo v2
# algo v3 test the number of guesses before follow g
# algo v4 randomize ranking (lost)
# algo v5 only count by chars (lost)
# algo v6 count char only once by its highest
# algo v7 filter out and persist the words (doesn't work) => I suspect we need
# be more open otherwise we run out of options
# algo #8 recalculate ranking after filtering


@dataclass
class AlgoV8(AlgoV3):
    def guess_words(self) -> List[Word]:
        words = self.filter_disqualified_words(False)
        words = self.rank_words(words)
        print(f"qualified candidateds: {len(words)}")
        return words[0:self.top_n]
