import os
import sys
from functools import *
from time import perf_counter
from collections import deque
from math import factorial
import heapq

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 16/12 ~~~
""")

start_time = perf_counter()
    
def find_distance_between(start, end):
    queue = deque()
    queue.append(start)
    distance: dict[str, int] = {}
    distance[start] = 0
    
    while len(queue):
        room = queue.popleft()
        if room == end:
            break
            
        for to in valve_tunnels[room]:
            if to not in distance:
                distance[to] = distance[room] + 1
                queue.append(to)
    
    return distance[end]

class Node:
    def __init__(self, location, pressure_released, time_remaining, remaining_valves, path):
        self.location = location
        self.pressure_released = pressure_released
        self.time_remaining = time_remaining
        self.remaining_valves = remaining_valves
        self.path = path

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
    
    distances = {}
    for from_valve in valve_tunnels:
        for to_valve in valve_tunnels:
            distances[from_valve, to_valve] = find_distance_between(from_valve, to_valve)
            
    remaining_valves = [valve for valve in valve_flow_rates if valve_flow_rates[valve] > 0]
    
    frontier: "deque[Node]" = deque()
    frontier.append(Node("AA", 0, 30, remaining_valves, ["AA"]))
    
    current_best: Node = None
    
    while len(frontier):
        current = frontier.popleft()
        
        for next in current.remaining_valves:
            distance = distances[(current.location, next)]
            new_time_remaining = current.time_remaining - distance - 1
            if new_time_remaining > 0:
                new_pressure_released = current.pressure_released + valve_flow_rates[next] * new_time_remaining
                new_remaning_valves = [v for v in current.remaining_valves if v != next]
                next_node = Node(next, new_pressure_released, new_time_remaining, new_remaning_valves, current.path + [next])
                if current_best == None or new_pressure_released > current_best.pressure_released:
                    current_best = next_node
                frontier.append(next_node)
    
    print(f"* If I do this methodically I should be able to release {current_best.pressure_released} units of pressure and save the elephants and me before the volcano erupts!")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")