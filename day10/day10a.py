import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 10/12 ~~~
""")

cycle = 0
total_signal_strength = 0
reg_x = 1

def advance_cycle():
    global cycle, total_signal_strength, reg_x
    cycle += 1
    if (cycle - 20) % 40 == 0:
        total_signal_strength += reg_x * cycle

with open("input.txt", "r") as file:
    instructions = [line.split() for line in file]
    
    cycle = 0
    
    for instruction in instructions:
        opcode = instruction[0]
        advance_cycle()
        if opcode == "addx":
            advance_cycle()
            reg_x += int(instruction[1])
            
print(f"Analyzing the programming of this most peculiar processor, I can see that {total_signal_strength} is the sum of the signal strengths of interest.")