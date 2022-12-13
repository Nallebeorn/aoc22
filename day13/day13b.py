import os
import sys
from functools import *
import ast

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

def compare_pair(left, right):
    for i in range(min(len(left), len(right))):
        l = left[i]
        r = right[i]
        
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return -1
            elif l > r:
                return 1
        else:
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]
            
            result = compare_pair(l, r)
            if result != 0:
                return result
            
    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1
    
    return 0

with open("input.txt", "r") as file:
    divider_packets = [[[2]], [[6]]]
    lines = [ast.literal_eval(line.strip()) for line in file if not line.isspace()]
    
    sorted_packets = sorted(lines + divider_packets, key=cmp_to_key(compare_pair))
    
    decoder_key = 1
    for i, packet in enumerate(sorted_packets):
        if packet in divider_packets:
            decoder_key *= i + 1
    
    print(f"* I have now painstakingly rearranged every packet into the correct order. Analyzing the divider packets, it seems {decoder_key} is the decoder key.")