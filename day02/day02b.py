import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

shape_to_score = {
    "A": 1,
    "B": 2,
    "C": 3,
}

result_to_score = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

shape_to_play = {
    ("A", "X"): "C",
    ("B", "X"): "A",
    ("C", "X"): "B",
    
    ("A", "Y"): "A",
    ("B", "Y"): "B",
    ("C", "Y"): "C",

    ("A", "Z",): "B",
    ("B", "Z",): "C",
    ("C", "Z",): "A",
    
}

with open("input.txt", "r") as file:
    games = [tuple(line.strip().split(" ")) for line in file]

    score = 0
    for (opponent_play, desired_result) in games:
        my_play = shape_to_play[(opponent_play, desired_result)]
        score += shape_to_score[my_play]
        score += result_to_score[desired_result]

    print(f"* If I follow the strategy guide fully, and its predictions are entirely nice and accurate, {score} should be my final result.")