import pytest
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from mr_dapa.components.lines import LinesComponent
from mr_dapa.components.map import MapComponent
from mr_dapa.helpers.base_interpreter import BaseInterpreter


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

    def test_axis_title(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='Test Title', keys=['x'])
        assert ax.get_title() == 'Test Title'
        plt.close(fig)

    def test_axis_xlabel(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X', keys=['x'])
        assert ax.get_xlabel() == 'Time (s)'
        plt.close(fig)

    def test_axis_ylabel_single_unit(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X', keys=['x'])
        ylabel = ax.get_ylabel()
        assert '(m)' in ylabel
        plt.close(fig)

    def test_axis_ylabel_mixed_units(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='Mixed', keys=['x', 'batt'])
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
        comp = LinesComponent(ax, interpreter, title='X', keys=['x'], bars=[-1.0, 0.0, 1.0])
        hline_count = sum(1 for line in ax.get_lines() if line.get_linestyle() == '--')
        assert hline_count >= 3
        plt.close(fig)

    def test_range_draws_span(self, interpreter):
        fig, ax = plt.subplots()
        comp = LinesComponent(ax, interpreter, title='X', keys=['x'], range=[-0.5, 0.5])
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
        comp = MapComponent(ax, interpreter, title='Map', limits={'x': [-5, 5], 'y': [-5, 5]})
        assert ax.get_xlim() == (-5, 5)
        assert ax.get_ylim() == (-5, 5)
        plt.close(fig)

    def test_default_limits(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        assert ax.get_xlim() == (-10, 10)
        assert ax.get_ylim() == (-10, 10)
        plt.close(fig)

    def test_title_is_set(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        assert ax.get_title() == 'Map'
        plt.close(fig)

    def test_xlabel_has_unit(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
        xlabel = ax.get_xlabel()
        assert '(m)' in xlabel
        plt.close(fig)

    def test_ylabel_has_unit(self, interpreter):
        fig, ax = plt.subplots()
        comp = MapComponent(ax, interpreter, title='Map')
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
        comp = MapComponent(ax, interpreter, title='Map')
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
