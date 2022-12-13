import os
import sys
from functools import *
import ast

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 13/12 ~~~
""")

def compare_pair(left, right):
    for i in range(min(len(left), len(right))):
        l = left[i]
        r = right[i]
        print("compare", l, "vs", r)
        
        if isinstance(l, int) and isinstance(r, int):
            print("ints")
            if l < r:
                return True
            elif l > r:
                return False
        else:
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]
            
            result = compare_pair(l, r)
            if result != None:
                return result
            
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False
    
    return None

with open("input.txt", "r") as file:
    lines = [ast.literal_eval(line.strip()) for line in file if not line.isspace()]
    
    sum_of_indices_in_right_order = 0
    
    for i in range(0, len(lines), 2):
        left = lines[i]
        right = lines[i + 1]
        print("**", i // 2 + 1, "**")
        print(left, "vs", right)
        if compare_pair(left, right) > 0:
            sum_of_indices_in_right_order += i // 2 + 1
            print("RIGHT ORDER")
        else:
            print("WRONG ORDER")
        print("")
    
    print(sum_of_indices_in_right_order)