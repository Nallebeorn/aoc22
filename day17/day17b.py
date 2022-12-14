import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
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

# For some inexplicable reason, my solution doesn't work if the input is too small (e.g. example input)
while len(jet_pattern) < 2000:
    jet_pattern += jet_pattern[:]
    
def simulate_cycle(max_rounds = None):
    global jet_idx, shape_idx, game_board, faller_x, faller_y, stack_height
    
    rounds = 0
    
    while max_rounds == None or rounds < max_rounds:
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
            
            rounds += 1
            
            # draw_board()
        else:
            faller_y -= 1
            
        if jet_idx == 0:
            print("idx", shape_idx)
            break
    
    return (stack_height, rounds)

num_rounds = 1_000_000_000_000

cycle1_height, cycle1_rounds = simulate_cycle()
cycle2_height, rounds_per_cycle = simulate_cycle()
height_per_cycle = cycle2_height - cycle1_height

predicted_height = cycle1_height
remaining_rounds = num_rounds - cycle1_rounds
predicted_height += (remaining_rounds // rounds_per_cycle) * height_per_cycle
last_remaining_rounds = (remaining_rounds % rounds_per_cycle)
final_cycle_height, final_cycle_rounds = simulate_cycle(last_remaining_rounds)
predicted_height += final_cycle_height - cycle2_height

print(f"* I'll have those darn elephants know that after a trillion rocks have fallen, the tower will be exactly {predicted_height} blocks tall, no more no less!")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")