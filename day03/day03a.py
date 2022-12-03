import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 03/12 ~~~
""")

item_priority_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("input.txt", "r") as file:
    rucksacks = [line.strip() for line in file]
    compartmented_rucksacks = [(line[:len(line)//2], line[len(line)//2:]) for line in rucksacks]
    
    total_priority = 0
    
    for compartment1, compartment2 in compartmented_rucksacks:
        for item in compartment1:
            if item in compartment2:
                total_priority += item_priority_order.index(item) + 1
                break

    print(f"* The total priority is {total_priority} for the items mistakenly placed into two compartments in any rucksack.")