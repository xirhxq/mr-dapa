import os
import json
import numpy as np

ROBOT_NUM = 3
ROBOT_IDS = [i + 1 for i in range(ROBOT_NUM)]

TOTAL_DATA_NUM = 5

TOTAL_TIME = 5
TIME_STEP = 0.1

keys = [
    {"name": "X Position", "alias": "x", "unit": "m", "tendency": "random"},
    {"name": "Y Position", "alias": "y", "unit": "m", "tendency": "random"},
    {"name": "Yaw Angle", "alias": "yaw", "unit": "rad", "tendency": "random"},
    {"name": "Battery Level", "alias": "batt", "unit": "mV", "tendency": "down"}
]

def generate_random_continuous_data(total_time, time_step, tendency, init_value, noise_level):
    timestamps = [i * time_step for i in range(int(total_time / time_step))]
    values = []
    value = init_value
    for t in timestamps:
        offset = np.random.normal(0, noise_level)
        if tendency == "up":
            value += abs(offset)
        elif tendency == "down":
            value -= abs(offset)
        else:
            value += offset
        values.append(value)
    return timestamps, values

for i in range(TOTAL_DATA_NUM):
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
            timestamps, values = generate_random_continuous_data(TOTAL_TIME, TIME_STEP, "up", 0, 0.1)
            data[-1]['values'].append(
                {
                    "name": key["name"],
                    "alias": key["alias"],
                    "unit": key["unit"],
                    "value": values,
                }
            )
    with open(f"data_{i + 1}.json", "w") as f:
        json.dump(data, f, indent=2)
