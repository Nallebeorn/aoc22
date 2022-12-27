import os
import sys
from functools import *
from time import perf_counter
from collections import deque
from math import factorial
from itertools import combinations

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~
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
    def __init__(self, my_location, el_location, my_distance_left, el_distance_left, pressure_released, time_remaining, remaining_valves, my_path, el_path):
        self.my_location = my_location
        self.el_location = el_location
        self.my_distance_left = my_distance_left
        self.el_distance_left = el_distance_left
        self.pressure_released = pressure_released
        self.time_remaining = time_remaining
        self.remaining_valves = remaining_valves
        self.my_path = my_path
        self.el_path = el_path


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
    frontier.append(Node("AA", "AA", 0, 0, 0, 26, remaining_valves, ["AA"], ["AA"]))

    current_best: Node = None

    while len(frontier):
        cur = frontier.pop()

        if current_best != None:
            best_possible = cur.pressure_released
            for valve in cur.remaining_valves:
                best_possible += valve_flow_rates[valve] * cur.time_remaining

            if best_possible < current_best.pressure_released:
                continue

        if cur.my_location == cur.el_location:
            for my_next, el_next in combinations(cur.remaining_valves, 2):
                my_distance = distances[(cur.my_location, my_next)]
                el_distance = distances[(cur.el_location, el_next)]
                my_new_time_remaining = cur.time_remaining - my_distance - 1
                el_new_time_remaining = cur.time_remaining - el_distance - 1
                if my_new_time_remaining > 0 and el_new_time_remaining > 0:
                    my_pressure = valve_flow_rates[my_next] * my_new_time_remaining
                    el_pressure = valve_flow_rates[el_next] * el_new_time_remaining
                    new_pressure_released = cur.pressure_released + my_pressure + el_pressure
                    new_remaning_valves = [v for v in cur.remaining_valves if v != my_next and v != el_next]
                    next_node = Node(my_next, el_next, my_distance + 1, el_distance + 1, new_pressure_released,
                                     cur.time_remaining, new_remaning_valves, cur.my_path + [my_next], cur.el_path + [el_next])
                    if current_best == None or new_pressure_released > current_best.pressure_released:
                        current_best = next_node
                    frontier.append(next_node)
        elif cur.my_distance_left <= 0:
            for next in cur.remaining_valves:
                distance = distances[(cur.my_location, next)]
                new_time_remaining = cur.time_remaining - distance - 1
                if new_time_remaining > 0:
                    new_pressure_released = cur.pressure_released + valve_flow_rates[next] * new_time_remaining
                    new_remaning_valves = [v for v in cur.remaining_valves if v != next]
                    next_node = Node(next, cur.el_location, distance + 1, cur.el_distance_left, new_pressure_released,
                                     cur.time_remaining, new_remaning_valves, cur.my_path + [next], cur.el_path)
                    if current_best == None or new_pressure_released > current_best.pressure_released:
                        current_best = next_node
                    frontier.append(next_node)
        elif cur.el_distance_left <= 0:
            for next in cur.remaining_valves:
                distance = distances[(cur.el_location, next)]
                new_time_remaining = cur.time_remaining - distance - 1
                if new_time_remaining > 0:
                    new_pressure_released = cur.pressure_released + valve_flow_rates[next] * new_time_remaining
                    new_remaning_valves = [v for v in cur.remaining_valves if v != next]
                    next_node = Node(cur.my_location, next, cur.my_distance_left, distance + 1, new_pressure_released,
                                     cur.time_remaining, new_remaning_valves, cur.my_path, cur.el_path + [next])
                    if current_best == None or new_pressure_released > current_best.pressure_released:
                        current_best = next_node
                    frontier.append(next_node)
        else:
            next_node = Node(cur.my_location, cur.el_location, cur.my_distance_left - 1, cur.el_distance_left - 1,
                             cur.pressure_released, cur.time_remaining - 1, cur.remaining_valves, cur.my_path, cur.el_path)
            frontier.append(next_node)

    print(current_best.my_path)
    print(current_best.el_path)
    print(f"* I quickly explained my plan to one of the elephants. I could now release {current_best.pressure_released} units of pressure working together as a team!")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")
