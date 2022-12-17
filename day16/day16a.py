import os
import sys
from functools import *
from time import perf_counter
from collections import deque

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 16/12 ~~~
""")

start_time = perf_counter()
    
class State:
    def __init__(self, location, path_since_open, pressure_release, time_remaining, opened_valves):
        self.location = location
        self.path_since_open = path_since_open
        self.pressure_release = pressure_release
        self.time_remaining = time_remaining
        self.opened_valves = opened_valves

    def __repr__(self):
        return f"{'*' if self.location in self.opened_valves else ''}{self.location} | {self.time_remaining}s | {self.pressure_release}"

with open("input.txt", "r") as file:
    valves_input = [line.split() for line in file]
    
    valves = {}
    for data in valves_input:
        name = data[1]
        flow_rate_info = data[4]
        flow_rate = int("".join(c for c in flow_rate_info if c.isdigit()))
        tunnels_to = [valve.strip(",") for valve in data[9:]]
        valves[name] = (flow_rate, tunnels_to)
    
    queue: "deque[State]" = deque()
    queue.append(State("AA", [], 0, 30, ["AA"])) # AA's valve hasn't been opened but it's flow rate is 0 so we can consider it opened
    
    current_best: State = None
    
    current_highest_pressure = 0
    
    num_valves_to_open = len([flow_rate for flow_rate, tunnels in valves.values() if flow_rate > 0]) + 1
    
    while len(queue):
        state = queue.popleft()
        flow_rate, tunnels = valves[state.location]
        
        current_highest_pressure = max(current_highest_pressure, state.pressure_release)
        
        best_possible_remaining = state.pressure_release
        for valve in valves:
            if valve not in state.opened_valves:
                best_possible_remaining += valves[valve][0] * (state.time_remaining - 1)
        if best_possible_remaining < current_highest_pressure:
            continue
        
        print(state, "::", best_possible_remaining, "/", current_highest_pressure, "::", len(state.opened_valves), "/", len(valves))
        
        if state.time_remaining > 0 and len(state.opened_valves) < num_valves_to_open:
            if flow_rate > 0 and state.location not in state.opened_valves:
                pressure_released = flow_rate * (state.time_remaining - 1)
                queue.append(State(state.location, [], state.pressure_release + pressure_released, state.time_remaining - 1, state.opened_valves + [state.location]))
            
            for to in tunnels:
                if to not in state.path_since_open:
                    queue.append(State(to, state.path_since_open + [to], state.pressure_release, state.time_remaining - 1, state.opened_valves))
        else:
            if current_best == None or state.pressure_release > current_best.pressure_release:
                current_best = state
    
    print(f"If I do this methodically I should be able to release {current_best.pressure_release} units of pressure and save the elephants and me before the volcano erupts!")

end_time = perf_counter()
print(f"[took {(end_time - start_time) * 1000}ms]")