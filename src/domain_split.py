"""
Contains the split_words() function with logic for splitting a
master word list into many individual lists per word length.
"""

import os
from typing import List


def split_words(path_to_list: str, write_to_files: bool = False) -> List[List[str]]:
    """
    Splits a master word list into separate lists per word length.

    Separated lists can be rewritten to files optionally (outputted to
    resources/generated), though there is currently no functionality to
    automatically leverage these files from within the program.

    Args:
        path_to_list (str): The path to the master word list.
        write_to_files (bool, optional):
            Whether to write the new lists to files
            (in resources/generated). Defaults to False.

    Returns:
        List[List[str]]:
            A list of lists of strings (i.e. a 2D array),
            where the list at index i contains words of length i.
    """
    word_lists = [
        [] for i in range(46)
    ]  # Apparently the longest word in the English dictionary is 45 letters long.

    with open(path_to_list, "r") as file:
        for line in file:
            stripped = line.strip()
            length = len(stripped)
            word_lists[length].append(stripped)

    if write_to_files:
        base_name = os.path.splitext(os.path.basename(path_to_list))[0]
        for i in range(46):
            current_list = word_lists[i]
            if len(current_list) == 0:
                continue

            new_file_path = "resources/generated/" + base_name + f"_len_{i}" + ".txt"
            if not os.path.isfile(new_file_path):
                with open(new_file_path, "w") as new_file:
                    for word in current_list:
                        new_file.write(f"{word}\n")

    return word_lists
