import os
import sys
from time import sleep
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 14/12 ~~~
""")

def draw_tilemap(tilemap, minx, maxx, maxy):
    output_lines = []
    for y in range(0, maxy + 1):
        line = ""
        for x in range(minx, maxx + 1):
            line += tilemap.get((x, y), ".")
        output_lines.append(line)
    output = "\n".join(output_lines)
    
    print(output)

with open("input.txt", "r") as file:
    paths = [[tuple(int(a) for a in point.split(",")) for point in line.strip().split(" -> ")] for line in file]
    
    start = (500, 0)
    
    tilemap = {start: "+"}
    for path in paths:
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    tilemap[x, y1] = "#"
            else:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    tilemap[x1, y] = "#"
                
    minx = min(x for x, y in tilemap.keys())
    maxx = max(x for x, y in tilemap.keys())
    maxy = max(y for x, y in tilemap.keys())
    
    sand_counter = 0
    fallen_into_abyss = False
    while not fallen_into_abyss:
        sandx, sandy = start
        while not fallen_into_abyss:
            tilemap[(sandx, sandy)] = "o"
            
            prev_sand_pos = (sandx, sandy)
            
            if (sandx, sandy + 1) not in tilemap:
                sandy += 1
            elif (sandx - 1, sandy + 1) not in tilemap:
                sandx -= 1
                sandy += 1
            elif (sandx + 1, sandy + 1) not in tilemap:
                sandx += 1
                sandy += 1
            else:
                sand_counter += 1
                break
            
            # print(chr(27) + "[2J")            
            # draw_tilemap(tilemap, minx, maxx, maxy)
            # sleep(0.05)
            
            del tilemap[prev_sand_pos]
            
            if sandy > maxy:
                fallen_into_abyss = True
    
    tilemap[start] = "+"
    draw_tilemap(tilemap, minx, maxx, maxy)
    print("")
    print(f"* Only after {sand_counter} units of sand have fallen and come to rest will the sand start flowing into the abyss below.")