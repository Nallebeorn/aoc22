import os
import sys
from runpy import run_path

day_folders_contents = [[os.path.join(root, file) for file in files] for root, dirs, files in os.walk(os.path.dirname(sys.argv[0])) if "day" in root]
scripts = sorted([script for folder in day_folders_contents for script in folder if script.endswith(".py")]) # flatten

for script in scripts:
    run_path(script)
    print("")
    if (script.endswith("b.py")):
        print("")