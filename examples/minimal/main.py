from mr_dapa.drawers.drawers import *

components = {
    'x': {
        'title': 'X Position',
        'class': 'LinesComponent',
        'keys': ['x'],
        'figsize': (6, 6),
    },
    'x-with-bars': {
        'title': 'X Position',
        'class': 'LinesComponent',
        'keys': ['x'],
        'figsize': (6, 6),
        'bars': [-1, 0, 1],
    },
    'y': {
        'title': 'Y Position',
        'class': 'LinesComponent',
        'keys': ['y'],
        'figsize': (12, 8),
    },
    'y-with-range': {
        'title': 'Y Position',
        'class': 'LinesComponent',
        'keys': ['y'],
        'figsize': (12, 8),
        'range': [-0.5, 3.9]
    },
    'xy-line': {
        'title': 'X & Y Position, Separated',
        'class': 'LinesComponent',
        'keys': ['x', 'y'],
        'figsize': (12, 6),
    },
    'map': {
        'title': 'Map',
        'class': 'MapComponent',
        'figsize': (8, 8),
    }
}


def minimal_main():
    file = 'data.json'

    StaticGlobalPlotDrawer([file]).register_components(components).draw(['x', 'y'])

    StaticGlobalPlotDrawer([file]).register_components(components).draw(['x-with-bars', 'y-with-range'])

    StaticGlobalPlotDrawer([file]).register_components(components).set_id_list([2, 3]).draw(['xy-line'])

    StaticGlobalPlotDrawer([file]).register_components(components).set_time_range((0.2, 0.5)).draw(['x', 'y'])

    StaticGlobalPlotDrawer([file]).register_components(components).set_last_seconds(2).draw(['x', 'y'])

    StaticSeparatePlotDrawer([file]).register_components(components).draw(['x'])

    StaticSeparatePlotDrawer([file]).register_components(components).set_first_seconds(2).draw(['x', 'y'])

    StaticGroupPlotDrawer([file]).register_components(components).draw(['x', 'y'])

    StaticGroupPlotDrawer([file]).register_components(components).set_time_range((0.2, 0.5)).set_id_list([1, 3]).draw(['x', 'y'])

    AnimationDrawer([file]).register_components(components).draw(['x', 'y'])

    AnimationDrawer([file]).register_components(components).draw(['x', 'y'], time_ratio=2)

    AnimationDrawer([file]).register_components(components).set_time_range((0.2, 0.5)).draw(['x'])

    AnimationDrawer([file]).register_components(components).set_last_seconds(2).draw(['y'], fps=20)

    AnimationDrawer([file]).register_components(components).draw(['map'])

    AnimationDrawer([file]).register_components(components).set_time_range((0.2, 0.5)).draw(['map', 'xy-line'])

    AnimationDrawer([file]).register_components(components).set_last_seconds(2).set_id_list([1, 3]).draw(['map', 'x', 'y'])

if __name__ == '__main__':
    minimal_main()
