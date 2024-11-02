import argparse
from typing import List

import domain_split as ds
import file_processor as fp
import recursive_backtracker as rb
from visualizer import Visualizer


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_path", type=str, help="Path to the puzzle input file.")
    return parser.parse_args()


def main():
    args = process_args()

    word_list = ds.split_words("resources/words/words.txt")

    variables = fp.read_variables(args.puzzle_path)
    fp.generate_constraints(variables)

    for variable in (v for v in variables if v.letters == None):
        domain_index = variable.length
        variable_domain = word_list[domain_index][:]

        critical_indices = []

        for constraint in variable.constraints:
            critical_index = constraint.index_self
            critical_indices.append(critical_index)

        def evaluate_string(
            s: str, critical_indices: List[int], char_values: List[float]
        ):
            value = 0

            for i in critical_indices:
                critical_char = s[i]
                alpha_position = ord(critical_char) - ord("a")  # ChatGPT line
                value += char_values[alpha_position]

            return value

        sorted_variable_domain = sorted(
            variable_domain,
            key=lambda s: evaluate_string(s, critical_indices, rb.letter_frequencies),
            reverse=True,
        )

        variable.domain = sorted_variable_domain

    print("Finished initializing variables, constraints, and domains.")

    used_values = []

    print("Commencing recursive backtracking. Stand by...")
    solution = rb.recursive_backtracking(variables, used_values)

    if solution != "Failure" and solution != None:
        print("Solution found!")
    else:
        print("Failure! All assignments exhausted, but no solution was found.")
        return

    visualizer = Visualizer(solution)
    print(visualizer)


if __name__ == "__main__":
    main()
