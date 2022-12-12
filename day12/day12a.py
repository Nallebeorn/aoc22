import os
import sys
from functools import *
import heapq

os.chdir(os.path.dirname(sys.argv[0]))

print(
"""~~~ 12/12 ~~~
""")

with open("input.txt", "r") as file:
    lines = file.read().splitlines()
    width = len(lines[0])
    inputmap = "".join(lines)
    
    start = inputmap.index("S")
    end = inputmap.index("E")
    heightmap = [ord(c) - ord("a") for c in inputmap.replace("S", "a").replace("E", "z")]
    graph = []
    for i in range(len(heightmap)):
        x = i % width
        max_height = heightmap[i] + 1
        edges = set()
        graph.append(edges)
        if x - 1 >= 0 and heightmap[i - 1] <= max_height:
            edges.add(i - 1)
        if x + 1 < width and heightmap[i + 1] <= max_height:
            edges.add(i + 1)
        if i - width >= 0 and heightmap[i - width] <= max_height:
            edges.add(i - width)
        if i + width < len(heightmap) and heightmap[i + width] <= max_height:
            edges.add(i + width)
    
    frontier = []
    heapq.heappush(frontier, (0, start))
    closed_set = set()
    shortest_path_so_far_to = {start: 0}
    
    end_x = end % width
    end_y = end // width
    
    while frontier:
        current = heapq.heappop(frontier)[1]
        
        if current == end:
            break
        
        for next in graph[current]:
            new_cost = shortest_path_so_far_to[current] + 1
            if next not in shortest_path_so_far_to or new_cost < shortest_path_so_far_to[next]:
                shortest_path_so_far_to[next] = new_cost
                
                next_x = next % width
                next_y = next // width
                heuristic = abs(end_x - next_x) + abs(end_y - next_y)
                
                priority = new_cost + heuristic
                
                heapq.heappush(frontier, (priority, next))
                
    shortest_path_to_goal = shortest_path_so_far_to[end]
    
    print(f"* I will have to travel at least {shortest_path_to_goal} steps if I want to climb the hill where I could get the best signal.")