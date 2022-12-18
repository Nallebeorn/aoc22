import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 18/12 ~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    cubemap = set(tuple([int(n) for n in line.strip().split(",")]) for line in file)
    
count = 0

for x, y, z in cubemap:
    count += (x + 1, y, z) not in cubemap
    count += (x - 1, y, z) not in cubemap
    count += (x, y + 1, z) not in cubemap
    count += (x, y - 1, z) not in cubemap
    count += (x, y, z + 1) not in cubemap
    count += (x, y, z - 1) not in cubemap
    
print(f"* A single lava droplet has a surface area of {count} according to my scan.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")