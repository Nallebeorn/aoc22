import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 20/12 ~~~
""")

start_time = perf_counter()

decryption_key = 811589153

with open("input.txt", "r") as file:
    sequence = [int(line) * decryption_key for line in file]
    original_indices = list(range(len(sequence)))

for mix_round in range(10):
    for orig_index in range(len(sequence)):
        from_index = original_indices.index(orig_index)
        value = sequence[from_index]
        to_index = (from_index + value) % (len(sequence) - 1)
        sequence.pop(from_index)
        sequence.insert(to_index, value)
        original_indices.pop(from_index)
        original_indices.insert(to_index, orig_index)

index_of_0 = sequence.index(0)
coordinates_sum = sum(sequence[(index_of_0 + offset) % len(sequence)] for offset in [1000, 2000, 3000])
print(f"* After mixing the encrypted file once, I get {coordinates_sum} as the sum of the 3D coordinates.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")