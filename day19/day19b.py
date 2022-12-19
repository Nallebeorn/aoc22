import os
import sys
from functools import *
from time import perf_counter
from collections import deque

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    cubemap = set(tuple([int(n) for n in line.strip().split(",")]) for line in file)

min_pos = (0, 0, 0)
max_pos = (0, 0, 0)

for x, y, z in cubemap:
    minx, miny, minz = min_pos
    maxx, maxy, maxz = max_pos
    min_pos = (min(minx, x - 1), min(miny, y - 1), min(minz, z - 1)) # Add margin of 1 so we have a margin where we know every voxel will be exterior air
    max_pos = (max(maxx, x + 1), max(maxy, y + 1), max(maxz, z + 1)) # that we can start the search from later
    
frontier = deque()
frontier.append(min_pos)

minx, miny, minz = min_pos
maxx, maxy, maxz = max_pos

sizex = maxx - minx + 1
sizey = maxy - miny + 1
sizez = maxz - minz + 1

# Checking if a value is in a set is supposed to pretty fast and O(1), but it's far too slow for the search with real input apparently...
# So I make an array that can be indexed with the position instead

UNKNOWN = 0
EXTERIOR_AIR = 1
BLOCK = 2

cubemap_arr = [UNKNOWN] * sizex * sizey * sizez

def get_index(x, y, z):
    return x + y * sizex + z * sizex * sizey

for x, y, z in cubemap:
    cubemap_arr[get_index(x, y, z)] = BLOCK

while len(frontier) > 0:
    current = frontier.popleft()
    
    x, y, z = current
    
    for neighbour in [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]:
        nx, ny, nz = neighbour
        if nx >= minx and ny >= miny and nz >= minz and nx <= maxx and ny <= maxy and nz <= maxz:
            if cubemap_arr[get_index(nx, ny, nz)] == UNKNOWN:
                cubemap_arr[get_index(nx, ny, nz)] = EXTERIOR_AIR
                frontier.append(neighbour)

count = 0                

for x, y, z in cubemap:
    for neighbour in [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]:
        nx, ny, nz = neighbour
        if cubemap_arr[get_index(nx, ny, nz)] == EXTERIOR_AIR:
            count += 1

print(f"* A single lava droplet has a surface area of {count} exposed to the open air.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")