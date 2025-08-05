import math
from matplotlib.gridspec import GridSpec
from ..components.components import *


class GridLayout:
    def __init__(self, fig, plot_list, registered_components, expand=True, id_list=None, **kwargs):
        self.fig = fig
        self.plot_list = plot_list
        self.REGISTERED_COMPONENTS = registered_components

        self.expand = expand
        self.id_list = id_list

        self.layout_config = self._get_layout()


    def _get_layout(self):
        side_list = [s for s in self.plot_list if s != 'map']
        side_num = len(side_list)

        layout_config = {}
        if side_num == 0:
            layout_config['rows'] = 1
            layout_config['cols'] = 1
            layout_config['components'] = [
                {
                    'name': 'map',
                    'grid': [[None, None], [None, None]],
                    **self.REGISTERED_COMPONENTS['map'],
                    'id_list': self.id_list
                }
            ]
        else:
            total_grids = side_num * (len(self.id_list) if self.expand else 1)
            side_cols = math.ceil(math.sqrt(total_grids))
            side_rows = math.ceil(side_num * (len(self.id_list) if self.expand else 1) / side_cols)

            if 'map' in self.plot_list:
                map_cols = math.ceil(side_cols / 2)
            else:
                map_cols = 0

            layout_config = {
                'components': [],
                'rows': side_rows,
                'cols': side_cols + map_cols,
            }

            grids = [[i, j + map_cols] for i in range(side_rows) for j in range(side_cols)]

            for index, item in enumerate(side_list):
                if self.expand:
                    for id in self.id_list:
                        layout_config['components'].append(
                            {
                                **self.REGISTERED_COMPONENTS[item],
                                'id_list': [id],
                            }
                        )
                else:
                    layout_config['components'].append(
                        {
                            **self.REGISTERED_COMPONENTS[item],
                            'id_list': self.id_list
                        }
                    )

            assert len(grids) >= len(layout_config['components']), "Not enough grids for all components"

            for index, item in enumerate(layout_config['components']):
                item['grid'] = grids[index]

            if 'map' in self.plot_list:
                layout_config['components'].append(
                    {
                        'grid': [[None, None], [None, map_cols]],
                        **self.REGISTERED_COMPONENTS['map'],
                        'id_list': self.id_list
                    }
                )

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
