import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from mr_dapa.helpers.grid_layout import GridLayout


def _registered_components():
    return {
        'x': {'title': 'X', 'class': 'LinesComponent', 'keys': ['x']},
        'y': {'title': 'Y', 'class': 'LinesComponent', 'keys': ['y']},
        'map': {'title': 'Map', 'class': 'MapComponent', 'limits': {'x': [-2, 2], 'y': [-2, 2]}},
    }


class TestGridLayoutDimensions:
    def test_single_component_map_only(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['map'], _registered_components(), id_list=[1, 2])
        assert layout.layout_config['rows'] == 1
        assert layout.layout_config['cols'] == 1
        plt.close(fig)

    def test_single_lines_component_expand_false(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x'], _registered_components(), expand=False, id_list=[1, 2, 3])
        assert layout.layout_config['rows'] >= 1
        assert layout.layout_config['cols'] >= 1
        plt.close(fig)

    def test_single_lines_component_expand_true(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x'], _registered_components(), expand=True, id_list=[1, 2, 3])
        assert layout.layout_config['components'][0]['id_list'] == [1]
        plt.close(fig)

    def test_two_components(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x', 'y'], _registered_components(), expand=False, id_list=[1])
        assert len(layout.layout_config['components']) == 2
        plt.close(fig)


class TestGridLayoutExpand:
    def test_expand_false_single_id_per_component(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x'], _registered_components(), expand=False, id_list=[1, 2, 3])
        comps = layout.layout_config['components']
        assert len(comps) == 1
        assert comps[0]['id_list'] == [1, 2, 3]
        plt.close(fig)

    def test_expand_true_splits_by_robot(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x'], _registered_components(), expand=True, id_list=[1, 2, 3])
        comps = layout.layout_config['components']
        assert len(comps) == 3
        ids = [c['id_list'][0] for c in comps]
        assert ids == [1, 2, 3]
        plt.close(fig)

    def test_expand_true_two_keys(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x', 'y'], _registered_components(), expand=True, id_list=[1, 2])
        comps = layout.layout_config['components']
        assert len(comps) == 4
        plt.close(fig)


class TestGridLayoutMapOnly:
    def test_map_only_layout(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['map'], _registered_components(), id_list=[1, 2, 3])
        comps = layout.layout_config['components']
        assert len(comps) == 1
        assert comps[0]['id_list'] == [1, 2, 3]
        plt.close(fig)


class TestGridLayoutMixed:
    def test_lines_plus_map(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x', 'map'], _registered_components(), expand=False, id_list=[1, 2])
        comps = layout.layout_config['components']
        has_map = any(c.get('class') == 'MapComponent' for c in comps)
        has_lines = any(c.get('class') == 'LinesComponent' for c in comps)
        assert has_map
        assert has_lines
        plt.close(fig)

    def test_allocate_axes_returns_config(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['x', 'y'], _registered_components(), expand=False, id_list=[1])
        axes_map = layout.allocate_axes()
        assert len(axes_map) == 2
        for item in axes_map:
            assert 'ax' in item
        plt.close(fig)

    def test_allocate_axes_map_only(self):
        fig = plt.figure()
        layout = GridLayout(fig, ['map'], _registered_components(), id_list=[1, 2])
        axes_map = layout.allocate_axes()
        assert len(axes_map) == 1
        assert 'ax' in axes_map[0]
        plt.close(fig)
