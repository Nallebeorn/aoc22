import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

with open("input.txt", "r") as file:
    section_assignments = [[tuple(int(num) for num in assignment.split("-")) for assignment in line.strip().split(",")] for line in file]
    
    counter = 0
    
    for pair in section_assignments:
        min1, max1 = pair[0]
        min2, max2 = pair[1]
        if (min1 >= min2 and min1 <= max2) or (max1 >= min2 and max1 <= max2) \
        or (min2 >= min1 and min2 <= max1) or (max2 >= min1 and max2 <= max1):
            counter += 1

    print(f"* There are {counter} assignment pairs where the ranges overlap.")