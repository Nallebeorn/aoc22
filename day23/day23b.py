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
    elves = set()
    for y, line in enumerate(file):
        for x, c in enumerate(line):
            if c == "#":
                elves.add((x, y))

def print_state(elves):
    minx = min(x for x, y in elves)
    maxx = max(x for x, y in elves)
    miny = min(y for x, y in elves)
    maxy = max(y for x, y in elves)
    output = ""
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            output += "#" if (x, y) in elves else "."
        output += "\n"
    
    print(output)

num_rounds = 10

directions = [
    [(-1, -1), (0, -1), (1, -1)], # NW N NE
    [(-1, 1), (0, 1), (1, 1)], # SW S SE
    [(-1, -1), (-1, 0), (-1, 1)], # NW W SW
    [(1, -1), (1, 0), (1, 1)], # NE E SE
]

all_adjacent = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

directions = [[all_adjacent.index((ofsx, ofsy)) for ofsx, ofsy in dir] for dir in directions]

# print_state(elves)

num_rounds = 0
while True:
    num_rounds += 1
    # print(num_rounds)

    proposals = {}
    for elfx, elfy in elves:
        adjacent_free = [(elfx + ofsx, elfy + ofsy) not in elves for ofsx, ofsy in all_adjacent]
        if all(adjacent_free):
            continue
        for direction in directions:
            if all(adjacent_free[idx] for idx in direction):
                movex, movey = all_adjacent[direction[1]]
                move_to = (elfx + movex, elfy + movey)
                proposals[move_to] = (elfx, elfy) if move_to not in proposals else None
                break

    first_direction = directions.pop(0)
    directions.append(first_direction)

    did_any_elf_move = False

    for move_to, elf in proposals.items():
        if elf != None:
            elves.remove(elf)
            elves.add(move_to)
            did_any_elf_move = True

    if not did_any_elf_move:
        break
    
    # print_state(elves)

print(f"* Round {num_rounds} will be the first round where no elf moves.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")