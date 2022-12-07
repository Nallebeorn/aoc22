import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 07/12 ~~~
""")

class Directory:
    def __init__(self, parent):
        self.parent = parent
        self.subdirs = {}
        self.files_sizes = []
        self.size = -1
    
root = Directory(None)
pointer = root

with open("input.txt", "r") as file:
    for line in file:
        if line.startswith("$"):
            split = line.split()
            if split[1] == "cd":
                arg = split[2]
                if arg == "/":
                    pointer = root
                elif arg == "..":
                    pointer = pointer.parent
                else:
                    pointer = pointer.subdirs[arg]
        else:
            left, right = line.split()
            if left == "dir":
                pointer.subdirs[right] = Directory(pointer)
            else:
                pointer.files_sizes.append(int(left))

total_size_sum = 0
    
def traverse_and_find_size(dir):
    global total_size_sum
    
    dir.size = sum(dir.files_sizes)
    for subdir in dir.subdirs.values():
        if subdir.size == -1:
            traverse_and_find_size(subdir)
            
        dir.size += subdir.size
    if dir.size <= 100_000:
        total_size_sum += dir.size
    
traverse_and_find_size(root)
    
print(f"The sum of the total sizes of directories {total_size_sum} (disregarding directories larger than 100 000)")
