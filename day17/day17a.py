import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 17/12 ~~~
""")

start_time = perf_counter()
    
shapes = [
    [(0, 0,), (1, 0), (2, 0), (3, 0)], # -
    [(0, 1,), (1, 0), (1, 1), (1, 2), (2, 1)], # +
    [(0, 0,), (1, 0), (2, 0), (2, 1), (2, 2)], # _|
    [(0, 0,), (0, 1), (0, 2), (0, 3)], # |
    [(0, 0,), (1, 0), (0, 1), (1, 1)], # []
]

shape_idx = 0
jet_idx = 0
faller_y = 3
faller_x = 2
game_board = {}
stack_height = 0

def draw_board():
    global shape_idx, jet_idx, faller_x, faller_y
    
    height = stack_height
    board = game_board.copy()
    for block_x, block_y in shapes[shape_idx]:
        height = max(height, faller_y + block_y)
        board[faller_x + block_x, faller_y + block_y] = chr(ord("/") + ((jet_idx + 1) % 46))
    
    output = ""
        
    for y in reversed(range(height + 1)):
        line = "|"
        for x in range(0, 7):
            line += board.get((x, y), ".")
        line += "|\n"
        output += line
        
    output += "+-------+"
    
    print(output)
    print("\n")
    
def is_position_blocked(x, y):
    global shape_idx, game_board
    
    if y < 0:
        return True
    
    for block_x, block_y in shapes[shape_idx]:
        if x + block_x < 0 or x + block_x >= 7:
            return True
        
        if (x + block_x, y + block_y) in game_board:
            return True
    
    return False

with open("input.txt", "r") as file:
    jet_pattern = [1 if c == ">" else -1 for c in file.read().strip()]
    
rounds_left = 2022
while rounds_left > 0:
    # draw_board()
    
    jet_push = jet_pattern[jet_idx]
    jet_idx = (jet_idx + 1) % len(jet_pattern)
    if not is_position_blocked(faller_x + jet_push, faller_y):
        faller_x += jet_push

    # draw_board()
    
    if is_position_blocked(faller_x, faller_y - 1):
        for block_x, block_y in shapes[shape_idx]:
            game_board[faller_x + block_x, faller_y + block_y] = chr(ord("/") + (jet_idx % 46))
            stack_height = max(stack_height, faller_y + block_y + 1)
            
        shape_idx = (shape_idx + 1) % len(shapes)
        faller_x = 2
        faller_y = stack_height + 3
        
        rounds_left -= 1
        
        # draw_board()
    else:
        faller_y -= 1
    
# draw_board()
print(f"* I'll tell the elephants that my simulation predicts the tower of rocks will reach {stack_height} blocks tall after 2022 rocks have fallen.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")