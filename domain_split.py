def split_words(path_to_list: str, write_to_files: bool = False):
    word_lists = [[] for i in range(45)]
                
    with open(path_to_list, "r") as file:
        for line in file:
            stripped = line.strip()
            length = len(stripped)
            word_lists[length].append(stripped)

    # if write_to_files:
    #     for list in word_lists:


    return word_lists
