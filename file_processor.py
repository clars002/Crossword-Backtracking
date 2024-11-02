from word import Word, Constraint
from typing import List
import re

def read_variables(filepath: str):
    variables = []
    with open(filepath) as variable_file:
        mode = "Variables"

        for line in variable_file:
            if line[0] in (" ", "\n"):
                continue
        
            title_match = re.search(r'\[(\w+)\]', line)
            if title_match:
                title = title_match.group(1)
                if title == "Letters":
                    mode = "Letters"
                else:
                    mode = "Variables"
                continue
            
            char_params = line.strip().split(',')
            params = []

            if mode == "Variables":
                for char in char_params:
                    params.append(int(char))


                start_loc = (params[2], params[3])

                new_variable = Word(params[0], params[1], start_loc, params[4])
            
            elif mode == "Letters":
                start_loc = (int(char_params[0]), int(char_params[1]))
                
                new_variable = Word(0, 0, start_loc, 1, char_params[2])

            
            variables.append(new_variable)


        sorted_variables = sorted(variables, key=lambda var: (var.number, var.orientation))
    
    return sorted_variables


def generate_constraints(variables: List[Word]):
    rows = 0
    columns = 0

    for value in variables:
        endpoint = value.length + value.start_location[not value.orientation]

        if value.orientation == 1 and endpoint > rows:
            rows = endpoint
        elif value.orientation == 0 and endpoint > columns:
            columns = endpoint

    grid = [[[] for _ in range(columns)] for _ in range(rows)] # ChatGPT line; 3D array

    for variable in variables:

        current_row = variable.start_location[0]
        current_col = variable.start_location[1]

        if variable.orientation == 0:

            def increment_space():
                nonlocal current_col
                current_col += 1

        else:

            def increment_space():
                nonlocal current_row
                current_row += 1
    
        for i in range(variable.length):
            grid[current_row][current_col].append((variable, i))
            increment_space()

    for i in range(rows):
        for j in range(columns):
            if len(grid[i][j]) > 1:
                constraint_a = Constraint(grid[i][j][1][0], grid[i][j][0][1], grid[i][j][1][1])
                constraint_b = Constraint(grid[i][j][0][0], grid[i][j][1][1], grid[i][j][0][1])

                grid[i][j][0][0].constraints.append(constraint_a)
                grid[i][j][1][0].constraints.append(constraint_b)

    
    # for variable in variables:
    #     print(f"Variable {variable} has the following constraints:")
    #     print(f"-------------------------------------------------------------------------")

    #     for constraint in variable.constraints:
    #         print(constraint)
        
    #     print("--------------------------------------------------------------------------")
    #     print("")
    
    # for row in grid:
    #     for col in row:
    #         print("[", end="")
    #         for word in col:
    #             orientation_letter = ""
    #             if word.orientation == 0:
    #                 orientation_letter = "a"
    #             else:
    #                 orientation_letter = "d"
                
    #             print(f"{word.number}{orientation_letter},", end="")
    #         print("]", end="")
    #     print("")

    return