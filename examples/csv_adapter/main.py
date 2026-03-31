"""CSV Adapter Example

This example demonstrates loading data from CSV files using CSVAdapter.
"""

import mr_dapa as mrdp
from mr_dapa import CSVAdapter

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
}

# Load from CSV with custom column names
drawer = mrdp.StaticGlobalPlotDrawer(
    files=['data.csv'],
    components=components,
    adapter=CSVAdapter(id_col='robot_id', timestamp_col='time', separator=',')
)

fig = drawer.draw(['x', 'y'], save=True)
print("CSV adapter example complete!")
