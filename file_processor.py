from word import Word

def read_variables(filepath: str):
    variables = []
    with open(filepath) as variable_file:
        for line in variable_file:
            if line[0] == '[':
                continue
            
            params = line.strip().split(',')
            print(params)
            start_loc = (params[2], params[3])

            new_variable = Word(params[0], params[1], start_loc, params[4])

            variables.append(new_variable)
    
    return variables