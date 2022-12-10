import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 09/12 ~~~

""")

def sign(x):
    return (x > 0) - (x < 0)

with open("input.txt", "r") as file:
    commands = [tuple(line.split()) for line in file]

    visited_positions = set()
    
    head_pos_x, head_pos_y = 0, 0
    tail_pos_x, tail_pos_y = 0, 0
    
    visited_positions.add((tail_pos_x, tail_pos_y))
    
    for direction, num_steps in commands:
        for i in range(int(num_steps)):
            if direction == "R":
                head_pos_x += 1
            elif direction == "L":
                head_pos_x -= 1
            elif direction == "U":
                head_pos_y -= 1
            elif direction == "D":
                head_pos_y += 1
                
            diff_x = head_pos_x - tail_pos_x
            diff_y = head_pos_y - tail_pos_y
            
            if max(abs(diff_x), abs(diff_y)) >= 2:
                tail_pos_x += sign(diff_x)
                tail_pos_y += sign(diff_y)
            
            visited_positions.add((tail_pos_x, tail_pos_y))
                    
    num_visisted_positions = len(visited_positions)
    
    print(f"In my diverting thought experiment, the tail of the rope would visit {num_visisted_positions} positions at least once.")