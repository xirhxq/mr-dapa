"""NumPy Adapter Example

This example demonstrates loading data from NumPy arrays using NumPyAdapter.
"""

import numpy as np
import mr_dapa as mrdp
from mr_dapa import NumPyAdapter

# Create sample data as NumPy arrays
np.random.seed(42)

num_robots = 3
timestamps = np.linspace(0, 5, 100)

data = {}
for robot_id in range(1, num_robots + 1):
    x = 5 * np.cos(2 * np.pi * 0.1 * timestamps + robot_id)
    y = 5 * np.sin(2 * np.pi * 0.1 * timestamps + robot_id)
    battery = 100 - 5 * timestamps + np.random.randn(len(timestamps)) * 0.5

    data[robot_id] = {
        'timestamps': timestamps,
        'values': {
            'x': x,
            'y': y,
            'battery': battery
        }
    }

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
}

# Load from NumPy dict
drawer = mrdp.StaticGlobalPlotDrawer(
    files=[None],  # NumPyAdapter ignores files
    components=components,
    adapter=NumPyAdapter()
)

# Manually set the data since NumPyAdapter needs it at load time
from mr_dapa.helpers.loader import DataLoader
loader = DataLoader([None], adapter=NumPyAdapter())
loader.data = NumPyAdapter().load(data)

drawer = mrdp.StaticGlobalPlotDrawer(
    files=[None],
    components=components,
    adapter=NumPyAdapter()
)
drawer.data = NumPyAdapter().load(data)
drawer.interpreter = drawer.interpreter.__class__(drawer.data)

fig = drawer.draw(['x', 'y'], save=True)
print("NumPy adapter example complete!")
