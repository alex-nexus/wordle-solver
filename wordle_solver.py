from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Iterable


@dataclass
class Word:
    chars: List[str]
    score: int = field(default_factory=lambda: 0)

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
    def __init__(self):
        fh = open('wordle_words.txt', 'r')  # filtered and sorted words
        self.words = [Word(list(line.strip())) for line in fh.readlines()]

    def __post_init__(self):
        self._score_words_by_char_pos_frequency()
        self.words.sort(key=lambda word: word.score, reverse=True)  # optional

    def start(self, top_n: int = 6):
        responses: List[Response] = []

        while(True):
            qualified_words = list(self._get_qualified_words(responses))
            print(f"Recommendations out of {len(qualified_words)}:")
            for i, word in enumerate(qualified_words[0:top_n]):
                print(f"\t{i+1}): {word}")

            choice = input(f'Please choose (1-{top_n}):')
            guess_word = qualified_words[int(choice) - 1]
            colors_input = input('Enter Wordle response:')
            if colors_input == 'ggggg':
                return print("congratulations!!")

            responses.append(Response(guess_word, list(colors_input)))

    def _score_words_by_char_pos_frequency(self):
        char_pos_to_counts: Dict[str, int] = defaultdict(int)
        for word in self.words:
            for pos, char in enumerate(word.chars):
                char_pos_to_counts[f"{char}:{pos}"] += 1

        for word in self.words:
            for pos, char in enumerate(word.chars):
                word.score += char_pos_to_counts[f"{char}:{pos}"]

    def _get_qualified_words(self, responses: List[Response]) -> Iterable[Word]:
        def _is_word_qualified(word: Word) -> bool:
            return all([r.is_word_qualified(word) for r in responses])

        return filter(lambda word: _is_word_qualified(word), self.words)


if __name__ == '__main__':
    WordleSolver().start()
