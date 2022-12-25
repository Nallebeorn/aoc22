import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 22/12 ~~~
""")

start_time = perf_counter()

CUBE_SIZE = 4

def parse_board(lines):
    width = max(len(line) for line in lines)
    height = len(lines)
    board = [" "] * width * height
    for y in range(height):
        line = lines[y]
        for x in range(len(line)):
            board[y * width + x] = line[x]

    return width, height, board

def split_board(board_tuple):
    width, height, board = board_tuple
    num_x = width // CUBE_SIZE
    num_y = height // CUBE_SIZE
    sides = {}
    for sidey in range(num_y):
        for sidex in range(num_x):
            side = {}
            startx = sidex * CUBE_SIZE
            starty = sidey * CUBE_SIZE
            for y in range(CUBE_SIZE):
                for x in range(CUBE_SIZE):
                    side[(x, y, CUBE_SIZE - 1)] = board_get(board_tuple, (startx + x, starty + y))

            if not all(c == " " for c in side.values()):
                sides[(sidex, sidey)] = side

    connections = {}
    for sidex, sidey in sides:
        cons = {}
        for ofsx, ofsy in movement.values():
            if (sidex + ofsx, sidey + ofsy) in sides:
                cons[ofsx, ofsy] = sidex + ofsx, sidey + ofsy
        connections[sidex, sidey] = cons

    print(connections)

    cube = {}

    visited = set()
    frontier = []
    frontier.append((next(iter(sides)), []))
    while len(frontier) > 0:
        side, transformations = frontier.pop()
        print("CUBE SIDE", side)
        visited.add(side)

        neg = CUBE_SIZE - 1
        for pos, value in sides[side].items():
            x, y, z = pos
            for trans in transformations:
                if trans == (1, 0):
                    x, y, z = (z, y, neg - x)
                elif trans == (-1, 0):
                    x, y, z = (neg - z, y, x)
                elif trans == (0, 1):
                    x, y, z = (x, z, neg - y)
                elif trans == (0, -1):
                    x, y, z = (x, neg - z, y)
                else:
                    raise Exception("Unreachable code")

            cube[x, y, z] = value

        for con, other_side in connections[side].items():
            if not other_side in visited:
                frontier.append((other_side, transformations + [con]))
    
    print("cube size", len(cube), "expected", 6 * CUBE_SIZE * CUBE_SIZE)
    return cube

def parse_path(string):
    path = []
    current_number = ""
    for c in string:
        if c.isdigit():
            current_number += c
        else:
            if current_number:
                path.append(int(current_number))
                current_number = ""
            path.append(c)

    if current_number:
        path.append(int(current_number))

    return path

def print_board(board_tuple):
    width, height, board = board_tuple
    output = ""
    for y in range(height):
        for x in range(width):
            output += board[y * width + x]
        output += "\n"
    
    print(output)

def board_get(board_tuple, pos):
    width, height, board = board_tuple
    x, y = pos
    return board[y * width + x]

def board_set(board_tuple, pos, value):
    width, height, board = board_tuple
    x, y = pos
    board[y * width + x] = value

def is_out_of_bounds(board_tuple, pos):
    width, height, board = board_tuple
    x, y = pos
    return x < 0 or y < 0 or x >= width or y >= height or board_get(board_tuple, pos) == " " 

with open("input.txt", "r") as file:
    lines = [line for line in file.read().splitlines() if line]

board = parse_board(lines[:-1])
width, height, board_array = board
path = parse_path(lines[-1])

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

movement = {
    RIGHT: (1, 0),
    DOWN: (0, 1),
    LEFT: (-1, 0),
    UP: (0, -1),
}

facing_symbol = {
    RIGHT: ">",
    DOWN: "v",
    LEFT: "<",
    UP: "^",
}

facing = RIGHT

position = (0, 0)
for x in range(width):
    if board_get(board, (x, 0)) == ".":
        position = (x, 0)
        break

board_set(board, position, facing_symbol[facing])

cube = split_board(board)
print("CUBEDIDOO", {k: v for k, v in cube.items() if k[0] == 4})
exit()

for instruction in path:
    if instruction == "L":
        facing = (facing - 1) % 4
    elif instruction == "R":
        facing = (facing + 1) % 4
    else:
        num_steps = instruction
        for i in range(num_steps):
            x, y = position
            movex, movey = movement[facing]
            newx, newy = x + movex, y + movey
            
            if is_out_of_bounds(board, (newx, newy)):
                while not is_out_of_bounds(board, (newx - movex, newy - movey)):
                    newx -= movex
                    newy -= movey

            cell_at_new = board_get(board, (newx, newy))

            if cell_at_new == "#":
                break
            else:
                position = (newx, newy)

            board_set(board, position, facing_symbol[facing])

    board_set(board, position, facing_symbol[facing])

print_board(board)

final_password = (position[0] + 1) * 4 + (position[1] + 1) * 1000 + facing

print(f"* Having traced the monkeys' path on the input device, I can conclude that {final_password} must be the password.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")