import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

from mr_dapa.components.lines import LinesComponent
from mr_dapa.components.map import MapComponent
from mr_dapa.components.search_heatmap import SearchHeatmapComponent
from mr_dapa.helpers.base_interpreter import BaseInterpreter
from mr_dapa.registry import get_component_class


class TestLinesComponentBasic:
    def test_creates_lines_for_single_key(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X Position', keys=['x'])
        assert len(comp.lines) == 3
        plt.close(fig)

    def test_creates_lines_for_multiple_keys(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X & Y', keys=['x', 'y'])
        assert len(comp.lines) == 6
        plt.close(fig)

    def test_can_hide_legend(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='X & Y', keys=['x', 'y'], show_legend=False)
        assert ax.get_legend() is None
        plt.close(fig)

    def test_axis_title(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='Test Title', keys=['x'])
        assert ax.get_title() == 'Test Title'
        plt.close(fig)

    def test_axis_xlabel(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='X', keys=['x'])
        assert ax.get_xlabel() == 'Time (s)'
        plt.close(fig)

    def test_custom_axis_labels(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(
            ax,
            interpreter,
            title='Coverage Sweep',
            keys=['x'],
            xlabel='Communication Range',
            ylabel='Final Coverage',
        )
        assert ax.get_xlabel() == 'Communication Range'
        assert ax.get_ylabel() == 'Final Coverage'
        plt.close(fig)

    def test_axis_ylabel_single_unit(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='X', keys=['x'])
        ylabel = ax.get_ylabel()
        assert '(m)' in ylabel
        plt.close(fig)

    def test_axis_ylabel_mixed_units(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='Mixed', keys=['x', 'batt'])
        ylabel = ax.get_ylabel()
        assert '(m)' not in ylabel
        plt.close(fig)

    def test_filtered_robot_count(self, sample_data):
        interp = BaseInterpreter(sample_data)
        filtered = interp.for_robots([1])
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, filtered, title='X', keys=['x'])
        assert len(comp.lines) == 1
        plt.close(fig)


class TestLinesComponentBarsAndRange:
    def test_bars_draws_horizontal_lines(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='X', keys=['x'], bars=[-1.0, 0.0, 1.0])
        hline_count = sum(1 for line in ax.get_lines() if line.get_linestyle() == '--')
        assert hline_count >= 3
        plt.close(fig)

    def test_range_draws_span(self, interpreter):
        fig, ax = plt.subplots()
        LinesComponent(ax, interpreter, title='X', keys=['x'], range=[-0.5, 0.5])
        from matplotlib.patches import Rectangle
        children = ax.get_children()
        rectangles = [c for c in children if isinstance(c, Rectangle)]
        assert len(rectangles) > 0
        plt.close(fig)


class TestMapComponent:
    def test_creates_markers(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        assert len(comp.robot_markers) == 3
        plt.close(fig)

    def test_custom_limits(self, interpreter):
        fig, ax = plt.subplots()
        MapComponent(ax, interpreter, title='Map', limits={'x': [-5, 5], 'y': [-5, 5]})
        assert ax.get_xlim() == (-5, 5)
        assert ax.get_ylim() == (-5, 5)
        plt.close(fig)

    def test_default_limits(self, interpreter):
        fig, ax = plt.subplots()
        MapComponent(ax, interpreter, title='Map')
        assert ax.get_xlim() == (-10, 10)
        assert ax.get_ylim() == (-10, 10)
        plt.close(fig)

    def test_title_is_set(self, interpreter):
        fig, ax = plt.subplots()
        MapComponent(ax, interpreter, title='Map')
        assert ax.get_title() == 'Map'
        plt.close(fig)

    def test_xlabel_has_unit(self, interpreter):
        fig, ax = plt.subplots()
        MapComponent(ax, interpreter, title='Map')
        xlabel = ax.get_xlabel()
        assert '(m)' in xlabel
        plt.close(fig)

    def test_ylabel_has_unit(self, interpreter):
        fig, ax = plt.subplots()
        MapComponent(ax, interpreter, title='Map')
        ylabel = ax.get_ylabel()
        assert '(m)' in ylabel
        plt.close(fig)

    def test_filtered_robot(self, sample_data):
        interp = BaseInterpreter(sample_data)
        filtered = interp.for_robots([2])
        fig, ax = plt.subplots()
        comp = MapComponent(ax, filtered, title='Map')
        assert len(comp.robot_markers) == 1
        assert 2 in comp.robot_markers
        plt.close(fig)

    def test_aspect_equal(self, interpreter):
        fig, ax = plt.subplots()
        MapComponent(ax, interpreter, title='Map')
        assert ax.get_aspect() in ('equal', 1.0)
        plt.close(fig)

    def test_trail_lines_created(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        assert len(comp.trail_lines) == 3
        plt.close(fig)

    def test_annotations_created(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        assert len(comp.robot_annotations) == 3
        plt.close(fig)


class TestSearchHeatmapComponent:
    def test_builds_first_search_time_grid(self):
        data = [{
            'id': 'global',
            'timestamp': [0.0, 1.0, 2.0],
            'values': [
                {
                    'name': 'search.cell_x',
                    'alias': 'search_cell_x',
                    'unit': 'cell',
                    'timestamp': [0.0, 1.0, 2.0],
                    'value': [0.0, 2.0, 1.0],
                },
                {
                    'name': 'search.cell_y',
                    'alias': 'search_cell_y',
                    'unit': 'cell',
                    'timestamp': [0.0, 1.0, 2.0],
                    'value': [0.0, 1.0, 2.0],
                },
                {
                    'name': 'search.cell_time',
                    'alias': 'search_cell_time',
                    'unit': 's',
                    'timestamp': [0.0, 1.0, 2.0],
                    'value': [0.0, 1.0, 2.0],
                },
            ],
        }]
        interp = BaseInterpreter(data)
        fig, ax = plt.subplots()

        comp = SearchHeatmapComponent(ax, interp, title='First Search Time', grid_shape=(3, 3))

        assert comp.grid[0, 0] == 0.0
        assert comp.grid[1, 2] == 1.0
        assert comp.grid[2, 1] == 2.0
        assert ax.get_title() == 'First Search Time'
        plt.close(fig)


class TestPairDistanceComponent:
    def test_draws_distance_for_configured_pair(self, interpreter):
        PairDistanceComponent = get_component_class('PairDistanceComponent')
        fig, ax = plt.subplots()

        comp = PairDistanceComponent(ax, interpreter, title='Pair Distance', pairs=[(1, 2)])

        line = comp.lines['1-2']
        robot_1 = interpreter.data[0]["values"]
        robot_2 = interpreter.data[1]["values"]
        x1 = np.array(next(item["value"] for item in robot_1 if item["alias"] == "x"))
        y1 = np.array(next(item["value"] for item in robot_1 if item["alias"] == "y"))
        x2 = np.array(next(item["value"] for item in robot_2 if item["alias"] == "x"))
        y2 = np.array(next(item["value"] for item in robot_2 if item["alias"] == "y"))

        assert ax.get_title() == 'Pair Distance'
        assert ax.get_ylabel() == 'Distance (m)'
        np.testing.assert_allclose(line.get_ydata(), np.hypot(x2 - x1, y2 - y1))
        plt.close(fig)

    def test_draws_distance_bounds(self, interpreter):
        PairDistanceComponent = get_component_class('PairDistanceComponent')
        fig, ax = plt.subplots()

        PairDistanceComponent(
            ax,
            interpreter,
            title='Valid Range',
            pairs=[(1, 2)],
            min_distance=0.5,
            max_distance=2.0,
        )

        dashed_lines = [line for line in ax.get_lines() if line.get_linestyle() == '--']
        assert len(dashed_lines) == 2
        assert [line.get_ydata()[0] for line in dashed_lines] == [0.5, 2.0]
        plt.close(fig)

    def test_can_draw_all_pairs(self, interpreter):
        PairDistanceComponent = get_component_class('PairDistanceComponent')
        fig, ax = plt.subplots()

        comp = PairDistanceComponent(ax, interpreter, title='All Pair Distances', pairs='all')

        assert set(comp.lines) == {'1-2', '1-3', '2-3'}
        plt.close(fig)

    def test_draws_uncertainty_buffer(self):
        data = [
            {
                'id': 1,
                'timestamp': [0.0, 1.0],
                'values': [
                    {'name': 'x', 'alias': 'x', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [0.0, 0.0]},
                    {'name': 'y', 'alias': 'y', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [0.0, 0.0]},
                    {'name': 'uncertainty', 'alias': 'uncertainty', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [0.1, 0.2]},
                ],
            },
            {
                'id': 2,
                'timestamp': [0.0, 1.0],
                'values': [
                    {'name': 'x', 'alias': 'x', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [3.0, 4.0]},
                    {'name': 'y', 'alias': 'y', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [4.0, 3.0]},
                    {'name': 'uncertainty', 'alias': 'uncertainty', 'unit': 'm', 'timestamp': [0.0, 1.0], 'value': [0.3, 0.4]},
                ],
            },
        ]
        PairDistanceComponent = get_component_class('PairDistanceComponent')
        fig, ax = plt.subplots()

        comp = PairDistanceComponent(
            ax,
            BaseInterpreter(data),
            title='Pair Distance',
            pairs=[{'ids': [1, 2], 'label': 'leader-follower'}],
            show_uncertainty=True,
        )

        assert 'leader-follower' in comp.lines
        assert len(comp.uncertainty_bands) == 1
        assert len(ax.collections) == 1
        plt.close(fig)


class TestComponentUpdate:
    def test_lines_update_no_error(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X', keys=['x'], mode='animation')
        comp.update(1.0)
        plt.close(fig)

    def test_map_update_no_error(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        comp.update(1.0)
        plt.close(fig)

    def test_map_update_at_end(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        comp.update(5.0)
        plt.close(fig)

    def test_map_update_at_start(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        comp.update(0.0)
        plt.close(fig)

    def test_lines_update_returns_artists(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X', keys=['x'], mode='animation')
        artists = comp.update(1.0)
        assert isinstance(artists, list)
        assert len(artists) > 0
        plt.close(fig)

    def test_map_update_returns_artists(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        artists = comp.update(1.0)
        assert isinstance(artists, list)
        assert len(artists) > 0
        plt.close(fig)
