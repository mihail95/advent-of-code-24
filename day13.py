import argparse
import re
import numpy as np

def read(filename:str) -> list:
    machines = []
    current_machine = {"A": '', "B": '', "prize": ''}
    with open(filename, mode='r') as f:
        lines = f.readlines()
        #first_line = [char for char in lines[0].strip()]
        for line in lines:
            re_match = ''
            if line == "\n":
                machines.append(current_machine)
                current_machine = {"A": '', "B": '', "prize": ''}
                continue
            if "Button A:" in line:
                key = "A"
                re_match = r'X\+(\d+), Y\+(\d+)'
            elif "Button B:" in line:
                key = "B"
                re_match = r'X\+(\d+), Y\+(\d+)'
            elif "Prize:" in line:
                key = "prize"
                re_match = r'X=(\d+), Y=(\d+)'
            
            re_found = re.search(re_match, line)
            if re_found is not None:
                current_machine[key] = (int(re_found[1]), int(re_found[2])) # type: ignore

    machines.append(current_machine)
    return machines

def _is_round_integer(array, tolerance=1e-3):
    return np.all(np.isclose(array, np.round(array), atol=tolerance))

def find_minimal_amount_of_tokens(machines:list) -> int:
    total_costs = []
    for machine in machines:
        a=[[machine['A'][0], machine['B'][0]],[machine['A'][1],machine['B'][1]]]
        b=[machine['prize'][0],machine['prize'][1]]
        res = np.linalg.lstsq(a,b)
        if 0 <= int(np.round(res[0][0], 0)) and 0 <= int(np.round(res[0][1], 0)) and _is_round_integer(res[0]):
            total_costs.append(int(np.round(res[0][0], 0))*3 + int(np.round(res[0][1], 0)))

    return sum(total_costs)

def find_corrected_amount_of_tokens(machines:list) -> int|None:
    total_costs = []
    added = 10000000000000
    for machine in machines:
        a = np.array([[machine['A'][0], machine['B'][0]],[machine['A'][1],machine['B'][1]]]).astype(int)
        b = np.array([machine['prize'][0]+added,machine['prize'][1]+added]).astype(int)
        s = np.linalg.solve(a, b)

        if np.all(np.abs(s - np.round(s)) < 1e-3):
            total_costs.append(s[0] * 3 + s[1] * 1)
            
    return sum(total_costs)

if __name__  == '__main__':
    file_name = 'input13.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    machines = read(input_name)
    
    min_tokens_count = find_minimal_amount_of_tokens(machines)
    print(f"Part 1: The minimum amount of tokens needed is {min_tokens_count}")

    corrected_tokens_count = find_corrected_amount_of_tokens(machines)
    print(f"Part 2: The corrected amount of tokens needed is {corrected_tokens_count}")


    