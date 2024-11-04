"""
Contains the Visualizer class, used to represent a puzzle visually.
"""

from typing import List

from word import Word


class Visualizer:
    """
    Can generate a visual representation of a puzzle.

    Given a list of assigned variables (i.e. Words with defined
    letters), can create a string representation of the puzzle.

    Attributes:
        assignment (List[Word]): The list of words to be represented.
        rows (int):
            The size of the puzzle in rows (can be discerned
            procedurally from assignment if not explicitly provided)
        columns (int):
            The size of the puzzle in columns (can be discerned
            procedurally from assignment if not explicitly provided)
    """

    def __init__(self, assignment: List[Word] = [], rows: int = 0, columns: int = 0):
        self.assignment = assignment
        self.rows = rows
        self.columns = columns
        self.grid = None

    def create_grid(self):
        """
        Generates a 2D array representation of the puzzle.

        The result is stored in this instance's grid attribute.

        Side effects:
            Assigns the generated 2D array representation of the
            puzzle to this instance's grid attribute.
        """
        # Calculate puzzle width (rows) and height (columns)
        if self.rows < 1 or self.columns < 1:
            for value in self.assignment:
                endpoint = value.length + value.start_location[not value.orientation]

                if value.orientation == 1 and endpoint > self.rows:
                    self.rows = endpoint
                elif value.orientation == 0 and endpoint > self.columns:
                    self.columns = endpoint

        self.grid = [[" "] * self.columns for _ in range(self.rows)]

        for value in self.assignment:

            current_row = value.start_location[0]
            current_col = value.start_location[1]

            if value.orientation == 0:

                def increment_space():
                    nonlocal current_col
                    current_col += 1

            else:

                def increment_space():
                    nonlocal current_row
                    current_row += 1

            for i in range(value.length):
                self.grid[current_row][current_col] = value.letters[i]
                increment_space()

        return

    def __str__(self):
        """
        Outputs the list of variable assignments, then the full puzzle.

        Returns:
            str: The string representation of the puzzle.
        """

        if self.grid == None:
            self.create_grid()

        for word in self.assignment:
            print(word)

        out_string = ""
        divider = "-" * ((len(self.grid[0]) * 4) + 1)
        out_string += divider
        out_string += "\n"
        for row in self.grid:
            for col in row:
                out_string += "| " + col + " "
            out_string += "|"
            out_string += "\n"
            out_string += divider
            out_string += "\n"

        return out_string
