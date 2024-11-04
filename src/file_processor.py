"""
Logic for reading variable info from file & procedural constraints.
"""

import re
from typing import List

from word import Constraint, Word


def read_variables(filepath: str) -> List[Word]:
    """
    Generates a list of Word objects from a file specifying them.

    The file provides number, orientation, starting coordinates, and
    length for each variable and Word objects are generated to match
    (with unassigned letters).

    Args:
        filepath (str):
            Path to the file containing the list of variables.

    Returns:
        List[Word]:
            A list containing all the variables generated from the file
            (i.e. Word objects with unassigned letters).
    """
    variables = []
    with open(filepath) as variable_file:
        # Two modes, "Variables" for regular variables and "Letters"
        # for predetermined letters such as the N, T, and H on
        # the heart puzzle.
        mode = "Variables"

        for line in variable_file:
            if line[0] in (" ", "\n"):
                continue

            # Use regex to check if this line specifies a mode and
            # change modes if so.
            title_match = re.search(r"\[(\w+)\]", line)  # ChatGPT line
            if title_match:
                title = title_match.group(1)
                if title == "Letters":
                    mode = "Letters"
                else:
                    mode = "Variables"
                continue

            # Split the current line by comma
            char_params = line.strip().split(",")
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

        # Sort primarily by orientation, secondarily by number
        sorted_variables = sorted(
            variables, key=lambda var: (var.orientation, var.number)
        )

    return sorted_variables


def generate_constraints(variables: List[Word]):
    """
    Procedurally generates constraints for each variable.

    Leverages known length and position data for each variable to
    discern where overlaps occur and generates corresponding
    constraints which are then assigned to each respective variable.

    Args:
        variables (List[Word]):
            The list of words whose constraints will be populated

    Side effects:
        Each variable will have its constraints member populated based
        on procedural generation.
    """
    rows = 0
    columns = 0

    # Discern the number of rows and columns of the puzzle:
    for value in variables:
        endpoint = value.length + value.start_location[not value.orientation]

        if value.orientation == 1 and endpoint > rows:
            rows = endpoint
        elif value.orientation == 0 and endpoint > columns:
            columns = endpoint

    # A 3D array; each row/column coordinate contains a list,
    # which will be populated with all variables that occupy that space
    grid = [[[] for _ in range(columns)] for _ in range(rows)]  # ChatGPT line; 3D array

    # Populate the 3D array
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
            # Add a tuple; the variable occupying this space is
            # needed, and so is the index at which it overlaps this
            # space.
            grid[current_row][current_col].append((variable, i))
            increment_space()

    # Generate respective constraints wherever a single coordinate
    # contains two distinct variables:
    for i in range(rows):
        for j in range(columns):
            coordinate_occupants = grid[i][j]

            if len(coordinate_occupants) > 1:
                first_occupant_tuple = coordinate_occupants[0]
                second_occupant_tuple = coordinate_occupants[1]

                constraint_a = Constraint(
                    second_occupant_tuple[0],
                    first_occupant_tuple[1],
                    second_occupant_tuple[1],
                )
                constraint_b = Constraint(
                    first_occupant_tuple[0],
                    second_occupant_tuple[1],
                    first_occupant_tuple[1],
                )

                first_occupant_tuple[0].constraints.append(constraint_a)
                second_occupant_tuple[0].constraints.append(constraint_b)

    return
