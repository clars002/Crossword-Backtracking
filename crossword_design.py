import copy
from typing import List
from word import Word

def main():
    # 2D array; row 0 is ACROSS, row 1 is DOWN
    assignment = [[None] * 8 for _ in range(2)]
    words = [None] * 5

    words[2] = ['AFT', 'ALE', 'EEL', 'LEE', 'TIE']
    words[3] = ['HEEL', 'HIKE', 'KEEL', 'KNOT', 'LINE']
    words[4] = ['HOSES', 'LASER', 'SAILS', 'SHEET', 'STEER']

    # 2D array; row 0 is ACROSS, row 1 is DOWN
    domains = [[None] * 8 for _ in range(2)]

    domains[0][0] = copy.deepcopy(words[4])
    domains[1][1] = copy.deepcopy(words[4])
    domains[1][2] = copy.deepcopy(words[4])
    domains[0][3] = copy.deepcopy(words[3])
    domains[1][4] = copy.deepcopy(words[3])
    domains[1][5] = copy.deepcopy(words[2])
    domains[0][6] = copy.deepcopy(words[2])
    domains[0][7] = copy.deepcopy(words[4])

    puzzle = [[None] * 5 for _ in range(6)] # ChatGPT


def recursive_backtracking(assignment: List[str], csp):
    if None not in assignment:
        return assignment
    else:
        var_index = select_unassigned_variable(assignment)
        
        for word in domains[var_index[0]][var_index[1]]:
            orientation = ''
            if var_index[0] == 0:
                orientation = 'across'
            else:
                orientation = 'down'
            meets_constraints = try_insert(word, csp, var_index[1], orientation)
            if meets_constraints:
                assignment[i] = word
                result = recursive_backtracking(assignment, csp)
                if result != 'failure':
                    return result
                else:
                    assignment[i] = None
        return 'failure'
    


def select_unassigned_variable(variables):
    for i in range(2):
        for j in range(len(variables[i])):
            if variables[i][j] != None:
                return (i, j)


def try_insert(word, csp, number, orientation):
    if orientation == 'across':



if __name__ == "__main__":
    main()