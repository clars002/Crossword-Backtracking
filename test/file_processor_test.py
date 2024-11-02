"""
This is far from any formal or structured test, and is instead where I
manually investigated the behavior of my file_processor code.
"""

import os
import sys

# Following 3 lines were ChatGPT suggested:
current_directory = os.path.dirname(os.path.abspath(__file__))
src_directory = os.path.abspath(os.path.join(current_directory, "../src"))
sys.path.append(src_directory)

import file_processor as fp


def main():
    puzzle_path = "resources/puzzles/heart.txt"

    the_variables = fp.read_variables(puzzle_path)

    for variable in the_variables:
        print(variable)

    fp.generate_constraints(the_variables)


if __name__ == "__main__":
    main()
