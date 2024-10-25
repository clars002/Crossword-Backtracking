import os

def split_words(path_to_list: str, write_to_files: bool = False):
    word_lists = [[] for i in range(46)] # apparently the longest word in the English dictionary is 45 letters long
                
    with open(path_to_list, "r") as file:
        for line in file:
            stripped = line.strip()
            length = len(stripped)
            word_lists[length].append(stripped)

    
    base_name = os.path.splitext(os.path.basename(path_to_list))[0]

    if write_to_files:
        for i in range(46):
            current_list = word_lists[i]
            if len(current_list) == 0:
                continue

            new_file_path = "docs/generated/" + base_name + f"_len_{i}" + ".txt"
            if not os.path.isfile(new_file_path):
                with open(new_file_path, "w") as new_file:
                    for word in current_list:
                        new_file.write(f"{word}\n")

    return word_lists
