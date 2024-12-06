import argparse
import re

def read(filename:str) -> str:
    with open(filename, mode='r') as f:
        memory = f.read().strip()
    return memory

def sumAllValidMults(memory:str) -> int:
    valid_mults_re = r'(mul\(([0-9]+),([0-9]+)\))'
    valid_mults = re.findall(valid_mults_re, memory)
    multiplied_mults = [ int(mult[1])*int(mult[2]) for mult in valid_mults ]
    
    return sum(multiplied_mults)

def sumAllEnabledMults(memory:str) -> int:
    valid_instructions_re = r"(mul\(([0-9]+),([0-9]+)\))|(do\(\))|(don't\(\))"
    valid_instructions = re.findall(valid_instructions_re, memory)

    enabled = True
    multiplied_mults = []
    for instruction in valid_instructions:
        if instruction[3] == "do()": enabled = True
        elif instruction[4] == "don't()": enabled = False

        if enabled and instruction[0] != '':
            multiplied_mults.append(int(instruction[1]) * int(instruction[2]))

    return sum(multiplied_mults)

if __name__  == '__main__':
    file_name = 'input3.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    memory = read(input_name)
    
    sum_of_mults = sumAllValidMults(memory)
    print(f"Sum of valid mults: {sum_of_mults}\n")

    sum_of_enabled_mults = sumAllEnabledMults(memory)
    print(f"Sum of enabled mults: {sum_of_enabled_mults}")

    

