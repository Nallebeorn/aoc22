import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 22/12 ~~~
""")

start_time = perf_counter()

def parse_board(lines):
    width = max(len(line) for line in lines)
    height = len(lines)
    board = [" "] * width * height
    for y in range(height):
        line = lines[y]
        for x in range(len(line)):
            board[y * width + x] = line[x]

    return width, height, board

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

print(f"* Having followed the monkeys' path, I can conclude that the password is {final_password} based on my location and the direction I'm facing.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")