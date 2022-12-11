import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 11/12 ~~~
""")

class Monkey:
    def __init__(self, input):
        self.items = [int(worry_level) for worry_level in input[0].split(", ")]
        self.operation_op, self.operation_arg = input[1].split()[-2:]
        self.test_divisible_by = int(input[2].split()[-1])
        self.if_true_throw_to = int(input[3].split()[-1])
        self.if_false_throw_to = int(input[4].split()[-1])
        
        self.business = 0
        
    def __repr__(self):
        return "Monkey: " + str(self.__dict__, )
    

with open("input.txt", "r") as file:
    monkeys_input = [["".join(line.split(":")[1:]).strip() for line in monkey.splitlines()[1:]] for monkey in file.read().split("\n\n")]
    monkeys = [Monkey(input) for input in monkeys_input]
    print(monkeys)
    
    num_rounds = 10_000
    for i in range(num_rounds):
        print(i)
        for monkey_idx, monkey in enumerate(monkeys):
            # print(f"Monkey {monkey_idx}:")
            while len(monkey.items):
                item = monkey.items.pop(0)
                monkey.business += 1
                
                op_arg = item if monkey.operation_arg == "old" else int(monkey.operation_arg)
                if monkey.operation_op == "*":
                    item *= op_arg
                elif monkey.operation_op == "+":
                    item += op_arg
                
                if item % monkey.test_divisible_by == 0:
                    monkeys[monkey.if_true_throw_to].items.append(item)
                else:
                    monkeys[monkey.if_false_throw_to].items.append(item)
                    
        if i == 0 or i == 19 or (i + 1) % 1000 == 0:
            print(f"Round {i + 1}")
            for monkey_idx, monkey in enumerate(monkeys):
                print(f"Monkey {monkey_idx} inspected items {monkey.business} times.")
            print("")
        
    monkey_business_leaderboard = sorted([monkey.business for monkey in monkeys], reverse=True)
    monkey_business_tally = monkey_business_leaderboard[0] * monkey_business_leaderboard[1]
    
    print(f"The level of monkey business has alrady reached {monkey_business_tally} after 20 rounds of stuff-slinging simian shenanigans!")