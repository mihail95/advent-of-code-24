import argparse
from aoc_helpers import Grid, GridSpace, flatten_nested_array

def read(filename:str) -> tuple[Grid, list]:
    with open(filename, mode='r') as f:
        lines = f.readlines()
        first_line = [int(char) for char in lines[0].strip()]
        grid = Grid((len(lines), len(first_line)))
        trailheads = []
        for row_idx, line in enumerate(lines):
            curr_row = [int(char) for char in line.strip()]
            for col_idx, num in enumerate(curr_row):
                grid.add_grid_space(GridSpace(y=row_idx, x=col_idx, value=num))
                if num == 0:
                    trailheads.append((row_idx, col_idx))
    
    grid.set_space_neighbours(diagonal=False)

    return grid, trailheads

def get_valid_trailhead_routes(grid:Grid, trailhead:tuple[int, int], end_node:int) -> list:
    valid_ends = []
    trailhead_value = int(grid.spaces[trailhead].value)
    for neighbour in grid.spaces[trailhead].neighbours:
        neighbour_value = int(grid.spaces[neighbour].value)
        if neighbour_value - trailhead_value == 1:
            if grid.spaces[neighbour].value == end_node:
                valid_ends.append(neighbour)
            else:
                valid_ends.append(get_valid_trailhead_routes(grid, (neighbour[0], neighbour[1]), end_node))
    return valid_ends


def sum_of_valid_trailhead_scores(grid:Grid, trailheads:list[tuple], end_node:int, unique_destination:bool = True) -> int:
    all_trailhead_valid_routes = []
    for trailhead in trailheads:
        current_trailhead_valid_routes = get_valid_trailhead_routes(grid, trailhead, end_node)
        current_trailhead_valid_routes = flatten_nested_array(current_trailhead_valid_routes)
        if unique_destination: current_trailhead_valid_routes = list(set(current_trailhead_valid_routes))
        print(f"Trailhead {trailhead}: {current_trailhead_valid_routes}")
        all_trailhead_valid_routes.append(current_trailhead_valid_routes)

    all_trailhead_valid_routes = flatten_nested_array(all_trailhead_valid_routes)
    return len(all_trailhead_valid_routes)

if __name__  == '__main__':
    file_name = 'input10.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    grid, trailheads = read(input_name)

    trailheads_sum = sum_of_valid_trailhead_scores(grid, trailheads, end_node = 9, unique_destination = True)
    print("Part 1: Sum of unique valid trailhead scores", trailheads_sum)

    trailheads_sum = sum_of_valid_trailhead_scores(grid, trailheads, end_node = 9, unique_destination = False)
    print("Part 2: Sum of all valid trailhead scores", trailheads_sum)
    

