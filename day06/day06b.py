import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

with open("input.txt", "r") as file:
    signal = file.read()

    for i in range(14, len(signal)):
        if len(set(signal[i-14:i])) == 14:
            print(f"* The first start-of-packet marker could be found after processing {i} characters in the datastram.")
            break
            
