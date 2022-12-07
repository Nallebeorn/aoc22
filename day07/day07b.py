import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
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

directories_sizes = []
    
def traverse_and_find_size(dir):
    global directories_sizes
    
    dir.size = sum(dir.files_sizes)
    for subdir in dir.subdirs.values():
        if subdir.size == -1:
            traverse_and_find_size(subdir)
            
        dir.size += subdir.size
        
    directories_sizes.append(dir.size)
    
traverse_and_find_size(root)

disk_total_space = 70_000_000
needed_space = 30_000_000

used_space = root.size
unused_space = disk_total_space - used_space
space_to_free_up = needed_space - unused_space

print(f"Disk usage: {used_space}/{disk_total_space}. Required: {needed_space}. Must free an additional {space_to_free_up} of space.")

size_of_smallest_viable_deletion = min([size for size in directories_sizes if size >= space_to_free_up])
    
print(f"Of the directories large enough that deleting one of them would free up the space required for the update, {size_of_smallest_viable_deletion} is the smallest size.")
