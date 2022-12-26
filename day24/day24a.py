import os
import sys
from functools import *
from time import perf_counter
import heapq

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 24/12 ~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    lines = [line.strip()[1:-1] for line in file][1:-1]
    width = len(lines[0])
    height = len(lines)
    blizzards = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in [">", "v", "<", "^"]:
                blizzards.append((c, x, y))

state_cache = {}
state_cache[0] = blizzards

def evaluate_blizzard_state(minute):
    global width, height, state_cache

    if minute in state_cache:
        return state_cache[minute]
    
    print("Simulate blizzards at minute:", minute)

    new_state = []
    blizzards = evaluate_blizzard_state(minute - 1)
    for direction, x, y in blizzards:
        if direction == ">":
            x += 1
        elif direction == "<":
            x -= 1
        elif direction == "v":
            y += 1
        elif direction == "^":
            y -= 1
        else:
            raise Exception("Unreachable code")
        x = x % width
        y = y % height
        new_state.append((direction, x, y))

    state_cache[minute] = new_state

    return new_state

def is_blizzard_at(blizzards, pos):
    x, y = pos
    for direction, blizx, blizy in blizzards:
        if x == blizx and y == blizy:
            return True
    
    return False

def is_in_bounds(pos):
    global width, height

    x, y = pos

    if x >= 0 and y >= 0 and x < width and y < height:
        return True

    if x == 0 and y == -1:
        return True

    if x == width - 1 and y == height:
        return True

    return False

def heuristic(begin, end):
    bx, by = begin
    ex, ey = end
    return abs(bx - ex) + abs(by - ey)

def print_blizzards(blizzards):
    global width, height

    board = []
    for y in range(height):
        board.append(["."] * width)

    for direction, x, y in blizzards:
        if board[y][x] == ".":
            board[y][x] = direction
        elif board[y][x].isdigit():
            board[y][x] = str(int(board[y][x]) + 1)
        else:
            board[y][x] = "2"

    output = ""
    for y in range(height):
        for x in range(width):
            output += board[y][x]
        output += "\n"

    print(output)

def find_path_length(start, goal):
    frontier = []
    heapq.heappush(frontier, (0, 0, start))

    visited = set()

    while len(frontier) > 0:
        priority, cost_so_far, pos = heapq.heappop(frontier)
        x, y = pos

        if pos == goal:
            return cost_so_far
        
        next_cost = cost_so_far + 1
        next_blizzard = evaluate_blizzard_state(next_cost)

        for movex, movey in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_pos = (x + movex, y + movey)
            if (next_cost, next_pos) not in visited:
                if (not is_blizzard_at(next_blizzard, next_pos)) and is_in_bounds(next_pos):
                    priority = next_cost + heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_cost, next_pos))
                    visited.add((next_cost, next_pos))

# print_blizzards(evaluate_blizzard_state(10))

start = (0, -1)
goal = (width - 1, height)

path_length = find_path_length((0, -1), (width - 1, height))
            
print(f"* It will take me at least {path_length} minutes to get through the valley while carefully avoiding the many blizzards.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")