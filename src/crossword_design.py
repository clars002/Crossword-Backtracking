import argparse
from typing import List

import domain_split as ds
import file_processor as fp
import recursive_backtracker as rb
from recursive_backtracker import RecursiveBacktracker
from visualizer import Visualizer


# ChatGPT Note: I learned how to use argparse with its help but wrote the code myself.
def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--puzzle",
        type=str,
        default="resources/puzzles/heart.txt",
        help="Path to the puzzle input file.",
    )
    parser.add_argument(
        "--words",
        type=str,
        default="resources/words/words.txt",
        help="Path to the list of words.",
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        default="mrv",
        help="Specify variable selection heuristic (mrv, degree, mrv+degree, first_unassigned)",
    )
    parser.add_argument(
        "--disable_forward_check",
        action="store_false",
        help="Disable forward checking (enabled by default).",
    )
    parser.add_argument(
        "--sort_domains",
        action="store_true",
        help="Enable sorting variable domains based on letter frequency analysis.",
    )
    parser.add_argument(
        "--show_stats",
        action="store_true",
        help="Enable display of additional stats after a solution is found.",
    )
    return parser.parse_args()


def main():
    args = process_args()

    word_list = ds.split_words(args.words)
    variables = fp.read_variables(args.puzzle)
    fp.generate_constraints(variables)

    backtracker = RecursiveBacktracker(args.heuristic, args.disable_forward_check)

    for variable in (v for v in variables if v.letters == None):
        domain_index = variable.length
        variable.domain = word_list[domain_index][:]

        if args.sort_domains:
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

            variable.domain.sort(
                key=lambda s: evaluate_string(
                    s, critical_indices, rb.letter_frequencies
                ),
                reverse=True,
            )

    print("Finished initializing variables, constraints, and domains.")

    used_values = []

    print("Commencing recursive backtracking. Stand by...")
    solution = backtracker.recursive_backtracking(variables, used_values)

    if solution != "Failure" and solution != None:
        print("Solution found!")
    else:
        print("Failure! All assignments exhausted, but no solution was found.")
        return

    visualizer = Visualizer(solution)
    print(visualizer)


if __name__ == "__main__":
    main()
