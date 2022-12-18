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
    cubemap = [tuple([int(n) for n in line.strip().split(",")]) for line in file]

count = 0

min_pos = cubemap[0]
max_pos = cubemap[0]

for x, y, z in cubemap:
    minx, miny, minz = min_pos
    maxx, maxy, maxz = max_pos
    min_pos = (min(minx, x), min(miny, y), min(minz, z))
    max_pos = (max(maxx, x), max(maxy, y), max(maxz, z))
    
print(min_pos, max_pos)

print(f"* A single lava droplet has a surface area of {count} according to my scan.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")