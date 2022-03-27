from dataclasses import dataclass, field
from typing import List


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
    colors: List[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        return (all([c in self.ALLOWED_COLORS for c in self.colors])
                and len(self.colors) == 5)

    def is_game_over(self) -> bool:
        return set(self.colors) == {'g'}

    def _is_word_qualified(self, word: Word) -> bool:
        for pos, (char, color) in enumerate(zip(self.word.chars, self.colors)):
            if color == 'b' and char in word.chars:
                return False

            if color == 'y' and (char not in word.chars or word.chars[pos] == char):
                return False

            # the following commented out codes seems unnecessary since
            # we already know the exact green location, we can actually use the
            # space to explore other possibilities
            # if color == 'g' and word.chars[pos] != char:
            #     return False

        return True

    def __str__(self) -> str:
        return ('').join(self.colors)
