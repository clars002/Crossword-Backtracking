import copy
from typing import List
from word import Word, Constraint
from puzzle import Puzzle
from typing import List
import domain_split as ds
from visualizer import Visualizer

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
    constraint_11_1 = Constraint(variables[1], 0, 0)
    constraint_1_11 = Constraint(variables[1], 0, 0)

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

    for variable in variables:
        domain_index = variable.length
        variable.domain = copy.deepcopy(word_list[domain_index])

    used_values = []

    solution = recursive_backtracking_2(variables, used_values)

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
    

def recursive_backtracking(assignment: List[Word], puzzle: Puzzle, word_list: List[List[Word]]):
    if is_complete(assignment):
        return assignment
    
    var = select_unassigned_variable(assignment)
    domain_index = var.length
    # print(f"DOMAIN INDEX: {domain_index}")
    for value in [v for v in word_list[domain_index] if v not in word_list[0]]:
        var.letters = value
        if puzzle.try_insert(var):
            word_list[0].append(value)
            result = recursive_backtracking(assignment, puzzle, word_list)
            if result != "Failure":
                return result
            word_list[0].remove(value)
            puzzle.remove(var)
            var.letters = None
    var.letters = None
    return "Failure"


def recursive_backtracking_2(assignment: List[Word], used_values: List[str]):
    if is_complete(assignment):
        return assignment

    var = select_unassigned_variable(assignment)
    
    for value in (v for v in var.domain if v not in used_values): # ChatGPT line
        # print(f"Current value: {value}")
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
                        # print("Forward looking has detected a dead end; avoiding it.")
                        break

            var.letters = value
            used_values.append(value)

            for word, new_domain in new_domains:
                word.domain = new_domain         

            result = recursive_backtracking_2(assignment, used_values)
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
        if other_value != None and value[constraint.index_self] != other_value[constraint.index_other]:
            return False
    return True


def update_other_domain(value: str, constraint: Constraint):
    other_word = constraint.other_word
    old_domain = other_word.domain
    critical_index = constraint.index_other
    critical_char = value[constraint.index_self]

    # print(f"Length before: {len(old_domain)}")

    new_domain = [value for value in old_domain if value[critical_index] == critical_char]

    # print(f"Length after: {len(new_domain)}")

    return new_domain


def is_complete(assignment: List[Word]):
    for word in assignment:
        if word.letters == None:
            return False
    return True


def select_unassigned_variable(assignment: List[Word]):
    for word in assignment:
        if word.letters == None:
            return word
    return None


if __name__ == "__main__":
    main()