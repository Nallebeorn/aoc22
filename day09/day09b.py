import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

def sign(x):
    return (x > 0) - (x < 0)

with open("input.txt", "r") as file:
    commands = [tuple(line.split()) for line in file]

    visited_positions = set()
    
    rope = [(0, 0)] * 10
    
    visited_positions.add(rope[-1])
    
    for direction, num_steps in commands:
        for step in range(int(num_steps)):
            head_pos_x, head_pos_y = rope[0]
            
            if direction == "R":
                head_pos_x += 1
            elif direction == "L":
                head_pos_x -= 1
            elif direction == "U":
                head_pos_y -= 1
            elif direction == "D":
                head_pos_y += 1
                
            rope[0] = (head_pos_x, head_pos_y)
                
            for tail_index in range(1, len(rope)):
                follow_pos_x, follow_pos_y = rope[tail_index -1]
                tail_pos_x, tail_pos_y = rope[tail_index]
                
                diff_x = follow_pos_x - tail_pos_x
                diff_y = follow_pos_y - tail_pos_y
                
                if max(abs(diff_x), abs(diff_y)) >= 2:
                    tail_pos_x += sign(diff_x)
                    tail_pos_y += sign(diff_y)
                
                rope[tail_index] = (tail_pos_x, tail_pos_y)
            
            visited_positions.add(rope[-1])
                    
    num_visisted_positions = len(visited_positions)
    
    print(f"In my suddenly tangible though experiment, the tail of the rope will visit {num_visisted_positions} positions at least once. If I arc my body just like so I should be able to avoid them all...")