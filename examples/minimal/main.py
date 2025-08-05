from mr_dapa.drawers.drawers import *

components = {
    'x': {
        'title': 'X Position',
        'class': 'LinesComponent',
        'keys': ['x'],
        'filename': 'x',
        'figsize': (6, 6),
    },
    'y': {
        'title': 'Y Position',
        'class': 'LinesComponent',
        'keys': ['y'],
        'filename': 'y',
        'figsize': (12, 8),
    },
    'xy-line': {
        'title': 'X & Y Position, Separated',
        'class': 'LinesComponent',
        'keys': ['x', 'y'],
        'filename': 'xy-line',
        'figsize': (12, 6),
    }
}


def minimal_main():
    file = 'data.json'

    StaticGlobalPlotDrawer([file]).register_components(components).draw(['x', 'y'])

    StaticGlobalPlotDrawer([file]).register_components(components).set_id_list([2, 3]).draw(['xy-line'])

    StaticGlobalPlotDrawer([file]).register_components(components).set_time_range((0.2, 0.5)).draw(['x', 'y'])

    StaticGlobalPlotDrawer([file]).register_components(components).set_last_seconds(2).draw(['x', 'y'])

    StaticSeparatePlotDrawer([file]).register_components(components).draw(['x'])

    StaticSeparatePlotDrawer([file]).register_components(components).set_first_seconds(2).draw(['x', 'y'])

    StaticGroupPlotDrawer([file]).register_components(components).draw(['x', 'y'])

    StaticGroupPlotDrawer([file]).register_components(components).set_time_range((0.2, 0.5)).set_id_list([1, 3]).draw(['x', 'y'])


if __name__ == '__main__':
    minimal_main()
