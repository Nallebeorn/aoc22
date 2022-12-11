import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

cycle = 0
scanline_x = 0
reg_x = 1

screen_width = 40

screen_output = ""

def advance_cycle():
    global cycle, scanline_x, reg_x, screen_output
    
    cycle += 1
    scanline_x = (cycle - 1) % screen_width
    
    is_sprite_visible = scanline_x - 1 <= reg_x <= scanline_x + 1
        
    screen_output += "#" if is_sprite_visible else "."
    
    if scanline_x == screen_width - 1:
        screen_output += "\n"

with open("input.txt", "r") as file:
    instructions = [line.split() for line in file]
    
    cycle = 0
    
    for instruction in instructions:
        opcode = instruction[0]
        advance_cycle()
        if opcode == "addx":
            advance_cycle()
            reg_x += int(instruction[1])
        
print(f"* Running the program to completion would paint the following picture to the screen:\n\n{screen_output}")