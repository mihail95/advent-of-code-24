import argparse
from aoc_helpers import Grid, GridSpace

class Garden(Grid):
    ...

class GardenPlot(GridSpace):
    ...

def read(filename:str) -> Garden:
    with open(filename, mode='r') as f:
        lines = f.readlines()
        first_line = [char for char in lines[0].strip()]
        grid = Garden((len(lines), len(first_line)))
        for row_idx, line in enumerate(lines):
            curr_row = [char for char in line.strip()]
            for col_idx, val in enumerate(curr_row):
                grid.add_grid_space(GardenPlot(y=row_idx, x=col_idx, value=val))
    
    grid.set_space_neighbours(diagonal=False)

    return grid


if __name__  == '__main__':
    file_name = 'input12.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    grid = read(input_name)
    grid.print_self()

    