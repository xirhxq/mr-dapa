"""Generate sample data for the with_menu example."""

import json
import numpy as np
import os

np.random.seed(42)

num_robots = 3
duration = 5.0
fps = 20
num_steps = int(duration * fps)
timestamps = np.linspace(0, duration, num_steps).tolist()

# Create one data file per robot
for robot_id in range(1, num_robots + 1):
    x = [5 * np.cos(2 * np.pi * 0.1 * t + robot_id) for t in timestamps]
    y = [5 * np.sin(2 * np.pi * 0.1 * t + robot_id) for t in timestamps]

    data = [{
        "id": robot_id,
        "timestamp": timestamps,
        "values": [
            {"name": "X Position", "alias": "x", "unit": "m", "value": x},
            {"name": "Y Position", "alias": "y", "unit": "m", "value": y},
        ]
    }]

    filename = f'data_{robot_id}.json'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated {filename}")

print(f"\nGenerated {num_robots} data files in data/")
print("You can now run 'python ../main.py' from this directory.")
