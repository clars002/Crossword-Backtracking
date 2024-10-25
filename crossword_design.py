import copy
from typing import List
from word import Word
from puzzle import Puzzle
from typing import List

def main():
    the_puzzle = Puzzle(6,5)

    word_list = [None] * 6
    word_list[0] = [] # used words

    word_list[3] = ["AFT", "ALE", "EEL", "LEE", "TIE"]
    word_list[4] = ["HEEL", "HIKE", "KEEL", "KNOT", "LINE"]
    word_list[5] = ["HOSES", "LASER", "SAILS", "SHEET", "STEER"]

    variables = [None] * 8
    variables[0] = Word(1, 0, (0, 0), 5)
    variables[1] = Word(2, 1, (0, 2), 5)
    variables[2] = Word(3, 1, (0, 4), 5)
    variables[3] = Word(4, 0, (2, 1), 4)
    variables[4] = Word(5, 1, (2, 3), 4)
    variables[5] = Word(6, 1, (3, 0), 3)
    variables[6] = Word(7, 0, (3, 2), 3)
    variables[7] = Word(8, 0, (4, 0), 5)

    solution = recursive_backtracking(variables, the_puzzle, word_list)

    if solution != "Failure":
        print("Solution found!")
    else:
        print("Failed. Uh oh...")
        return

    print(the_puzzle)

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