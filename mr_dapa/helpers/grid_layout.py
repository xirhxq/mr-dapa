"""Grid layout manager for allocating matplotlib subplots."""

import math
from matplotlib.gridspec import GridSpec


class GridLayout:
    """Allocates matplotlib subplots based on component configuration.

    Determines subplot arrangement based on component expand attributes
    and the number of robots. Returns a list of axis configuration dicts
    that can be used to instantiate components.
    """

    def __init__(self, fig, plot_list, registered_components, expand=True, id_list=None, **kwargs):
        self.fig = fig
        self.plot_list = plot_list
        self.REGISTERED_COMPONENTS = registered_components

        self.expand = expand
        self.id_list = id_list

        self.layout_config = self._get_layout()

    def _get_layout(self):
        from ..registry import get_component_class

        expandable = []
        non_expandable = []

        for item_name in self.plot_list:
            class_name = self.REGISTERED_COMPONENTS[item_name]['class']
            comp_cls = get_component_class(class_name)
            if comp_cls and not comp_cls.expand:
                non_expandable.append(item_name)
            else:
                expandable.append(item_name)

        side_num = len(expandable)

        layout_config = {}
        if side_num == 0 and len(non_expandable) == 1:
            layout_config['rows'] = 1
            layout_config['cols'] = 1
            layout_config['components'] = [
                {
                    'name': non_expandable[0],
                    'grid': [[None, None], [None, None]],
                    **self.REGISTERED_COMPONENTS[non_expandable[0]],
                    'id_list': self.id_list
                }
            ]
        elif side_num == 0:
            cols = min(len(non_expandable), 2)
            rows = math.ceil(len(non_expandable) / cols)
            layout_config['rows'] = rows
            layout_config['cols'] = cols
            layout_config['components'] = []
            grids = [[i // cols, i % cols] for i in range(len(non_expandable))]
            for idx, item_name in enumerate(non_expandable):
                layout_config['components'].append(
                    {
                        'name': item_name,
                        'grid': grids[idx],
                        **self.REGISTERED_COMPONENTS[item_name],
                        'id_list': self.id_list
                    }
                )
        else:
            layout_components = []
            for item_name in self.plot_list:
                class_name = self.REGISTERED_COMPONENTS[item_name]['class']
                comp_cls = get_component_class(class_name)
                if comp_cls and not comp_cls.expand:
                    layout_components.append({
                        'name': item_name,
                        **self.REGISTERED_COMPONENTS[item_name],
                        'id_list': self.id_list,
                    })
                elif self.expand:
                    for id in self.id_list:
                        layout_components.append({
                            'name': item_name,
                            **self.REGISTERED_COMPONENTS[item_name],
                            'id_list': [id],
                        })
                else:
                    layout_components.append({
                        'name': item_name,
                        **self.REGISTERED_COMPONENTS[item_name],
                        'id_list': self.id_list,
                    })

            total_grids = len(layout_components)
            cols = math.ceil(math.sqrt(total_grids))
            rows = math.ceil(total_grids / cols)

            layout_config = {
                'components': layout_components,
                'rows': rows,
                'cols': cols,
            }

            grids = [[i, j] for i in range(rows) for j in range(cols)]

            assert len(grids) >= len(layout_config['components']), "Not enough grids for all components"

            for index, item in enumerate(layout_config['components']):
                item['grid'] = grids[index]

        return layout_config

    def allocate_axes(self):
        rows = self.layout_config.get("rows", 2)
        cols = self.layout_config.get("cols", 2)
        gs = GridSpec(rows, cols)
        axes_map = []
        for comp_cfg in self.layout_config.get("components", []):
            grid = comp_cfg.get("grid", [0, 0])
            row_spec, col_spec = self._get_grid(grid)
            comp_cfg["ax"] = self.fig.add_subplot(gs[row_spec, col_spec])
            axes_map.append(comp_cfg)
        return axes_map

    def _get_grid(self, grid):
        if isinstance(grid, list) and all(isinstance(g, list) for g in grid):
            row_slice = self._parse_slice(grid[0])
            col_slice = self._parse_slice(grid[1])
            return row_slice, col_slice
        elif isinstance(grid, list) and len(grid) == 2:
            row, col = grid
            return row, col
        else:
            raise ValueError(f"Invalid grid format: {grid}")

    def _parse_slice(self, slice_list):
        if not (isinstance(slice_list, list) and len(slice_list) <= 2):
            raise ValueError("Slice must be a list of 1 or 2 elements.")

        start = slice_list[0] if slice_list[0] is not None else None
        stop = slice_list[1] if len(slice_list) > 1 and slice_list[1] is not None else None

        return slice(start, stop)
