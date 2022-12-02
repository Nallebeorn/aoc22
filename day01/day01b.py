import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

print("DAY 01b")

with open("input.txt", "r") as file:
    lines = [line.strip() for line in file] + ['']

    elves_calories = []
    current_elf_calories = 0
    for line in lines:
        if line:
            current_elf_calories += int(line)
        else:
            elves_calories.append(current_elf_calories)
            current_elf_calories = 0

    elves_calories.sort(reverse = True)
    top_three_total_calories = sum(elves_calories[:3])

    print(f"The top three elves carrying the most calories are carrying a total of {top_three_total_calories} calories worth of food.")