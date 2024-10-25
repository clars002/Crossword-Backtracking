import copy
from typing import List
from word import Word
from puzzle import Puzzle


def main():
    myPuzzle = Puzzle(6, 5)
    myWord = Word(1, 1, (1, 1), 3, "egg")
    myWord2 = Word(2, 0, (2, 0), 5, "aglet")
    print(myWord.letters)

    print(myPuzzle)

    print(myPuzzle.try_insert(myWord))

    print(myPuzzle)

    print(myPuzzle.try_insert(myWord2))

    print(myPuzzle)


if __name__ == "__main__":
    main()
