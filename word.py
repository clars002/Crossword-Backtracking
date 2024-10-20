from typing import Tuple

class Word:
    def __init__(self, number: int, orientation: bool, start_location: Tuple[int, int], length: int, letters: str):
        self.number = number
        self.orientation = orientation
        self.start_location = start_location
        self.length = length
        self.letters = letters

    