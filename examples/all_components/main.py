"""All Components Example

This example demonstrates all four visualization components:
LinesComponent, MapComponent, ScatterComponent, and FillComponent.
"""

import mr_dapa as mrdp

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
    'map': {'title': 'Robot Map', 'class': 'MapComponent'},
    'phase': {'title': 'Phase Plot', 'class': 'ScatterComponent', 'x_key': 'x', 'y_key': 'y'},
    'range': {'title': 'Value Range', 'class': 'FillComponent', 'keys': ['x', 'y']},
}

drawer = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)

# Draw all components in one figure
fig1 = drawer.draw(['x', 'y', 'map', 'phase', 'range'], save=True)
print("All components example complete!")
print("Generated: x (Lines), y (Lines), map (Map), phase (Scatter), range (Fill)")
