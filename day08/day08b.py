import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

with open("input.txt", "r") as file:
    grid = [[char for char in line.strip()] for line in file]

    best_scenic_score_so_far = 0
    
    for y, row in enumerate(grid):
        for x, height in enumerate(row):
            scores = [0, 0, 0, 0]
            
            for xx in reversed(range(0, x)):
                scores[0] += 1
                if grid[y][xx] >= height:
                    break
                
            for xx in range(x + 1, len(row)):
                scores[1] += 1
                if grid[y][xx] >= height:
                    break
                
            for yy in reversed(range(0, y)):
                scores[2] += 1
                if grid[yy][x] >= height:
                    break
                
            for yy in range(y + 1, len(grid)):
                scores[3] += 1
                if grid[yy][x] >= height:
                    break
                
            best_scenic_score_so_far = max(best_scenic_score_so_far, reduce(lambda a, b: a * b, scores, 1))
            
    print(f"* It seems like {best_scenic_score_so_far} is the highest scenic score for any tree.")
