import os
import sys
from functools import *
from time import perf_counter
from math import ceil
from copy import deepcopy
from collections import deque

os.chdir(os.path.dirname(sys.argv[0]))

print(
    """~~~ 19/12 ~~~
""")

start_time = perf_counter()

ORE = "ore"
CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"

class Node:
    def __init__(self, time_remaining: int, inventory: dict[int, int], robots: dict[int, int], prev: "Node"):
        self.time_remaining = time_remaining
        self.inventory = inventory.copy()
        self.robots = robots.copy()
        self.prev = prev
        self.depth = 0 if prev == None else prev.depth + 1

    def __repr__(self):
        return f"[{self.depth}] {self.time_remaining} :: INV {self.inventory} ROB {self.robots}"

with open("input.txt", "r") as file:

    blueprints = []

    for blueprint in file.read().splitlines():
        numbers = [int(c) for c in blueprint.split() if c.isdigit()]
        blueprints.append({
            ORE: {ORE: numbers[0]},
            CLAY: {ORE: numbers[1]},
            OBSIDIAN: {ORE: numbers[2], CLAY: numbers[3]},
            GEODE: {ORE: numbers[4], OBSIDIAN: numbers[5]},
        })

quality_level_sum = 0

for bp_index, blueprint in enumerate(blueprints[:1]):
    print("BLUEPRINT", bp_index)
    start_state = Node(24, {ORE: 0, CLAY: 0, OBSIDIAN: 0, GEODE: 0}, {ORE: 1, CLAY: 0, OBSIDIAN: 0, GEODE: 0}, None)
    frontier: deque[Node] = deque()
    frontier.append(start_state)

    best_so_far = None

    while len(frontier) > 0:
        state = frontier.pop()

        # print(most_geodes, state)

        if state.time_remaining <= 0:
            print(0 if not best_so_far else best_so_far.inventory[GEODE], state.inventory[GEODE])
            print(state)
            if best_so_far == None or state.inventory[GEODE] > best_so_far.inventory[GEODE]:
                best_so_far = state
                if state.inventory[GEODE] >= 14:
                    break
            continue

        if best_so_far != None:
            theoretical_best = state.robots[GEODE] * state.time_remaining
            for i in reversed(range(0, state.time_remaining)):
                theoretical_best += i

            if theoretical_best < best_so_far.inventory[GEODE]:
                continue

        rate = state.robots
        inventory = state.inventory

        for robot_type, recipe in blueprint.items():
            remaining = {mat: max(0, recipe[mat] - inventory[mat]) for mat in recipe}
            
            could_build_anything = False
            if all(rate[mat] > 0 for mat in recipe):
                new_state = Node(state.time_remaining, state.inventory, state.robots, state)
                time_until_build = max(ceil(remaining[mat] / rate[mat]) for mat in remaining)
                new_state.inventory = {mat: inventory[mat] - recipe.get(mat, 0) + rate[mat] * time_until_build for mat in inventory}
                new_state.robots[robot_type] += 1
                new_state.time_remaining -= max(1, time_until_build)
                if new_state.time_remaining > 0:
                    could_build_anything = True
                    frontier.append(new_state)
            
            if not could_build_anything:
                new_state = Node(state.time_remaining, state.inventory, state.robots, state)
                new_state.inventory = {mat: inventory[mat] + rate[mat] * state.time_remaining for mat in inventory}
                new_state.time_remaining -= state.time_remaining
                frontier.append(new_state)
    
    quality_level_sum += (bp_index + 1) * best_so_far.inventory[GEODE]
    
    path = [best_so_far]
    while best_so_far.prev != None:
        best_so_far = best_so_far.prev
        path.append(best_so_far)

    print("STEPS")
    for step in reversed(path):
        print(step)

print(quality_level_sum)

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")
