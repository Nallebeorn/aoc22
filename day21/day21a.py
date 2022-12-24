import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 21/12 ~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    monkeys = {words[0][:-1]: int(words[1]) if words[1].isdigit() else tuple(words[1:]) for words in [line.strip().split() for line in file]}

def find_monkey_number(monkey):
    job = monkeys[monkey]
    if isinstance(job, int):
        return job
    else:
        left, operator, right = job
        left_num = find_monkey_number(left)
        right_num = find_monkey_number(right)
        if operator == "+":
            return left_num + right_num
        elif operator == "-":
            return left_num - right_num
        elif operator == "*":
            return left_num * right_num
        elif operator == "/":
            return left_num // right_num
        else:
            raise "Invalid monkey operator"
    
root_number = find_monkey_number("root")

print(f"* I predict that the monkey who goes by name Root is going to yell the number {root_number} at the end of this cacophony.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")