import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 01/12 ~~~
""")

with open("input.txt", "r") as file:
    lines = [line.strip() for line in file] + ['']

    highest_calories_yet = 0
    current_elf_calories = 0
    for line in lines:
        if line:
            current_elf_calories += int(line)
        else:
            if current_elf_calories > highest_calories_yet:
                highest_calories_yet = current_elf_calories
            current_elf_calories = 0

    print(f"* Having processed the list, it appears the elf carrying the most calories is carrying a whooping {highest_calories_yet} calories worth of food!")