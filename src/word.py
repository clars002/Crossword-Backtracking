from __future__ import annotations

from typing import List, Tuple


class Constraint:
    def __init__(self, other_word: Word, index_self: int, index_other: int):
        self.other_word = other_word
        self.index_self = index_self
        self.index_other = index_other

    def __str__(self):
        output = ""
        output += f"Constraint with {self.other_word} w/ self-index {self.index_self} and other-index {self.index_other}"
        return output


class Word:
    def __init__(
        self,
        number: int,
        orientation: bool,  # 0/False = across; 1/True = down
        start_location: Tuple[int, int],
        length: int,
        letters: str = None,
        domain: List[str] = None,
    ):
        self.number = number
        self.orientation = orientation
        self.start_location = start_location
        self.length = length
        self.letters = letters
        self.constraints = []
        self.domain = domain

    def __str__(self):
        output = ""
        if self.orientation:
            orient = "Down"
        else:
            orient = "Across"

        if self.number != 0:
            output += f"{self.number} {orient}: {self.letters} - starting at {self.start_location}; length {self.length}"
        else:
            output += f"[Predetermined]: {self.letters} at {self.start_location}"

        return output
