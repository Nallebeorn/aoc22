import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 22
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

CUBE = 50

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

            new_facing = facing
            
            if is_out_of_bounds(board, (newx, newy)):
                relx, rely = (x % CUBE, y % CUBE)
                chunkx, chunky = (newx // CUBE, newy // CUBE)
                print("WRAP", facing_symbol[facing], chunkx, chunky, "at", newx, newy)
                if chunkx == 1 and chunky == -1 and facing == UP:
                    newx = 0
                    newy = 3 * CUBE + relx
                    new_facing = RIGHT
                elif chunkx == 2 and chunky == -1 and facing == UP:
                    newx = relx
                    newy = 3 * CUBE + CUBE - 1
                    new_facing = UP
                elif chunkx == 0 and chunky == 0 and facing == LEFT:
                    newx = 0
                    newy = 2 * CUBE + (CUBE - 1 - rely)
                    new_facing = RIGHT
                elif chunkx == 3 and chunky == 0 and facing == RIGHT:
                    newx = CUBE + CUBE - 1
                    newy = 2 * CUBE + (CUBE - 1 - rely)
                    new_facing = LEFT
                elif chunkx == 0 and chunky == 1:
                    if facing == LEFT and relx == 0:
                        newx = rely
                        newy = CUBE * 2
                        new_facing = DOWN
                    elif facing == UP and rely == 0:
                        newx = CUBE
                        newy = CUBE + relx
                        new_facing = RIGHT
                    else:
                        raise Exception(f"Unreachable code in special case, {facing}, {relx}, {rely}")
                elif chunkx == 2 and chunky == 1:
                    if facing == RIGHT and relx == CUBE - 1:
                        newx = CUBE * 2 + rely
                        newy = CUBE - 1
                        new_facing = UP
                    elif facing == DOWN and rely == CUBE - 1:
                        newx = CUBE + CUBE - 1
                        newy = CUBE + relx
                        new_facing = LEFT
                    else:
                        raise Exception(f"Unreachable code in special case, {facing}, {relx}, {rely}")
                elif chunkx == -1 and chunky == 2 and facing == LEFT:
                    newx = CUBE
                    newy = CUBE - 1 - rely
                    new_facing = RIGHT
                elif chunkx == 2 and chunky == 2 and facing == RIGHT:
                    newx = CUBE * 2 + CUBE - 1
                    newy = CUBE - 1 - rely
                    new_facing = LEFT
                elif chunkx == -1 and chunky == 3 and facing == LEFT:
                    newx = CUBE + rely
                    newy = 0
                    new_facing = DOWN
                elif chunkx == 0 and chunky == 4 and facing == DOWN:
                    newx = CUBE * 2 + relx
                    newy = 0
                    new_facing = DOWN
                elif chunkx == 1 and chunky == 3:
                    if facing == DOWN and rely == CUBE - 1:
                        newx = CUBE - 1
                        newy = CUBE * 3 + relx
                        new_facing = LEFT
                    elif facing == RIGHT and relx == CUBE - 1:
                        newx = CUBE + rely
                        newy = CUBE * 2 + CUBE - 1
                        new_facing = UP
                    else:
                        raise Exception(f"Unreachable code in special case, {facing}, {relx}, {rely}")
                else:
                    raise Exception(f"Unreachable code {facing_symbol[facing]} {chunkx},{chunky} ({newx}, {newy})")

                print(x, y, facing_symbol[facing], "=>", newx, newy, facing_symbol[new_facing], "\n")

            cell_at_new = board_get(board, (newx, newy))

            if cell_at_new == "#":
                break
            else:
                position = (newx, newy)
                facing = new_facing

            board_set(board, position, facing_symbol[facing])

    board_set(board, position, facing_symbol[facing])

print_board(board)

final_password = (position[0] + 1) * 4 + (position[1] + 1) * 1000 + facing

print(f"* Having retraced the monkeys' path on the (apparently cubic!) input device, I can conclude that {final_password} must be the real password.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")