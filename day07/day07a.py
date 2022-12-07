import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 07/12 ~~~
""")

class Directory:
    def __init__(self, parent):
        self.subdirs = {"..": parent}
        self.files_sizes = []
        self.size = -1

with open("input.txt", "r") as file:
    root = Directory(None)

    pointer = root

    for line in file:
        if line.startswith("$"):
            split = line.split()
            if split[1] == "cd":
                arg = split[2]
                pointer = root if arg == "/" else pointer.subdirs[arg]
        else:
            left, right = line.split()
            if left == "dir":
                pointer.subdirs[right] = Directory(pointer)
            else:
                pointer.files_sizes.append(left)
