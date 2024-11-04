"""
Contains the Word and Constraint classes.
"""

from __future__ import annotations

from typing import List, Tuple


class Constraint:
    """
    Contains info pertaining to one constraint.

    Takes the perspective of a given Word to whom it's attached.

    Attributes:
        other_word (Word):
            The other word (besides the one to whom this constraint is
            presumably attached) mutually bound by this constraint.
        index_self (int):
            The index of the letter on the first word which overlaps
            with the other word.
        index_other (int):
            The index of the letter on the other word which overlaps
            with the first word.
    """

    def __init__(self, other_word: Word, index_self: int, index_other: int):
        self.other_word = other_word
        self.index_self = index_self
        self.index_other = index_other

    def __str__(self):
        output = ""
        output += f"Constraint with {self.other_word} w/ self-index {self.index_self} and other-index {self.index_other}"
        return output


class Word:
    """
    A single word/variable belonging to a puzzle.

    Attributes:
        number (int): The number assigned to this word in the puzzle.
        orientation (bool):
            The orientation of this word in the puzzle; 0/False
            corresponds to "across", 1/True corresponds to "down".
        start_location (Tuple[int, int]):
            The respective x and y coordinates where this word starts
            in the puzzle.
        length (int): The length of this Word.
        letters (str): The assigned string/letters of this word.
        constraints (List[Constraint]): The constraints this word
        is bound by.
        domain (List[str]):
            The domain of possible assignmetns to this word.
    """

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
