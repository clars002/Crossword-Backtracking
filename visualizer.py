from typing import List
from word import Word

class Visualizer:
    def __init__(self, assignment: List[Word] = [], rows: int = 0, columns: int = 0):
        self.assignment = assignment
        self.rows = rows
        self.columns = columns
        self.grid = None

    def create_grid(self):
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
        
    
    def __str__(self):
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