from word import Word

class Puzzle:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.grid = [[' '] * columns for _ in range(rows)]

    
    def __str__(self):
        out_string = ''
        divider = '-' * ((len(self.grid[0]) * 4) + 1)
        out_string += divider
        out_string += '\n'
        for row in self.grid:
            for col in row:
                out_string += '| ' + col + ' '
            out_string += '|'
            out_string += '\n'
            out_string += divider
            out_string += '\n'
        return out_string

    
    def try_insert(self, value: Word):
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
            if self.grid[current_row][current_col] not in (' ', value.letters[i]):
                return False
            increment_space()

        current_row = value.start_location[0]
        current_col = value.start_location[1]
        
        for i in range(value.length):
            self.grid[current_row][current_col] = value.letters[i]
            increment_space()
        
        
        return True