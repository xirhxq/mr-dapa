"""Generate sample CSV files for the csv_adapter example."""

import csv
import numpy as np

np.random.seed(42)

num_robots = 3
duration = 5.0
fps = 20
num_steps = int(duration * fps)
timestamps = np.linspace(0, duration, num_steps)

with open('data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['robot_id', 'time', 'x', 'y', 'battery'])
    writer.writeheader()

    for robot_id in range(1, num_robots + 1):
        for i, t in enumerate(timestamps):
            x = 5 * np.cos(2 * np.pi * 0.1 * t + robot_id)
            y = 5 * np.sin(2 * np.pi * 0.1 * t + robot_id)
            battery = 100 - 5 * t + np.random.randn() * 0.5

            writer.writerow({
                'robot_id': robot_id,
                'time': round(t, 3),
                'x': round(x, 3),
                'y': round(y, 3),
                'battery': round(battery, 3)
            })

print("Generated data.csv")
