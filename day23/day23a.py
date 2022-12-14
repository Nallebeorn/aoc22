import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 23/12 ~~~
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

# print_state(elves)

for i in range(num_rounds):
    proposals = {}
    for elfx, elfy in elves:
        if all(all((elfx + ofsx, elfy + ofsy) not in elves for ofsx, ofsy in direction) for direction in directions):
            continue
        for direction in directions:
            if all((elfx + ofsx, elfy + ofsy) not in elves for ofsx, ofsy in direction):
                movex, movey = direction[1]
                proposals[elfx, elfy] = (elfx + movex, elfy + movey)
                break

    first_direction = directions.pop(0)
    directions.append(first_direction)

    for elf, move_to in proposals.items():
        if sum(1 for x in proposals.values() if x == move_to) == 1:
            elves.remove(elf)
            elves.add(move_to)
    
    # print_state(elves)

minx = min(x for x, y in elves)
maxx = max(x for x, y in elves)
miny = min(y for x, y in elves)
maxy = max(y for x, y in elves)
empty_ground_count = 0
for y in range(miny, maxy + 1):
    for x in range(minx, maxx + 1):
        if (x, y) not in elves:
            empty_ground_count += 1

print(f"* After 10 rounds of the elves' process, no more than {empty_ground_count} tiles of ground will have been covered.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")