"""Publication Style Example

This example demonstrates how to customize plot appearance for publication
using style presets, palettes, and format options.
"""

import mr_dapa as mrdp

components = {
    'x': {'title': 'X Position (m)', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position (m)', 'class': 'LinesComponent', 'keys': ['y']},
    'map': {'title': 'Trajectory', 'class': 'MapComponent'},
}

# Paper preset: high DPI, publication-ready
print("Creating paper-style plot (PNG, high DPI)...")
drawer1 = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
drawer1.set_style('paper')
drawer1.draw(['x', 'y', 'map'], save=True, path='paper_style.png')

# Presentation preset: large figure, bold fonts
print("Creating presentation-style plot...")
drawer2 = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
drawer2.set_style('presentation').set_palette('vivid')
drawer2.draw(['x', 'y', 'map'], save=True, path='presentation_style.png')

# Dark theme
print("Creating dark theme plot...")
drawer3 = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
drawer3.set_style('dark')
drawer3.draw(['x', 'y', 'map'], save=True, path='dark_theme.png')

# Colorblind-friendly palette
print("Creating colorblind-friendly plot...")
drawer4 = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
drawer4.set_palette('colorblind')
drawer4.draw(['x', 'y', 'map'], save=True, path='colorblind_palette.png')

# SVG export for vector graphics
print("Creating SVG export...")
drawer5 = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
drawer5.style.format = 'svg'
drawer5.draw(['x', 'y', 'map'], save=True, path='vector_output.svg')

print("\nPublication style example complete!")
print("Generated: paper_style.png, presentation_style.png, dark_theme.png, colorblind_palette.png, vector_output.svg")
