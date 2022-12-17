import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 15/12 ~~~
""")

with open("input.txt", "r") as file:
    look_at_y = 2_000_000
    
    covered_positions = set()
    for data in [line.split() for line in file]:
        sensor_x = int("".join(c for c in data[2] if c.isdigit() or c == "-"))
        sensor_y = int("".join(c for c in data[3] if c.isdigit() or c == "-"))
        
        beacon_x = int("".join(c for c in data[-2] if c.isdigit() or c == "-"))
        beacon_y = int("".join(c for c in data[-1] if c.isdigit() or c == "-"))
        
        distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        
        y = look_at_y - sensor_y
            
        xdist = distance - abs(y)
        if xdist > 0:
            for x in range(-xdist, xdist):
                covered_positions.add((sensor_x + x, look_at_y))
    
    num_covered_postions_in_row = len(covered_positions)
    print(f"* In the row where y={look_at_y}, there are {num_covered_postions_in_row} positions where I can deduce a beacon cannot be present.")