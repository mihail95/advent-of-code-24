import argparse
import operator
import itertools

def read(filename:str) -> list:
    equation_list= []
    with open(filename, mode='r') as f:
        for line in f:
            key, values = line.split(":")
            equation_list.append((int(key.strip()), [int(num) for num in values.strip().split(" ")]))
    
    return equation_list

def result_can_be_combination_of_inputs(result:int, numbers:list[int], operator_list:list) -> bool:
    operations_product = [p for p in itertools.product(operator_list, repeat=len(numbers)-1)]
    for op_comb in operations_product:
        temp_result = None
        for idx in range(len(numbers)-1):
            if not temp_result: 
                temp_result = op_comb[idx](numbers[idx], numbers[idx+1])
            else:
                temp_result = op_comb[idx](temp_result, numbers[idx+1])
            
            if temp_result > result:
                break
        
        if temp_result == result: return True

    return False

def get_calibration_score(equation_list:list, operator_list:list) -> int:
    valid_results = []
    for result, numbers in equation_list:
        if result_can_be_combination_of_inputs(result, numbers, operator_list):
            valid_results.append(result)

    return sum(valid_results)

def concat(a:int, b:int) -> int:
    result = str(a) + str(b)
    return int(result)

if __name__  == '__main__':
    file_name = 'input7.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    equation_list = read(input_name)

    calibration_score = get_calibration_score(equation_list, [operator.add, operator.mul])
    print("Calibration Score Part 1:", calibration_score)

    calibration_score = get_calibration_score(equation_list, [operator.add, operator.mul, concat])
    print("Calibration Score Part 2:", calibration_score)


   