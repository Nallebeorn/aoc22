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
    
    num_rounds = 20
    for i in range(num_rounds):
        for monkey_idx, monkey in enumerate(monkeys):
            # print(f"Monkey {monkey_idx}:")
            while len(monkey.items):
                item = monkey.items.pop(0)
                # print(f"\tMonkey inspects an item with a worry level of {item}.")
                monkey.business += 1
                
                op_arg = item if monkey.operation_arg == "old" else int(monkey.operation_arg)
                if monkey.operation_op == "*":
                    item *= op_arg
                    # print(f"\t\tWorry level is multiplied by {monkey.operation_arg.replace('old', 'itself')} to {item}.")
                elif monkey.operation_op == "+":
                    item += op_arg
                    # print(f"\t\tWorry level increases by {monkey.operation_arg.replace('old', 'itself')} to {item}.")
                    
                item = item // 3
                # print(f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {item}.")
                
                if item % monkey.test_divisible_by == 0:
                    # print(f"\t\tCurrent worry level is not divisible by {monkey.test_divisible_by}.")
                    # print(f"\t\tItem with worry level {item} is thrown to monkey {monkey.if_true_throw_to}.")
                    monkeys[monkey.if_true_throw_to].items.append(item)
                else:
                    # print(f"\t\tCurrent worry level is divisible by {monkey.test_divisible_by}.")
                    # print(f"\t\tItem with worry level {item} is thrown to monkey {monkey.if_false_throw_to}.")
                    monkeys[monkey.if_false_throw_to].items.append(item)
                    
    # print("")
    # for monkey_idx, monkey in enumerate(monkeys):
    #     print(f"Monkey {monkey_idx} inspected items {monkey.business} times.")
    # print("")
    
    monkey_business_leaderboard = sorted([monkey.business for monkey in monkeys], reverse=True)
    monkey_business_tally = monkey_business_leaderboard[0] * monkey_business_leaderboard[1]
    
    print(f"The level of monkey business has alrady reached {monkey_business_tally} after 20 rounds of stuff-slinging simian shenanigans!")