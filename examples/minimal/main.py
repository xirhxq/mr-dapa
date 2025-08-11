import mr_dapa as mrdp

components = {
    'x': {  # basic component for drawing X position
        'title': 'X Position',  # subplot title
        'class': 'LinesComponent',  # component to use
        'keys': ['x'],  # keys to plot
    },
    'x-with-bars': {
        'title': 'X Position',
        'class': 'LinesComponent',
        'keys': ['x'],
        'bars': [-1, 0, 1],  # customised horizontal lines
    },
    'y': {
        'title': 'Y Position',
        'class': 'LinesComponent',
        'keys': ['y'],
        'filename': 'ypos',  # customised saving filename
    },
    'y-with-range': {
        'title': 'Y Position',
        'class': 'LinesComponent',
        'keys': ['y'],
        'range': [-0.5, 3.9],  # customised grey area
    },
    'xy-line': {
        'title': 'X & Y Position, Separated',
        'class': 'LinesComponent',
        'keys': ['x', 'y'],
        'figsize': (12, 8),  # customised figure size
    },
    'map': {
        'title': 'Map',
        'class': 'MapComponent',  # 2d map component
    }
}


def minimal_main():
    file = 'data.json'

    # plot all x and all y in two subplots
    mrdp.StaticGlobalPlotDrawer([file]).register_components(components) \
        .draw(['x', 'y'])

    # plot all x and all y with customised bars and range
    mrdp.StaticGlobalPlotDrawer([file]).register_components(components) \
        .draw(['x-with-bars', 'y-with-range'])

    # we can specify which robots to plot
    mrdp.StaticGlobalPlotDrawer([file]).register_components(components) \
        .set_id_list([2, 3]) \
        .draw(['xy-line'])

    # we can also specify time range
    mrdp.StaticGlobalPlotDrawer([file]).register_components(components) \
        .set_time_range((0.2, 0.5)) \
        .draw(['x', 'y'])

    # also specify last seconds
    mrdp.StaticGlobalPlotDrawer([file]).register_components(components) \
        .set_last_seconds(2).draw(['x', 'y'])

    # plot x position per robot in separate plots
    mrdp.StaticSeparatePlotDrawer([file]).register_components(components) \
        .draw(['x'])

    # this mode also support customising time range
    mrdp.StaticSeparatePlotDrawer([file]).register_components(components) \
        .set_first_seconds(2) \
        .draw(['x', 'y'])

    # plot all x and all y per robot, but in one plot
    mrdp.StaticGroupPlotDrawer([file]).register_components(components) \
        .draw(['x', 'y'])

    # set time range and id list at the same time
    mrdp.StaticGroupPlotDrawer([file]).register_components(components) \
        .set_time_range((0.2, 0.5)) \
        .set_id_list([1, 3]) \
        .draw(['x', 'y'])

    # plot animation
    mrdp.AnimationDrawer([file]).register_components(components) \
        .draw(['x', 'y'])

    # speed up 2x
    mrdp.AnimationDrawer([file]).register_components(components) \
        .draw(['x', 'y'], time_ratio=2)

    # customising time range
    mrdp.AnimationDrawer([file]).register_components(components) \
        .set_time_range((0.2, 0.5)).draw(['x'])

    # customising last seconds, then specify fps
    mrdp.AnimationDrawer([file]).register_components(components) \
        .set_last_seconds(2).draw(['y'], fps=20)

    # plot 2d map
    mrdp.AnimationDrawer([file]).register_components(components) \
        .draw(['map'])

    # we could draw animation with multiple components
    mrdp.AnimationDrawer([file]).register_components(components) \
        .set_time_range((0.2, 0.5)) \
        .draw(['map', 'xy-line'])

    # we can also specify id list
    mrdp.AnimationDrawer([file]).register_components(components) \
        .set_last_seconds(2) \
        .set_id_list([1, 3]). \
        draw(['map', 'x', 'y'])


if __name__ == '__main__':
    minimal_main()
