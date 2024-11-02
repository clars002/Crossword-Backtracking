import copy
from typing import List

import domain_split as ds
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


def main():
    the_puzzle = Puzzle(11, 12)

    word_list = ds.split_words("docs/Words.txt")

    variables = [None] * 12

    variables[0] = Word(1, 0, (0, 2), 7)
    variables[1] = Word(2, 1, (0, 8), 4)
    variables[2] = Word(3, 1, (1, 11), 6)
    variables[3] = Word(4, 0, (3, 5), 5)
    variables[4] = Word(5, 1, (3, 7), 6)
    variables[5] = Word(6, 1, (5, 4), 6)
    variables[6] = Word(7, 0, (5, 7), 5)
    variables[7] = Word(8, 1, (5, 9), 6)
    variables[8] = Word(9, 1, (7, 1), 4)
    variables[9] = Word(10, 0, (7, 3), 5)
    variables[10] = Word(11, 0, (9, 0), 6)
    variables[11] = Word(1, 1, (0, 2), 5)

    constraint_0 = Constraint(variables[1], 6, 0)
    constraint_1 = Constraint(variables[0], 0, 6)
    constraint_1_1 = Constraint(variables[3], 3, 3)
    constraint_3 = Constraint(variables[1], 3, 3)
    constraint_3_4 = Constraint(variables[4], 2, 0)
    constraint_4 = Constraint(variables[3], 0, 2)
    constraint_6_4 = Constraint(variables[4], 0, 2)
    constraint_4_6 = Constraint(variables[6], 2, 0)
    constraint_6_2 = Constraint(variables[2], 4, 4)
    constraint_2_6 = Constraint(variables[6], 4, 4)
    constraint_7_6 = Constraint(variables[6], 0, 2)
    constraint_6_7 = Constraint(variables[7], 2, 0)
    constraint_9_5 = Constraint(variables[5], 1, 2)
    constraint_5_9 = Constraint(variables[9], 2, 1)
    constraint_9_4 = Constraint(variables[4], 4, 4)
    constraint_4_9 = Constraint(variables[9], 4, 4)
    constraint_10_8 = Constraint(variables[8], 1, 2)
    constraint_8_10 = Constraint(variables[10], 2, 1)
    constraint_10_5 = Constraint(variables[5], 4, 4)
    constraint_5_10 = Constraint(variables[10], 4, 4)
    constraint_11_0 = Constraint(variables[0], 0, 0)
    constraint_0_11 = Constraint(variables[11], 0, 0)

    variables[0].constraints.append(constraint_0)
    variables[1].constraints.append(constraint_1)
    variables[1].constraints.append(constraint_1_1)
    variables[3].constraints.append(constraint_3)
    variables[4].constraints.append(constraint_4)
    variables[3].constraints.append(constraint_3_4)
    variables[6].constraints.append(constraint_6_4)
    variables[4].constraints.append(constraint_4_6)
    variables[6].constraints.append(constraint_6_2)
    variables[2].constraints.append(constraint_2_6)
    variables[7].constraints.append(constraint_7_6)
    variables[6].constraints.append(constraint_6_7)
    variables[9].constraints.append(constraint_9_5)
    variables[5].constraints.append(constraint_5_9)
    variables[9].constraints.append(constraint_9_4)
    variables[4].constraints.append(constraint_4_9)
    variables[10].constraints.append(constraint_10_8)
    variables[8].constraints.append(constraint_8_10)
    variables[10].constraints.append(constraint_10_5)
    variables[5].constraints.append(constraint_5_10)
    variables[11].constraints.append(constraint_11_0)
    variables[0].constraints.append(constraint_0_11)

    for variable in variables:
        domain_index = variable.length
        variable_domain = word_list[domain_index][:]

        critical_indices = []

        for constraint in variable.constraints:
            critical_index = constraint.index_self
            critical_indices.append(critical_index)

        # print(f"Critical indices for {variable}: {critical_indices}")

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

        # print(f"The 10 highest scoring words in the domain of {variable}")
        # print("-------------------------------------------------------------------------")
        # for string in variable.domain[:10]:
        #     print(string)

    print("Finished initializing variables, constraints, and domains.")

    used_values = []

    print("Commencing recursive backtracking. Stand by...")
    solution = recursive_backtracking(variables, used_values)

    if solution != "Failure" and solution != None:
        print("Solution found!")
    else:
        print("Failed. Uh oh...")
        return

    visualizer = Visualizer(solution, 11, 12)
    print(visualizer)

    # for word in solution:
    #     print(word)

    # for word in word_list[0]:
    #     print(word)


# def recursive_backtracking(assignment: List[Word], puzzle: Puzzle, word_list: List[List[Word]]):
#     if is_complete(assignment):
#         return assignment

#     var = first_unassigned(assignment)
#     domain_index = var.length
#     # print(f"DOMAIN INDEX: {domain_index}")
#     for value in [v for v in word_list[domain_index] if v not in word_list[0]]:
#         var.letters = value
#         if puzzle.try_insert(var):
#             word_list[0].append(value)
#             result = recursive_backtracking(assignment, puzzle, word_list)
#             if result != "Failure":
#                 return result
#             word_list[0].remove(value)
#             puzzle.remove(var)
#             var.letters = None
#     var.letters = None
#     return "Failure"


def recursive_backtracking(assignment: List[Word], used_values: List[str]):
    if is_complete(assignment):
        return assignment

    var = minimum_remaining_values(assignment)

    for value in (v for v in var.domain if v not in used_values):  # ChatGPT line
        # print(f"Current value: {value}")
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
                        print("Forward looking has detected a dead end; avoiding it.")
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


def satisfies_constraints(value: str, variable: Word):
    for constraint in variable.constraints:
        other_value = constraint.other_word.letters
        if (
            other_value != None
            and value[constraint.index_self] != other_value[constraint.index_other]
        ):
            return False
    return True


def update_other_domain(value: str, constraint: Constraint):
    other_word = constraint.other_word
    old_domain = other_word.domain
    critical_index = constraint.index_other
    critical_char = value[constraint.index_self]

    # print(f"Length before: {len(old_domain)}")

    new_domain = [
        value for value in old_domain if value[critical_index] == critical_char
    ]

    # print(f"Length after: {len(new_domain)}")

    return new_domain


def is_complete(assignment: List[Word]):
    for word in assignment:
        if word.letters == None:
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


if __name__ == "__main__":
    main()
