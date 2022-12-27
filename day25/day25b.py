import os
import sys
from functools import *
from time import perf_counter
import heapq

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

start_time = perf_counter()

print("* FIN")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")