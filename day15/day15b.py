import os
import sys
from functools import *
from time import perf_counter
from operator import itemgetter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 15/12 ~~~
""")

start_time = perf_counter()

def merge_ranges(ranges):
    out_ranges = sorted(ranges, key=itemgetter(0))
    
    out_index = 0
    
    for i in range(1, len(out_ranges)):
        start1, end1 = out_ranges[out_index]
        start2, end2 = out_ranges[i]
        if end1 >= start2:
            out_ranges[out_index] = (start1, max(end1, end2))
        else:
            out_index += 1
            out_ranges[out_index] = out_ranges[i]
            
    return out_ranges[0:out_index+1]

with open("input.txt", "r") as file:
    size = 4_000_000
    
    covered_rows = [[] for i in range(size + 1)]
    covered_columns = [[] for i in range(size + 1)]
    
    print("Read sensors")
    
    for data in [line.split() for line in file]:
        sensor_x = int("".join(c for c in data[2] if c.isdigit() or c == "-"))
        sensor_y = int("".join(c for c in data[3] if c.isdigit() or c == "-"))
        print("Sensor:", sensor_x, sensor_y)
        
        beacon_x = int("".join(c for c in data[-2] if c.isdigit() or c == "-"))
        beacon_y = int("".join(c for c in data[-1] if c.isdigit() or c == "-"))
        
        distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        
        min_x = max(0, sensor_x - distance)
        max_x = min(size, sensor_x + distance)
        min_y = max(0, sensor_y - distance)
        max_y = min(size, sensor_y + distance)
        
        for column in range(min_x, max_x + 1):
            cross_dist = distance - abs(sensor_x - column)
            
            y1 = sensor_y - cross_dist
            y2 = sensor_y + cross_dist
            covered_columns[column].append((y1, y2))
        
        for row in range(min_y, max_y + 1):
            cross_dist = distance - abs(sensor_y - row)
            
            x1 = sensor_x - cross_dist
            x2 = sensor_x + cross_dist
            covered_rows[row].append((x1, x2))
            
    print("Merge ranges")
    
    candidates_x = []
    candidates_y = []
    
    for i in range(len(covered_rows)):
        if i % 100_000 == 0:
            print("Range no:", i)
        merged_rows = merge_ranges(covered_rows[i])
        merged_columns = merge_ranges(covered_columns[i])
        if len(merged_rows) > 1:
            candidates_x.append((i, merged_rows[0][1] + 1))
        if len(merged_columns) > 1:
            candidates_y.append((i, merged_columns[0][1] + 1))
        
    print("Find beacon")
    
    for column, y in candidates_y:
        for row, x in candidates_x:
            print("Candidate position:", x, y)
            if column == x and row == y:
                tuning_frequency = x * 4_000_000 + y
                print(f"* If my calculations are correct, then {tuning_frequency} is the tuning frequency of the only possible location of the distress beacon.")
                break

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")