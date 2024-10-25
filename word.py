from typing import Tuple


class Word:
    def __init__(
        self,
        number: int,
        orientation: bool, # 0/False = across; 1/True = down
        start_location: Tuple[int, int],
        length: int,
        letters: str = None,
    ):
        self.number = number
        self.orientation = orientation
        self.start_location = start_location
        self.length = length
        self.letters = letters
    
    def __str__(self):
        output = ""
        if self.orientation:
            orient = "Down"
        else:
            orient = "Across"

        output += f"{self.number} {orient}: {self.letters} - starting at {self.start_location}; length {self.length}"

        return output
