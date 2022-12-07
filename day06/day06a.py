import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 06/12 ~~~
""")

with open("input.txt", "r") as file:
    signal = file.read()

    for i in range(4, len(signal)):
        if len(set(signal[i-4:i])) == 4:
            print(f"* The first start-of-packet marker could be found after processing {i} characters in the datastream.")
            break
            
