import domain_split as ds


def main():
    my_words = ds.split_words("docs/Words.txt", True)

    # for i in range(4):
    #     print(f"Words of length {i}:")
    #     print("---------------------------")
    #     for word in my_words[i]:
    #         print(word)


if __name__ == "__main__":
    main()
