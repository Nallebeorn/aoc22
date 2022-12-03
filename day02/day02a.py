import os
import sys
from functools import *

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 02/12 ~~~
""")

shape_to_score = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

result_matrix = {
    ("A", "X"): 3,
    ("B", "Y"): 3,
    ("C", "Z"): 3,

    ("A", "Y"): 6,
    ("B", "Z"): 6,
    ("C", "X"): 6,

    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("C", "Y"): 0,
}

with open("input.txt", "r") as file:
    games = [tuple(line.strip().split(" ")) for line in file]

    score = 0
    for (opponent_play, my_play) in games:
        score += shape_to_score[my_play]
        score += result_matrix[(opponent_play, my_play)]

    print(f"* If I follow the strategy guide fully, and its predictions are entirely nice and accurate, {score} should be my final score.")