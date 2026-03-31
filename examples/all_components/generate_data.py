"""Generate sample data for the all_components example."""

import json
import numpy as np

np.random.seed(42)

num_robots = 3
duration = 5.0
fps = 20
num_steps = int(duration * fps)
timestamps = np.linspace(0, duration, num_steps).tolist()

data = []
for robot_id in range(1, num_robots + 1):
    x = [5 * np.cos(2 * np.pi * 0.1 * t + robot_id) for t in timestamps]
    y = [5 * np.sin(2 * np.pi * 0.1 * t + robot_id) for t in timestamps]
    battery = [100 - 5 * t + np.random.randn() * 0.5 for t in timestamps]

    data.append({
        "id": robot_id,
        "timestamp": timestamps,
        "values": [
            {"name": "X Position", "alias": "x", "unit": "m", "value": x},
            {"name": "Y Position", "alias": "y", "unit": "m", "value": y},
            {"name": "Battery", "alias": "battery", "unit": "%", "value": battery},
        ]
    })

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Generated data.json")
