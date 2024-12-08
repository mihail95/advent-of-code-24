import argparse
import itertools

def read(filename:str) -> tuple[list, dict]:
    grid = []
    node_coords = {}
    with open(filename, mode='r') as f:
        for row_idx, line in enumerate(f):
            curr_row = [char for char in line.strip()]
            grid.append(curr_row)
            for col_idx, char in enumerate(curr_row):
                if char != '.':
                    node_coords.setdefault(char, []).append((row_idx, col_idx))

    return grid, node_coords

def print_grid(grid:list) -> None:
    for row in grid:
        for col in row:
            print(col, end = "")
        print("\n", end="")

def calculate_signal_impact(grid:list, node_coords:dict, extended_mode:bool = False) -> int:
    antinode_locations = set()

    for node_type, all_coords in node_coords.items():
        for node_pair in itertools.combinations(all_coords, 2):
            delta_y = node_pair[0][0] - node_pair[1][0]
            delta_x = node_pair[0][1] - node_pair[1][1]
            seen_nodes = [pair for pair in node_pair]

            for node in node_pair:
                new_node_coords = (node[0] + delta_y, node[1] + delta_x)
                if new_node_coords in node_pair:
                    new_node_coords = (node[0] - delta_y, node[1] - delta_x)
                if extended_mode:
                    while 0 <= new_node_coords[0] < len(grid) and 0 <= new_node_coords[1] < len(grid[0]):
                        antinode_locations.add(new_node_coords)
                        seen_nodes.append(new_node_coords)
                        prev_node_coords = (new_node_coords[0], new_node_coords[1])
                        new_node_coords = (prev_node_coords[0] + delta_y, prev_node_coords[1] + delta_x)
                        if new_node_coords in seen_nodes:
                            new_node_coords = (prev_node_coords[0] - delta_y, prev_node_coords[1] - delta_x)
                else:
                    if 0 <= new_node_coords[0] < len(grid) and 0 <= new_node_coords[1] < len(grid[0]):
                        antinode_locations.add(new_node_coords)
    
    if not extended_mode:
        return len(antinode_locations)
    else:
        unique_start_nodes = set().union(*node_coords.values())
        return len(set().union(antinode_locations, unique_start_nodes))

if __name__  == '__main__':
    file_name = 'input8.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="turns testing mode on", action="store_true")
    args = parser.parse_args()
    if args.test:
        input_name = f'test_inputs/{file_name}'
    else:
        input_name = f'inputs/{file_name}'

    grid, node_coords = read(input_name)

    antinode_locations_count = calculate_signal_impact(grid, node_coords)
    print("Part 1: Unique antinode connections count:", antinode_locations_count)

    extended_locations_count = calculate_signal_impact(grid, node_coords, True)
    print("Part 2: Unique antinode connections count in line:", extended_locations_count)




   