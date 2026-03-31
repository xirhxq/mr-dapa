"""Chain API Example

This example demonstrates the chain API for filtering and configuration.
"""

import mr_dapa as mrdp

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
    'map': {'title': 'Map', 'class': 'MapComponent'},
}

# Example 1: Filter by robot IDs
print("Example 1: Filter to robots 1 and 2")
drawer1 = (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_id_list([1, 2])
    .draw(['x', 'y', 'map'], save=True, path='robots_1_2.png'))

# Example 2: Filter by time range (first 2 seconds)
print("Example 2: First 2 seconds only")
drawer2 = (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_first_seconds(2.0)
    .draw(['x', 'y', 'map'], save=True, path='first_2_seconds.png'))

# Example 3: Filter by time range (last 2 seconds)
print("Example 3: Last 2 seconds only")
drawer3 = (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_last_seconds(2.0)
    .draw(['x', 'y', 'map'], save=True, path='last_2_seconds.png'))

# Example 4: Custom time range
print("Example 4: Time range 1-3 seconds")
drawer4 = (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_time_range((1.0, 3.0))
    .draw(['x', 'y', 'map'], save=True, path='time_1_to_3.png'))

# Example 5: Chain multiple filters + style
print("Example 5: Robot 3, middle 3 seconds, with colorblind palette")
drawer5 = (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_id_list([3])
    .set_time_range((1.5, 4.5))
    .set_palette('colorblind')
    .draw(['x', 'map'], save=True, path='robot3_middle_colorblind.png'))

# Example 6: Style customization chain
print("Example 6: All robots, presentation style with vivid palette")
drawer6 = (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_style('presentation')
    .set_palette('vivid')
    .draw(['x', 'y', 'map'], save=True, path='presentation_vivid.png'))

print("\nChain API example complete!")
print("Check the generated PNG files for each example.")
