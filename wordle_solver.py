from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Iterable


@dataclass
class Word:
    chars: List[str]
    score: int = field(default_factory=lambda: 0)

    def __str__(self) -> str:
        return ('').join(self.chars)


@dataclass
class Response:
    ALLOWED_COLORS = ['b', 'g', 'y']

    word: Word
    colors: List[str]

    def is_valid(self) -> bool:
        return (all([c in self.ALLOWED_COLORS for c in self.colors])
                and len(self.colors) == 5)

    def is_game_over(self) -> bool:
        return set(self.colors) == {'g'}

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

            choice = int(input(f'Please choose (1-{top_n}):').strip())
            colors = list(input('Enter Wordle response:'))

            response = Response(qualified_words[choice - 1], colors)
            if not response.is_valid():
                print("\tRESPONSE INVALID. Please try again\n")
            elif response.is_game_over():
                return print("Game Over! Congratulations!!")
            else:
                responses.append(response)

    def _score_words_by_char_pos_frequency(self):
        char_pos_to_counts = defaultdict(int)

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
