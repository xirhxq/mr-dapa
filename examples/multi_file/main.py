"""Multi-File Adapter Example

This example demonstrates loading and merging data from multiple JSON files,
where each file contains data for one or more robots.
"""

import mr_dapa as mrdp
from mr_dapa import MultiFileAdapter

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
}

# Load from multiple JSON files
import glob
file_list = sorted(glob.glob('data/robot_*.json'))

drawer = mrdp.StaticGlobalPlotDrawer(
    files=file_list,
    components=components,
    adapter=MultiFileAdapter()
)

fig = drawer.draw(['x', 'y'], save=True)
print(f"Multi-file example complete! Loaded {len(file_list)} files.")
