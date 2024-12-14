import argparse
import re
from math import prod

def read(filename:str) -> list:
    robots = []
    with open(filename, mode='r') as f:
        lines = f.readlines()
        for line in lines:
            pattern = r'p=(-*\d+),(-*\d+) v=(-*\d+),(-*\d+)'
            robot = re.search(pattern, line)
            if robot:
                robots.append(((int(robot[1]), int(robot[2])), (int(robot[3]), int(robot[4]))))
        
    return robots


def calculate_end_positions(robots:list, seconds:int , width:int , height:int) -> list:
    """robots:list - position(x,y), velocity(x,y)"""
    final_state = []
    for robot in robots:
        start_x = robot[0][0]
        start_y = robot[0][1]
        vel_x = robot[1][0]
        vel_y = robot[1][1]

        final_x = (start_x + vel_x * seconds) % (width)
        final_y = (start_y + vel_y * seconds) % (height)
        final_state.append((final_x, final_y))

    return final_state

def calculate_safety_factor(end_positions:list, width:int, height:int) -> tuple[int, list]:
    if width % 2 == 0: raise Exception("Grid width must be odd")
    if height % 2 == 0: raise Exception("Grid height must be odd")

    mid_x = int((width+1)/2) - 1
    mid_y = int((height+1)/2) - 1

    quadrant_counts = [0, 0, 0, 0] # top left; top right; bottom right; bottom left

    for position in end_positions:
        if position[0] < mid_x and position[1] < mid_y: # top left
            quadrant_counts[0] += 1
        elif position[0] > mid_x and position[1] < mid_y: # top right
            quadrant_counts[1] += 1
        elif position[0] > mid_x and position[1] > mid_y: # bottom right
            quadrant_counts[2] += 1
        elif position[0] < mid_x and position[1] > mid_y: # bottom left
            quadrant_counts[3] += 1
    
    return (prod(quadrant_counts), quadrant_counts)

def find_christmas_tree(robots:list, seconds:int , width:int , height:int) -> int:
    """Hypothesis: in order for there to be a christmas tree (centered), quadrants 1+4 should have approx. as many robots as 2+3"""
    diff_per_second = []
    for second in range(seconds):
        curr_positions = calculate_end_positions(robots, seconds = second, width = width, height = height)
        safety_factor, quadrants = calculate_safety_factor(curr_positions, width = width, height = height)

        diff_per_second.append(safety_factor)
    return diff_per_second.index(min(diff_per_second))


if __name__  == '__main__':
    file_name = 'input14.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
        width = 11
        height = 7
    else:
        input_name = f'inputs/{file_name}'
        width = 101
        height = 103

    robots = read(input_name)


    end_positions = calculate_end_positions(robots, seconds = 100, width = width, height = height)
    safety_factor, quadrants = calculate_safety_factor(end_positions, width = width, height = height)
    print(f"Part 1: Safety factor = {safety_factor}")

    christmas_tree_after_seconds = find_christmas_tree(robots, seconds = 10403, width = width, height = height)
    print(f"Part 2: Christmas tree (possibly) found after {christmas_tree_after_seconds} seconds")
