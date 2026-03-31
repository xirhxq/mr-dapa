import os
import json
import numpy as np

ROBOT_NUM = 3
ROBOT_IDS = [i + 1 for i in range(ROBOT_NUM)]

TOTAL_TIME = 5
TIME_STEP = 0.02

keys = [
    {"name": "X Position", "alias": "x", "unit": "m", "noise": 0.01},
    {"name": "Y Position", "alias": "y", "unit": "m", "noise": 0.01},
    {"name": "Yaw Angle", "alias": "yaw", "unit": "rad", "noise": np.deg2rad(0.1)},
    {"name": "Battery Level", "alias": "batt", "unit": "mV", "noise": 0}
]

value_functions = {
    1: {
        "x": lambda t: np.sin(t / TOTAL_TIME * 2 * np.pi) * 2 + 3,
        "y": lambda t: np.cos(t / TOTAL_TIME * 2 * np.pi) * 2 + 3,
        "yaw": lambda t: t / TOTAL_TIME * 2 * np.pi - np.pi,
        "batt": lambda t: 4200 - t * 1000 / TOTAL_TIME,
    },
    2: {
        "x": lambda t: t * 0.5 - 1,
        "y": lambda t: 3 - t * 1,
        "yaw": lambda t: t / TOTAL_TIME * 2 * np.pi / 100 - np.pi / 2,
        "batt": lambda t: 3700 - t * 600 / TOTAL_TIME,
    },
    3: {
        "x": lambda t: t * (TOTAL_TIME - t),
        "y": lambda t: t * (TOTAL_TIME - t),
        "yaw": lambda t: t / TOTAL_TIME * 2 * np.pi / 10,
        "batt": lambda t: 3600 - t * 200 / TOTAL_TIME
    }
}

def generate_random_continuous_data(total_time, time_step, value_function, noise_level):
    timestamps = [i * time_step for i in range(int(total_time / time_step))]
    values = []
    for t in timestamps:
        offset = np.random.normal(0, noise_level)
        values.append(value_function(t) + offset)
    return timestamps, values

data = []
for id in ROBOT_IDS:
    data.append(
        {
            'id': id,
            'timestamp': [TIME_STEP * j for j in range(int(TOTAL_TIME / TIME_STEP))],
            'values': []
        }
    )
    for key in keys:
        timestamps, values = generate_random_continuous_data(
            TOTAL_TIME, TIME_STEP,
            value_functions[id][key["alias"]],
            key["noise"])
        data[-1]['values'].append(
            {
                "name": key["name"],
                "alias": key["alias"],
                "unit": key["unit"],
                "value": values,
            }
        )
with open(f"data.json", "w") as f:
    json.dump(data, f, indent=2)
