import argparse
import copy
import random as rand
from typing import List

import domain_split as ds
import file_processor as fp
from puzzle import Puzzle
from visualizer import Visualizer
from word import Constraint, Word

letter_frequencies = [
    43.31,
    10.56,
    23.14,
    17.25,
    56.88,
    9.24,
    12.59,
    15.31,
    38.45,
    1.00,
    5.61,
    27.98,
    15.36,
    33.92,
    36.51,
    16.14,
    1.00,
    38.64,
    29.23,
    35.43,
    18.51,
    5.13,
    6.57,
    1.48,
    9.06,
    1.39,
]


def is_complete(assignment: List[Word]):
    for word in assignment:
        if word.letters == None:
            return False
    return True


def satisfies_constraints(value: str, variable: Word):
    for constraint in variable.constraints:
        other_value = constraint.other_word.letters
        if (
            other_value != None
            and value[constraint.index_self] != other_value[constraint.index_other]
        ):
            return False
    return True


def first_unassigned(assignment: List[Word]):
    for word in assignment:
        if word.letters == None:
            return word
    return None


def minimum_remaining_values(assignment: List[Word]):
    minimum_remaining = -1
    selection = None

    for word in (w for w in assignment if w.letters == None):
        remaining = len(word.domain)
        if minimum_remaining == -1 or remaining < minimum_remaining:
            minimum_remaining = remaining
            selection = word

    return selection


def degree_heuristic(assignment: List[Word]):
    most_constraints = -1
    selection = None

    for word in (w for w in assignment if w.letters == None):
        constraint_count = len(word.constraints)
        if constraint_count > most_constraints:
            most_constraints = constraint_count
            selection = word

    return selection


def minimum_remaining_and_degree(assignment: List[Word]):
    minimum_remaining = -1
    selection = []

    for word in (w for w in assignment if w.letters == None):
        remaining = len(word.domain)
        if minimum_remaining == -1 or remaining < minimum_remaining:
            minimum_remaining = remaining

    for word in (w for w in assignment if w.letters == None):
        remaining = len(word.domain)
        if remaining == minimum_remaining:
            selection.append(word)

    most_constraints = -1
    final_choice = None

    for choice in selection:
        constraint_count = len(choice.constraints)
        if constraint_count > most_constraints:
            most_constraints = constraint_count
            final_choice = choice

    return final_choice


def update_other_domain(value: str, constraint: Constraint):
    other_word = constraint.other_word
    old_domain = other_word.domain
    critical_index = constraint.index_other
    critical_char = value[constraint.index_self]

    new_domain = [
        value for value in old_domain if value[critical_index] == critical_char
    ]

    return new_domain


def recursive_backtracking(assignment: List[Word], used_values: List[str]):
    if is_complete(assignment):
        return assignment

    var = minimum_remaining_values(assignment)

    for value in (v for v in var.domain if v not in used_values):  # ChatGPT line
        dead_end = False

        if satisfies_constraints(value, var):
            old_domains = []
            new_domains = []
            for constraint in var.constraints:
                other_word = constraint.other_word
                if constraint.other_word.letters == None:
                    updated_domain = update_other_domain(value, constraint)
                    old_domains.append((other_word, other_word.domain))
                    if len(updated_domain) != 0:
                        new_domains.append((other_word, updated_domain))
                    else:
                        dead_end = True
                        # print("Forward looking has detected a dead end; avoiding it.")
                        break  # Breaks out of the for constraint loop (only) (I think)

            if not dead_end:
                var.letters = value
                used_values.append(value)

                for word, new_domain in new_domains:
                    word.domain = new_domain

                result = recursive_backtracking(assignment, used_values)
                if result != None:
                    return result

                var.letters = None
                used_values.remove(value)

                for word, old_domain in old_domains:
                    word.domain = old_domain

    return None


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('puzzle_path', type=str, help='Path to the puzzle input file.')
    return parser.parse_args()


def main():
    args = process_args()

    the_puzzle = Puzzle(11, 12)

    word_list = ds.split_words("docs/words/words.txt")

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
            key=lambda s: evaluate_string(s, critical_indices, letter_frequencies),
            reverse=True,
        )

        variable.domain = sorted_variable_domain

    print("Finished initializing variables, constraints, and domains.")

    used_values = []

    print("Commencing recursive backtracking. Stand by...")
    solution = recursive_backtracking(variables, used_values)

    if solution != "Failure" and solution != None:
        print("Solution found!")
    else:
        print("Failure! All assignments exhausted, but no solution was found.")
        return

    visualizer = Visualizer(solution)
    print(visualizer)


if __name__ == "__main__":
    main()
