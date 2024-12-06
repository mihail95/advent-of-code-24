import argparse
from enum import Enum
from copy import deepcopy

class Direction(Enum):
    UP = 0 # -y
    RIGHT = 1 # +x
    DOWN = 2 # +y
    LEFT = 3 # -x

def read(filename:str) -> tuple[list[list[str]],tuple[int,int]]:
    grid = []
    guard_start = (0, 0)
    with open(filename, mode='r') as f:
        for idx, line in enumerate(f):
            curr_row = [char for char in line.strip()]
            grid.append(curr_row)
            if "^" in curr_row:
                col = curr_row.index("^")
                guard_start = (idx, col)
    
    return grid, guard_start


def findGuardPath(grid:list[list[str]], guard_start:tuple[int,int]) -> set:
    """Guard actions:
    - If there is something directly in front of you, turn right 90 degrees.
    - Otherwise, take a step forward.
    - Continue until exiting the grid

    Retrun: Distinct visited positions count"""

    direction_changes = 0
    guard_y, guard_x = guard_start
    visited_positions = set()

    while 0 <= guard_y < len(grid) and 0 <= guard_x < len(grid[0]):
        # Look at next space 
        delta_x = 0
        delta_y = 0
        if Direction(direction_changes%len(Direction)) == Direction.UP:
            delta_y = -1
        elif Direction(direction_changes%len(Direction)) == Direction.RIGHT:
            delta_x = 1
        elif Direction(direction_changes%len(Direction)) == Direction.DOWN:
            delta_y = 1
        elif Direction(direction_changes%len(Direction)) == Direction.LEFT:
            delta_x = -1

        next_y, next_x = guard_y + delta_y, guard_x + delta_x
        if 0 <= next_y < len(grid) and 0 <= next_x < len(grid[0]) and grid[next_y][next_x] == '#':
            direction_changes += 1
        else:
            guard_y, guard_x = next_y, next_x
            visited_positions.add((guard_y, guard_x))
    
    return visited_positions

def containsLoop(grid:list[list[str]], guard_start:tuple[int,int]) -> bool:
    direction_changes = 0
    moves = 0
    move_limit = 50000
    limit_reachead = False
    guard_y, guard_x = guard_start

    while 0 <= guard_y < len(grid) and 0 <= guard_x < len(grid[0]):
        if moves >= move_limit:
            limit_reachead = True
            break
        # Look at next space 
        delta_x = 0
        delta_y = 0
        if Direction(direction_changes%len(Direction)) == Direction.UP:
            delta_y = -1
        elif Direction(direction_changes%len(Direction)) == Direction.RIGHT:
            delta_x = 1
        elif Direction(direction_changes%len(Direction)) == Direction.DOWN:
            delta_y = 1
        elif Direction(direction_changes%len(Direction)) == Direction.LEFT:
            delta_x = -1

        next_y, next_x = guard_y + delta_y, guard_x + delta_x
        if 0 <= next_y < len(grid) and 0 <= next_x < len(grid[0]) and grid[next_y][next_x] == '#':
            direction_changes += 1
            moves += 1
        else:
            guard_y, guard_x = next_y, next_x
            moves += 1

    return limit_reachead

def findPossibleLoops(grid:list[list[str]], guard_start:tuple[int,int], guard_path:set) -> int:
    loops_found = 0
    guard_y, guard_x = guard_start
    for point in guard_path:
        if point[0] >= len(grid): continue
        if point[1] >= len(grid[0]): continue
        if grid[point[0]][point[1]] in ['#', '^']: continue
        altered_grid = deepcopy(grid)
        altered_grid[point[0]][point[1]] = '#'
        loops_found += containsLoop(altered_grid, guard_start)

    return loops_found

def print_grid(grid:list) -> None:
    for row in grid:
        for col in row:
            print(col, end = "")
        print("\n", end="")

if __name__  == '__main__':
    file_name = 'input6.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    grid, guard_start = read(input_name)

    visited_spaces = findGuardPath(grid, guard_start)
    print("Visited spaces:", len(visited_spaces))

    loops_found = findPossibleLoops(grid, guard_start, visited_spaces)
    print("Loops found:", loops_found)
   