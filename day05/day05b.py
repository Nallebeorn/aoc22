import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

with open("input.txt", "r") as file:
    lines = file.read().splitlines()

    empty_line_index = lines.index("")
    initial_board_state_lines = [line for line in lines[:empty_line_index - 1]]
    digit_line = lines[empty_line_index - 1]
    instructions = [[int(word) for word in line.split() if word.isdigit()] for line in lines[empty_line_index + 1:]]

    towers = []
    for i, chr in enumerate(digit_line):
        if chr.strip():
            full_column = [initial_board_state_lines[y][i] for y in reversed(range(empty_line_index - 1))]
            towers.append([crate for crate in full_column if crate.strip()])

    for amount, from_column, to_column in instructions:
        towers[to_column - 1] += towers[from_column - 1][-amount:]
        del towers[from_column - 1][-amount:]

    top_crates = "".join(stack[-1] for stack in towers)

    print(f"* After the rearrangement procedure completed, {top_crates} are the crates that ended up on top of each stack.")