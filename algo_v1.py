from collections import defaultdict
from typing import List, Iterable

from models import Word, Response


class AlgoBase:
    def __init__(self):
        self.responses = []

    def run_cli(self, top_n: int = 6):
        while(True):
            qualified_words = list(self.get_qualified_words())
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
                self.responses.append(response)


class AlgoV1(AlgoBase):
    def __init__(self):
        super().__init__()

        fh = open('wordle-answers-alphabetical.txt', 'r')
        self.words = [Word(list(line.strip())) for line in fh.readlines()]
        self._score_words_by_char_pos_frequency()
        self.words.sort(key=lambda word: word.score, reverse=True)  # optional

    def get_qualified_words(self) -> Iterable[Word]:
        def _is_word_qualified(word: Word) -> bool:

            return all([r.is_word_qualified(word) for r in self.responses])

        return filter(lambda word: _is_word_qualified(word), self.words)

    def _score_words_by_char_pos_frequency(self):
        char_pos_to_counts = defaultdict(int)

        for word in self.words:
            for pos, char in enumerate(word.chars):
                char_pos_to_counts[f"{char}:{pos}"] += 1

        for word in self.words:
            char_to_pos = {char: pos for pos, char in enumerate(word.chars)}
            for char, pos in char_to_pos.items():
                word.score += char_pos_to_counts[f"{char}:{pos}"]


if __name__ == '__main__':
    AlgoV1().run_cli()
