import json
import os
import pytest
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from mr_dapa.drawers.static_global import StaticGlobalPlotDrawer
from mr_dapa.drawers.static_separate import StaticSeparatePlotDrawer
from mr_dapa.drawers.static_group import StaticGroupPlotDrawer


def _write_data(tmp_path, sample_data):
    data_file = tmp_path / 'data.json'
    data_file.write_text(json.dumps(sample_data))
    return str(data_file)


def _components():
    return {
        'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
        'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
        'map': {
            'title': 'Map',
            'class': 'MapComponent',
            'limits': {'x': [-2, 2], 'y': [-2, 2]},
        },
    }


class TestStaticGlobalPlotDrawer:
    def test_draw_returns_figure(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        result = drawer.draw(['x'])
        assert isinstance(result, Figure)
        plt.close(result)

    def test_draw_multiple_plots(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        result = drawer.draw(['x', 'y'])
        assert isinstance(result, Figure)
        plt.close(result)

    def test_draw_with_save(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x'], save=True)
        output_dir = os.path.join(str(tmp_path), 'data-plots')
        assert os.path.isdir(output_dir)
        files = os.listdir(output_dir)
        assert any(f.endswith('.png') for f in files)

    def test_output_file_has_reasonable_size(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x'], save=True)
        output_dir = os.path.join(str(tmp_path), 'data-plots')
        png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        png_path = os.path.join(output_dir, png_files[0])
        assert os.path.getsize(png_path) > 1000

    def test_draw_with_path(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        output_path = str(tmp_path / 'custom_output.png')
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x'], path=output_path)
        assert os.path.isfile(output_path)
        assert os.path.getsize(output_path) > 1000


class TestStaticSeparatePlotDrawer:
    def test_returns_list_of_figures(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticSeparatePlotDrawer(files=[data_file], components=_components())
        result = drawer.draw(['x'])
        assert isinstance(result, list)
        assert len(result) == 3
        for fig in result:
            assert isinstance(fig, Figure)
            plt.close(fig)

    def test_save_produces_file_per_robot(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticSeparatePlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x'], save=True)
        output_dir = os.path.join(str(tmp_path), 'data-plots')
        png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        assert len(png_files) == 3

    def test_each_file_has_reasonable_size(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticSeparatePlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x'], save=True)
        output_dir = os.path.join(str(tmp_path), 'data-plots')
        png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        for f in png_files:
            assert os.path.getsize(os.path.join(output_dir, f)) > 1000


class TestStaticGroupPlotDrawer:
    def test_draw_returns_figure(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGroupPlotDrawer(files=[data_file], components=_components())
        result = drawer.draw(['x'])
        assert isinstance(result, Figure)
        plt.close(result)

    def test_grouped_filename(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGroupPlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x'], save=True)
        output_dir = os.path.join(str(tmp_path), 'data-plots')
        png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        assert any('grouped' in f for f in png_files)


class TestDrawerChainAPI:
    def test_set_id_list(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        result = drawer.set_id_list([1])
        assert result is drawer
        assert drawer.interpreter.id_list == [1]

    def test_set_time_range(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        result = drawer.set_time_range((1.0, 3.0))
        assert result is drawer
        assert drawer.interpreter.time_range == (1.0, 3.0)

    def test_set_first_seconds(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        result = drawer.set_first_seconds(2.0)
        assert result is drawer
        assert drawer.interpreter.time_range[1] == pytest.approx(2.0)

    def test_set_last_seconds(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        result = drawer.set_last_seconds(2.0)
        assert result is drawer
        assert drawer.interpreter.time_range[0] == pytest.approx(3.0)

    def test_chain_set_id_then_draw(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        fig = drawer.set_id_list([1]).draw(['x'])
        assert isinstance(fig, Figure)
        plt.close(fig)

    def test_chain_all(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        fig = drawer.set_time_range((1.0, 3.0)).set_id_list([1, 2]).draw(['x', 'y'])
        assert isinstance(fig, Figure)
        plt.close(fig)

    def test_invalid_plot_type_raises(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        with pytest.raises(ValueError, match="not registered"):
            drawer.draw(['nonexistent'])


class TestDrawerIntegration:
    def test_full_pipeline_json_to_png(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        drawer.draw(['x', 'y'], save=True)
        output_dir = os.path.join(str(tmp_path), 'data-plots')
        assert os.path.isdir(output_dir)
        png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
        assert len(png_files) >= 1
        for f in png_files:
            path = os.path.join(output_dir, f)
            assert os.path.getsize(path) > 1000

    def test_separate_draws_per_robot(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticSeparatePlotDrawer(files=[data_file], components=_components())
        figs = drawer.draw(['x'])
        assert len(figs) == 3
        for fig in figs:
            plt.close(fig)

    def test_group_draws_expanded(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGroupPlotDrawer(files=[data_file], components=_components())
        fig = drawer.draw(['x', 'y'])
        assert isinstance(fig, Figure)
        plt.close(fig)

    def test_draw_with_map(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        fig = drawer.draw(['map'])
        assert isinstance(fig, Figure)
        plt.close(fig)

    def test_draw_mixed_lines_and_map(self, tmp_path, sample_data):
        data_file = _write_data(tmp_path, sample_data)
        drawer = StaticGlobalPlotDrawer(files=[data_file], components=_components())
        fig = drawer.draw(['x', 'map'])
        assert isinstance(fig, Figure)
        plt.close(fig)
