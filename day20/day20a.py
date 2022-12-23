import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 20/12 ~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    sequence = [(orig_index, int(original)) for orig_index, original in enumerate(file)]

def find_index_by_orig_index(sequence, orig_index):
    for i, element in enumerate(sequence):
        if element[0] == orig_index:
            return i

def find_index_by_value(sequence, value):
    for i, element in enumerate(sequence):
        if element[1] == value:
            return i

for orig_index in range(len(sequence)):
    from_index = find_index_by_orig_index(sequence, orig_index)
    orig_index, value = sequence[from_index]
    to_index = (from_index + value) % (len(sequence) - 1)
    sequence.pop(from_index)
    sequence.insert(to_index, (orig_index, value))

index_of_0 = find_index_by_value(sequence, 0)
coordinates_sum = sum(sequence[(index_of_0 + offset) % len(sequence)][1] for offset in [1000, 2000, 3000])
print(f"* After mixing the encrypted file once, I get {coordinates_sum} as the sum of the 3D coordinates, but this seems nonsensical.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")