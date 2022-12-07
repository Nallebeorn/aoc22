import os
import sys
import time
from runpy import run_path

day_folders_contents = [[os.path.join(root, file) for file in files] for root, dirs, files in os.walk(os.path.dirname(sys.argv[0])) if "day" in root]
scripts = sorted([script for folder in day_folders_contents for script in folder if script.endswith(".py")]) # flatten

start_time = time.perf_counter()
for script in scripts:
    run_path(script)
    print("")
    if (script.endswith("b.py")):
        print("")        
end_time = time.perf_counter()

elapsed_time = end_time - start_time

print(f"Running all scripts took {elapsed_time * 1000}ms")