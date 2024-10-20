import copy
from typing import List
from word import Word
from puzzle import Puzzle

def main():
    myPuzzle = Puzzle(6, 5)
    myWord = Word(1, 1, (2,2), 3, 'egg')
    print(myWord.letters)

    print(myPuzzle)

    print(myPuzzle.try_insert(myWord))

    print(myPuzzle)




if __name__ == "__main__":
    main()