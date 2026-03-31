"""Generate sample JSON files for the multi_file example."""

import json
import numpy as np
import os

os.makedirs('data', exist_ok=True)

np.random.seed(42)

num_files = 3
robots_per_file = 1
duration = 5.0
fps = 20
num_steps = int(duration * fps)
timestamps = np.linspace(0, duration, num_steps).tolist()

for file_idx in range(num_files):
    robot_id = file_idx + 1

    x = [5 * np.cos(2 * np.pi * 0.1 * t + robot_id) for t in timestamps]
    y = [5 * np.sin(2 * np.pi * 0.1 * t + robot_id) for t in timestamps]
    battery = [100 - 5 * t + np.random.randn() * 0.5 for t in timestamps]

    data = [{
        "id": robot_id,
        "timestamp": timestamps,
        "values": [
            {"name": "X Position", "alias": "x", "unit": "m", "value": x},
            {"name": "Y Position", "alias": "y", "unit": "m", "value": y},
            {"name": "Battery", "alias": "battery", "unit": "%", "value": battery},
        ]
    }]

    with open(f'data/robot_{robot_id}.json', 'w') as f:
        json.dump(data, f, indent=2)

print(f"Generated {num_files} JSON files in data/")
