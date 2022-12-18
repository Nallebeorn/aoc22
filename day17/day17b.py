import os
import sys
from functools import *
from itertools import permutations
from time import perf_counter
from collections import deque

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
""")

start_time = perf_counter()
    
def find_path_between(start, end):
    queue = deque()
    queue.append(start)
    path: dict[str, list[str]] = {}
    path[start] = []
    
    while len(queue):
        room = queue.popleft()
        if room == end:
            break
            
        for to in valve_tunnels[room]:
            if to not in path:
                path[to] = path[room] + [to]
                queue.append(to)
    
    return path[end]

class Node:
    def __init__(self, my_location, elephant_location, pressure_released, time_remaining, remaining_valves, my_path, elephant_path, my_goal = None, elephant_goal = None):
        self.my_location = my_location
        self.elephant_location = elephant_location
        self.pressure_released = pressure_released
        self.time_remaining = time_remaining
        self.remaining_valves = remaining_valves
        self.my_path = my_path + ([my_location] if my_goal == None else [])
        self.elephant_path = elephant_path + ([elephant_location] if elephant_goal == None else [])
        self.my_goal = my_goal
        self.elephant_goal = elephant_goal

with open("input.txt", "r") as file:
    valves_input = [line.split() for line in file]
    
    valve_flow_rates = {}
    valve_tunnels = {}
    for data in valves_input:
        name = data[1]
        flow_rate_info = data[4]
        flow_rate = int("".join(c for c in flow_rate_info if c.isdigit()))
        tunnels_to = [valve.strip(",") for valve in data[9:]]
        valve_flow_rates[name] = flow_rate
        valve_tunnels[name] = tunnels_to
    
    paths = {}
    for from_valve in valve_tunnels:
        for to_valve in valve_tunnels:
            paths[from_valve, to_valve] = find_path_between(from_valve, to_valve)

    remaining_valves = [valve for valve in valve_flow_rates if valve_flow_rates[valve] > 0]
    
    frontier: "deque[Node]" = deque()
    frontier.append(Node("AA", "AA", 0, 26, remaining_valves, [], []))
    
    current_best: Node = None
    
    while len(frontier):
        current = frontier.popleft()
        
        if current.my_goal != None and current.elephant_goal != None:
            valve_targets = [(current.my_goal, current.elephant_goal)]
        elif current.my_goal != None:
            valve_targets = [(current.my_goal, v) for v in current.remaining_valves]
        elif current.elephant_goal != None:
            valve_targets = [(v, current.elephant_goal) for v in current.remaining_valves]
        else:
            valve_targets = permutations(current.remaining_valves, 2)
        
        for my_next, elephant_next in valve_targets:
            my_path = paths[(current.my_location, my_next)] + [my_next]
            elephant_path = paths[(current.elephant_location, elephant_next)] + [elephant_next]
            
            my_distance = len(my_path)
            elephant_distance = len(elephant_path)
            
            new_time_remaining = current.time_remaining - min(my_distance, elephant_distance)
            new_remaining_valves = [v for v in current.remaining_valves if v != my_next and v != elephant_next]
            
            if new_time_remaining > 0:
                if my_distance == elephant_distance:
                    new_pressure_released = current.pressure_released + (valve_flow_rates[my_next] + valve_flow_rates[elephant_next]) * new_time_remaining
                    
                    next_node = Node(my_next, elephant_next, new_pressure_released, new_time_remaining, new_remaining_valves, current.my_path, current.elephant_path, None, None)
                elif my_distance < elephant_distance:
                    new_pressure_released = current.pressure_released + valve_flow_rates[my_next] * new_time_remaining
                    
                    elephant_short_next = elephant_path[my_distance - 1]
                    next_node = Node(my_next, elephant_short_next, new_pressure_released, new_time_remaining, new_remaining_valves, current.my_path, current.elephant_path, None, elephant_next)
                elif elephant_distance < my_distance:
                    new_pressure_released = current.pressure_released + valve_flow_rates[elephant_next] * new_time_remaining
                    
                    my_short_next = my_path[elephant_distance - 1]
                    next_node = Node(my_short_next, elephant_next, new_pressure_released, new_time_remaining, new_remaining_valves, current.my_path, current.elephant_path, my_next, None)
                    
                if current_best == None or new_pressure_released > current_best.pressure_released:
                    current_best = next_node
                frontier.append(next_node)
    
    print(f"* If I do this methodically I should be able to release {current_best.pressure_released + 2} units of pressure and save the elephants and me before the volcano erupts!")
    print(current_best.my_path)
    print(current_best.elephant_path)

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")