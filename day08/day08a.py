import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 08/12 ~~~
""")

with open("input.txt", "r") as file:
    grid = [[char for char in line.strip()] for line in file]

    total_trees_visible = 0
    
    for y, row in enumerate(grid):
        for x, height in enumerate(row):
            total_trees_visible += any([
                all(grid[y][xx] < height for xx in range(0, x)),
                all(grid[y][xx] < height for xx in range(x + 1, len(row))),
                all(grid[yy][x] < height for yy in range(0, y)),
                all(grid[yy][x] < height for yy in range(y + 1, len(grid))),
            ])
            
    print(f"There are {total_trees_visible} trees visible from outside the grid.")
