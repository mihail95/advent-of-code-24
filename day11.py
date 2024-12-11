import argparse
from functools import lru_cache

def read(filename:str) -> list:
    with open(filename, mode='r') as f:
        lines = f.readlines()
        first_line = [int(char) for char in lines[0].strip().split()]
    return first_line

@lru_cache(maxsize=4096)
def mutate_stone(value:int) -> int|tuple[int,int]:
    """ - If the stone is 0, replace stone with the number 1.
    - If the stone is number with even number of digits, replace by two stones. 1000 = 10|00 = 10, 0 
    - Else, replace by a new stone = old stone * 2024 """
    if value == 0:
        return 1
    elif (val_len:=len(strval := str(value))) % 2 == 0:
        mid_point = int(val_len/2)
        return (int(strval[:mid_point]), int(strval[mid_point:]))
    else:
        return value * 2024

def blink(state:dict) -> dict:
    new_state = dict()
    for num, ctr in state.items():
        mutated_stone = mutate_stone(num)
        if isinstance(mutated_stone, int):
            new_state[mutated_stone] = new_state.get(mutated_stone, 0) + ctr
        elif isinstance(mutated_stone, list) or isinstance(mutated_stone, tuple):
            new_state[mutated_stone[0]] = new_state.get(mutated_stone[0], 0) + ctr
            new_state[mutated_stone[1]] = new_state.get(mutated_stone[1], 0) + ctr
        else:
            raise Exception("Invalid type of stone returned!")

    return new_state

def calculate_state_after_blinks(initial_state:list, blinks:int) -> int:
    mutated_state = {n: initial_state.count(n) for n in initial_state}
    for _ in range(blinks):
        mutated_state = blink(mutated_state)
    return sum(mutated_state.values())

if __name__  == '__main__':
    file_name = 'input11.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    initial_stones = read(input_name)

    stones_after_25_blinks = calculate_state_after_blinks(initial_stones, blinks=25)
    print("Part 1: Stones after 25 blinks:", stones_after_25_blinks)

    stones_after_75_blinks = calculate_state_after_blinks(initial_stones, blinks=75)
    print("Part 2: Stones after 75 blinks:", stones_after_75_blinks)

    mutate_stone.cache_clear()
    

