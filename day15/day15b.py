import os
import sys
from functools import *
from time import perf_counter

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 15/12 ~~~
""")

start_time = perf_counter()

with open("input.txt", "r") as file:
    size = 4_000_000
    
    sensors = {}
    for data in [line.split() for line in file]:
        sensor_x = int("".join(c for c in data[2] if c.isdigit() or c == "-"))
        sensor_y = int("".join(c for c in data[3] if c.isdigit() or c == "-"))
        
        beacon_x = int("".join(c for c in data[-2] if c.isdigit() or c == "-"))
        beacon_y = int("".join(c for c in data[-1] if c.isdigit() or c == "-"))
        
        distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        
        sensors[(sensor_x, sensor_y)] = distance
        
    def find_distress_beacon():
        for y in range(0, size + 1):
            for x in range(0, size + 1):
                is_in_range_of_any_sensor = False
                
                for sensor_pos, sensor_distance in sensors.items():
                    sensor_x, sensor_y = sensor_pos
                    distance = abs(x - sensor_x) + abs(y - sensor_y)
                    
                    # if x == 9 and y == 19:
                    #     print("found correct pos", distance, sensor_distance, (sensor_x, sensor_y))
                    
                    if distance <= sensor_distance:
                        is_in_range_of_any_sensor = True
                        break
                
                if not is_in_range_of_any_sensor:
                    freq = x * 4_000_000 + y
                    print(x, y, freq)
                    return freq
    
        return None
        
    distress_beacon_tuning_freq = find_distress_beacon()
    
    print(f"* If my calculations are correct, then {distress_beacon_tuning_freq} is the tuning frequency of the only possible location of the distress beacon.")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")