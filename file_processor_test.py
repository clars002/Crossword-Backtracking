import file_processor as fp

def main():
    puzzle_path = "docs/puzzle3.txt"

    the_variables = fp.read_variables(puzzle_path)

    for variable in the_variables:
        print(variable)


if __name__ == "__main__":
    main()