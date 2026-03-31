"""All Draw Modes Example

This example demonstrates all four mr-dapa drawer types:
StaticGlobalPlotDrawer, StaticSeparatePlotDrawer, StaticGroupPlotDrawer, and AnimationDrawer.
"""

import mr_dapa as mrdp

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'map': {'title': 'Map', 'class': 'MapComponent'},
}

# 1. StaticGlobal - all robots in shared subplots
print("Creating StaticGlobal plot...")
drawer1 = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
fig1 = drawer1.draw(['x', 'map'], save=True, path='static_global.png')
print("  -> static_global.png")

# 2. StaticSeparate - one figure per robot
print("Creating StaticSeparate plots...")
drawer2 = mrdp.StaticSeparatePlotDrawer(files=['data.json'], components=components)
figs2 = drawer2.draw(['x', 'map'], save=True)
print(f"  -> {len(figs2)} separate figures")

# 3. StaticGroup - per-robot subplots in one figure
print("Creating StaticGroup plot...")
drawer3 = mrdp.StaticGroupPlotDrawer(files=['data.json'], components=components)
fig3 = drawer3.draw(['x', 'map'], save=True, path='static_group.png')
print("  -> static_group.png")

# 4. Animation - MP4 animation
print("Creating Animation...")
drawer4 = mrdp.AnimationDrawer(files=['data.json'], components=components)
fig4 = drawer4.draw(['x', 'map'], time_ratio=2, save=True, path='animation.mp4')
print("  -> animation.mp4")

print("\nAll draw modes example complete!")
