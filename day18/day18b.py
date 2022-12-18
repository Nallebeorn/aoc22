import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    cubemap = set(tuple([int(n) for n in line.strip().split(",")]) for line in file)
    
def is_cube_in_xpos(cubemap, start_pos):
    x1, y1, z1 = start_pos
    for x2, y2, z2 in cubemap - {start_pos}:
        if y1 == y2 and z1 == z2 and x2 > x1:
            return True
            
    return False
    
def is_cube_in_xneg(cubemap, start_pos):
    x1, y1, z1 = start_pos
    for x2, y2, z2 in cubemap - {start_pos}:
        if y1 == y2 and z1 == z2 and x2 < x1:
            return True
            
    return False
    
def is_cube_in_ypos(cubemap, start_pos):
    x1, y1, z1 = start_pos
    for x2, y2, z2 in cubemap - {start_pos}:
        if x1 == x2 and z1 == z2 and y2 > y1:
            return True
            
    return False
    
def is_cube_in_yneg(cubemap, start_pos):
    x1, y1, z1 = start_pos
    for x2, y2, z2 in cubemap - {start_pos}:
        if x1 == x2 and z1 == z2 and y2 < y1:
            return True
            
    return False
    
def is_cube_in_zpos(cubemap, start_pos):
    x1, y1, z1 = start_pos
    for x2, y2, z2 in cubemap - {start_pos}:
        if x1 == x2 and y1 == y2 and z2 > z1:
            return True
            
    return False
    
def is_cube_in_zneg(cubemap, start_pos):
    x1, y1, z1 = start_pos
    for x2, y2, z2 in cubemap - {start_pos}:
        if x1 == x2 and y1 == y2 and z2 < z1:
            return True
            
    return False

count = 0

air_pockets = set()

def check_if_air_pocket(cubemap, pos):
    return pos not in cubemap \
       and is_cube_in_xpos(cubemap, pos) \
       and is_cube_in_xneg(cubemap, pos) \
       and is_cube_in_ypos(cubemap, pos) \
       and is_cube_in_yneg(cubemap, pos) \
       and is_cube_in_zpos(cubemap, pos) \
       and is_cube_in_zneg(cubemap, pos)

for x, y, z in cubemap:
    for pos in [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]:
        if check_if_air_pocket(cubemap, pos):
            air_pockets.add(pos)
        
for cube in cubemap:
    x, y, z = cube
    
    for pos in [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]:
        count += pos not in cubemap and pos not in air_pockets
    
print(f"* A single lava droplet has a surface area of {count} according to my scan.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")