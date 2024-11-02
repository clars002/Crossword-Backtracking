"""
This is far from any formal or structured test, and is instead where I
manually investigated the behavior of my domain_split code.
"""

import os
import sys

# Following 3 lines were ChatGPT suggested:
current_directory = os.path.dirname(os.path.abspath(__file__))
src_directory = os.path.abspath(os.path.join(current_directory, "../src"))
sys.path.append(src_directory)

import domain_split as ds


def main():
    my_words = ds.split_words("resources/words/words.txt", True)

    for i in range(4):
        print(f"Words of length {i}:")
        print("---------------------------")
        for word in my_words[i]:
            print(word)


if __name__ == "__main__":
    main()
