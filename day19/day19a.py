import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 19/12 ~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    
    blueprints = []
    
    for blueprint in file.read().splitlines():
        numbers = [int(c) for c in blueprint.split() if c.isdigit()]
        blueprints.append({
            "ore": {
                "ore": numbers[0],
            },
            "clay": {
                "ore": numbers[1],
            },
            "obsidian": {
                "ore": numbers[2],
                "clay": numbers[3],
            },
            "geode": {
                "ore": numbers[4],
                "obsidian": numbers[5],
            },
        })
        
    print(blueprints)
    
start_state = {
    "time_remaining": 24,
    "rate": {
        "ore": 1,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    },
    "inventory": {
        "ore": 0,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }
}
    
end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")