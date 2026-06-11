"""Search heatmap component for first-discovery grids."""

import numpy as np

from .base import BaseComponent


class SearchHeatmapComponent(BaseComponent):
    """Render first-search time for grid cells."""

    FIGSIZE = (8, 8)
    expand = False

    def __init__(
        self,
        ax,
        interpreter,
        title="",
        mode='static',
        x_key='search_cell_x',
        y_key='search_cell_y',
        value_key='search_cell_time',
        **kwargs,
    ):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
        self.x_key = x_key
        self.y_key = y_key
        self.value_key = value_key
        self.grid_shape = self.kwargs.get('grid_shape')
        self.cmap = self.kwargs.get('cmap', 'viridis')
        self.show_colorbar = self.kwargs.get('show_colorbar', True)
        self.limits = self.kwargs.get('limits')
        self.grid = None
        self.image = None
        self.colorbar = None

        self._initialize()

    def _initialize(self):
        x_values = self._series(self.x_key)
        y_values = self._series(self.y_key)
        time_values = self._series(self.value_key)

        if self.grid_shape is None:
            self.grid_shape = self._infer_grid_shape(x_values, y_values)

        x_num, y_num = self.grid_shape
        self.grid = np.full((y_num, x_num), np.nan)

        for x_raw, y_raw, time in zip(x_values, y_values, time_values):
            x = int(x_raw)
            y = int(y_raw)
            if 0 <= x < x_num and 0 <= y < y_num:
                self.grid[y, x] = time

        self.ax.set_title(self.title)
        self.ax.set_xlabel('x cell')
        self.ax.set_ylabel('y cell')
        self.ax.set_aspect('equal')

        self.image = self.ax.imshow(
            self.grid,
            origin='lower',
            cmap=self.cmap,
            extent=self._extent(x_num, y_num),
            aspect='auto',
        )

        if self.show_colorbar:
            self.colorbar = self.ax.figure.colorbar(self.image, ax=self.ax)
            self.colorbar.set_label('First search time (s)')

    def update(self, timestamp):
        if self.image is None:
            return []
        frame_grid = self.grid.copy()
        frame_grid[frame_grid > timestamp] = np.nan
        self.image.set_data(frame_grid)
        return [self.image]

    def _series(self, key):
        for robot in self.interpreter.data:
            for value in robot["values"]:
                if value["alias"] == key or value["name"] == key:
                    return list(value["value"])
        return []

    def _infer_grid_shape(self, x_values, y_values):
        if not x_values or not y_values:
            return (1, 1)
        return (int(max(x_values)) + 1, int(max(y_values)) + 1)

    def _extent(self, x_num, y_num):
        if self.limits:
            return [
                self.limits["x"][0],
                self.limits["x"][1],
                self.limits["y"][0],
                self.limits["y"][1],
            ]
        return [-0.5, x_num - 0.5, -0.5, y_num - 0.5]
