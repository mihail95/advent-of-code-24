class GridSpace:
    """
    Represents a space in a `Grid` object.

    Attributes:
        x (int): The x-coordinate (column) of the grid space.
        y (int): The y-coordinate (row) of the grid space.
        value (str | int): The value stored in the grid space.
        neighbours (list): A list of coordinates for all space neighbours.

    Methods:
        __init__(y: int, x: int, value: str | int)
        set_space_neighbours(grid_dimensions:tuple[int,int])
    """
    def __init__(self, y:int, x:int, value:str|int) -> None:
        """Initializes a new `GridSpace` with the given coordinates and value."""
        self.x = x
        self.y = y
        self.value = value
        self.neighbours:set[tuple[int,int]] = set()

    def set_space_neighbours(self, grid_dimensions:tuple[int,int], diagonal:bool = False) -> None:
        if diagonal:
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,1), (1,-1), (-1,-1)]
        else:
            directions = [(0,1), (0,-1), (1,0), (-1,0)]

        self.neighbours = {(self.y + d_y, self.x + d_x) for (d_x, d_y) in directions if 0 <= self.x + d_x <= grid_dimensions[1] and 0 <= self.y + d_y <= grid_dimensions[0]}

class Grid:
    """
    A class representing a two-dimensional grid of `GridSpace` objects.

    Attributes:
        height (int): The height of the grid (number of rows).
        width (int): The width of the grid (number of columns).
        spaces (dict[tuple[int, int], GridSpace]): A dictionary mapping grid coordinates 
            (row, column) to `GridSpace` objects.

    Methods:
        __init__(dimensions: tuple[int, int]) -> None
        add_grid_space(space: GridSpace) -> None
        print_self() -> None
    """
    def __init__(self, dimensions:tuple[int,int]) -> None:
        """Initializes a new `Grid` object with the specified dimensions."""
        self.height = dimensions[0]
        self.width = dimensions[1]
        self.spaces:dict[tuple[int,int], GridSpace] = {}

    def add_grid_space(self, space:GridSpace) -> None:
        """Adds a `GridSpace` object to the grid at its specified coordinates."""
        self.spaces[(space.y, space.x)] = space

    def print_self(self) -> None:
        """Prints a visual representation of the grid to the console."""
        for row in range(self.height):
            for col in range(self.width):
                print(self.spaces[(row, col)].value, end = "")
            print("\n", end="")
    
    def set_space_neighbours(self, diagonal:bool = False) -> None:
        """Sets the valid neighbours for each space in the grid"""
        for space in self.spaces.values():
            space.set_space_neighbours((self.height-1, self.width-1), diagonal)
