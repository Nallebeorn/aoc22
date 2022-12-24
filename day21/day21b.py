import os
import sys
from functools import *
from time import perf_counter
from collections import deque

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    monkeys = {words[0][:-1]: int(words[1]) if words[1].isdigit() else tuple(words[1:]) for words in [line.strip().split() for line in file]}

root_left, _, root_right = monkeys["root"]
monkeys["root"] = (root_left, "=", root_right)

monkey_numbers = {}

def find_monkey_number(monkey):
    job = monkeys[monkey]
    if isinstance(job, int):
        return job
    else:
        left, operator, right = job
        left_num = find_monkey_number(left)
        right_num = find_monkey_number(right)

        monkey_numbers[left] = left_num
        monkey_numbers[right] = right_num

        if operator == "+":
            return left_num + right_num
        elif operator == "-":
            return left_num - right_num
        elif operator == "*":
            return left_num * right_num
        elif operator == "/":
            return left_num // right_num
        elif operator == "=":
            return (left, right)
        else:
            raise Exception("Invalid monkey operator")


def trace_to_human(start):
    monkey_listeners = {}

    frontier = deque()
    frontier.append(start)

    while len(frontier) > 0:
        monkey = frontier.popleft()

        if monkey == "humn":
            break
        
        if isinstance(monkeys[monkey], int):
            continue

        left, op, right = monkeys[monkey]
        monkey_listeners[left] = (monkey, op, monkey_numbers[right], "right")
        monkey_listeners[right] = (monkey, op, monkey_numbers[left], "left")
        frontier.append(left)
        frontier.append(right)

    path = []
    monkey = "humn"

    while monkey in monkey_listeners:
        path.append(monkey_listeners[monkey][1:])
        monkey = monkey_listeners[monkey][0]
    
    path.reverse()

    return path

def reverse_engineer_number(path, start_num):
    yell = start_num

    for op, arg, side in path:
        if op == "-":
            if side == "right":
                yell = yell + arg
            elif side == "left":
                yell = arg - yell
        elif op == "+":
            yell = yell - arg
        elif op == "/":
            if side == "right":
                yell = yell * arg
            elif side == "left":
                yell = arg // yell
        elif op == "*":
            yell = yell // arg
        else:
            raise Exception("Invalid monkey operator " + str(op))
    
    return yell

root_left, root_right = find_monkey_number("root")
path_left = trace_to_human(root_left)
path_right = trace_to_human(root_right)

if len(path_left) == 0:
    my_number = reverse_engineer_number(path_right, monkey_numbers[root_left])
else:
    my_number = reverse_engineer_number(path_left, monkey_numbers[root_right])

monkeys["humn"] = my_number
root_left, root_right = find_monkey_number("root")

print(f"* I must apparently yell the number {my_number} at the top of my lungs in order to satisfy the monkeys' game.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")