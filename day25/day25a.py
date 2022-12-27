import os
import sys
from functools import *
from time import perf_counter
import heapq

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 25/12
""")

start_time = perf_counter()

digit_to_value = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}
value_to_digit = {v: k for k, v in digit_to_value.items()}

def add_snafu(a: str, b: str):
    global digit_to_value, value_to_digit

    num_digits = max(len(a), len(b))
    a = a.zfill(num_digits)
    b = b.zfill(num_digits)
    carry = 0
    result = ""
    for i in reversed(range(num_digits)):
        digita = digit_to_value[a[i]]
        digitb = digit_to_value[b[i]]
        digit_sum = digita + digitb + carry
        if digit_sum > 2:
            digit_sum -= 5
            carry = 1
        elif digit_sum < -2:
            digit_sum += 5
            carry = -1
        else:
            carry = 0

        result = value_to_digit[digit_sum] + result

    if carry != 0:
        result = value_to_digit[carry] + result

    return result

with open("input.txt", "r") as file:
   snafu_numbers = file.read().splitlines()

total_fuel = "0"
for fuel in snafu_numbers:
    total_fuel = add_snafu(total_fuel, fuel)

print(f"* Expressed as a SNAFU number, {total_fuel} is the total fuel requirement. I should enter this into Bob's console!")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")