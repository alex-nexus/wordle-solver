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

    def __str__(self) -> str:
        return ('').join(self.colors)
