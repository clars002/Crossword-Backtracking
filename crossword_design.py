import copy
from typing import List
from word import Word
from puzzle import Puzzle
from typing import List
import domain_split as ds

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