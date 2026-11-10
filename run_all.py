import subprocess
import sys

steps = ["make_data.py", "validate.py", "cluster2.py", "charts.py"]

for script in steps:
    print(f"\n=== Running {script} ===")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"STOPPED: {script} failed")
        sys.exit(1)

print("\nAll steps finished. Check the data and charts folders.")