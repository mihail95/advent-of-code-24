import argparse
from aoc_helpers import Grid, GridSpace


class GardenPlot(GridSpace):
    def set_plant_region_index(self, index:int) -> None:
        self.region_idx = index

class Garden(Grid[GardenPlot]):
    def find_plant_regions(self) -> None:
        self.regions:dict[str|int, list[list[tuple[int,int]]]] = dict()
        for coords, space in self.spaces.items():
            if space.value not in self.regions.keys():
                self.regions[space.value] = [[coords]]
                space.set_plant_region_index(0)
            else:
                for idx, group in enumerate(self.regions[space.value]):
                    if any([n in group for n in space.neighbours]):
                        if not hasattr(space, 'region_idx'):
                            self.regions[space.value][idx].append(coords)
                            space.set_plant_region_index(idx)
                            break
                if not hasattr(space, 'region_idx'):
                    self.regions[space.value].append([coords])
                    space.set_plant_region_index(len(self.regions[space.value])-1)
        self.merge_touching_plots()
    
    def merge_touching_plots(self):
        def _are_touching(coord1, coord2):
            return (abs(coord1[0] - coord2[0]) == 1 and coord1[1] == coord2[1]) or (abs(coord1[1] - coord2[1]) == 1 and coord1[0] == coord2[0])

        def _find_connected_component(plot):
            visited = set()
            merged = []
            
            for coord in plot:
                if coord not in visited:
                    stack, component = [coord], set()
                    while stack:
                        c = stack.pop()
                        if c not in visited:
                            visited.add(c)
                            component.add(c)
                            stack.extend(n for n in plot if n not in visited and _are_touching(c, n))
                    merged.append(list(component))
            return merged

        for key in self.regions:
            flattened_plot = {coord for group in self.regions[key] for coord in group}
            self.regions[key] = _find_connected_component(flattened_plot)


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
    grid.find_plant_regions()

    return grid

def calculate_total_fencing_price(grid:Garden) -> int:
    region_costs = []
    for region_type in grid.regions:
        for region in grid.regions[region_type]:
            region_area = len(region)
            region_perimeter = 0
            for plot in region:
                neighbours_in_region = [n for n in grid.spaces[plot].neighbours if n in region]
                region_perimeter += 4 - len(neighbours_in_region)
            region_costs.append(region_area*region_perimeter)
    
    return sum(region_costs)


def calculate_reduced_fencing_price(grid:Garden) -> int:
    region_costs = []
    for region_type in grid.regions:
        for region in grid.regions[region_type]:
            region_area = len(region)
            region_corners = 0
            for plot in region:
                plot_corners = 0
                left = (plot[0], plot[1] - 1)
                right = (plot[0], plot[1] + 1)
                up = (plot[0] + 1, plot[1])
                down = (plot[0] - 1, plot[1])
                down_left = (plot[0] - 1, plot[1] - 1)
                down_right = (plot[0] - 1, plot[1] + 1)
                up_left = (plot[0] + 1, plot[1] - 1)
                up_right = (plot[0] + 1, plot[1] + 1)

                if left not in region and up not in region:
                    plot_corners += 1
                if right not in region and up not in region:
                    plot_corners += 1
                if left not in region and down not in region:
                    plot_corners += 1
                if right not in region and down not in region:
                    plot_corners += 1
                if down_left in region and down not in region:
                    if left in region:
                        plot_corners += 1
                if down_right in region and down not in region:
                    if right in region:
                        plot_corners += 1
                if up_left in region and up not in region:
                    if left in region:
                        plot_corners += 1
                if up_right in region and up not in region:
                    if right in region:
                        plot_corners += 1
                region_corners += plot_corners
            region_costs.append(region_area*region_corners)
    
    return sum(region_costs)

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
    total_fencing_price = calculate_total_fencing_price(grid)
    print(f"Part 1: Total fencing price: {total_fencing_price}")

    reduced_fencing_price = calculate_reduced_fencing_price(grid)
    print(f"Part 2: Reduced fencing price: {reduced_fencing_price}")

    