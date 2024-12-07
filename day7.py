import argparse

def read(filename:str) -> dict:
    equation_dict = {}
    with open(filename, mode='r') as f:
        for line in f:
            key, values = line.split(":")
            if key.strip() in equation_dict: raise Exception("Key already present in dict!")
            equation_dict[int(key.strip())] = [int(num) for num in values.strip().split(" ")]
    
    return equation_dict

if __name__  == '__main__':
    file_name = 'input7.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    equation_dict = read(input_name)
    print(equation_dict)


   