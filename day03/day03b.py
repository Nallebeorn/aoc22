import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

item_priority_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
group_size = 3

def is_item_in_every_rucksack(item, rucksacks):
    for rucksack in rucksacks:
        if not item in rucksack:
            return False
    return True

with open("input.txt", "r") as file:
    rucksacks = [line.strip() for line in file]
    elf_groups = [rucksacks[i:i + group_size] for i in range(0, len(rucksacks), group_size)]
    
    total_priority = 0
    
    for group in elf_groups:
        for item in group[0]:
            if is_item_in_every_rucksack(item, group[1:]):
                total_priority += item_priority_order.index(item) + 1
                break

    print(f"* The total priority is {total_priority} for the items used as badges by the elf-groups.")