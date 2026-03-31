"""Heatmap component for 2D density visualization."""

import numpy as np
from .base import BaseComponent


class HeatmapComponent(BaseComponent):
    """2D density heatmap component.

    Visualizes spatial distribution of robot positions as a density heatmap.
    Useful for identifying areas where robots spend the most time.

    Config options:
        x_key: Key name for x position data (default: 'x')
        y_key: Key name for y position data (default: 'y')
        grid_size: Number of bins for histogram (default: 50)
        cmap: Colormap name (default: 'viridis')
        show_colorbar: Whether to show colorbar (default: True)
        limits: Dict with 'x' and 'y' limits [[min, max], [min, max]]
    """

    FIGSIZE = (8, 8)
    expand = True

    def __init__(self, ax, interpreter, title="", mode='static', x_key='x', y_key='y', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)

        self.x_key = x_key
        self.y_key = y_key
        self.grid_size = self.kwargs.get('grid_size', 50)
        self.cmap = self.kwargs.get('cmap', 'viridis')
        self.show_colorbar = self.kwargs.get('show_colorbar', True)

        if 'limits' in self.kwargs:
            self.map_limits = self.kwargs['limits']
        elif hasattr(self.interpreter, 'get_map_limits'):
            self.map_limits = self.interpreter.get_map_limits()
        else:
            self.map_limits = {"x": [-10, 10], "y": [-10, 10]}

        self.robot_data = {}
        for robot in self.interpreter.data:
            robot_id = robot["id"]
            x_data = None
            y_data = None

            for value in robot["values"]:
                if value["alias"] == self.x_key or value["name"] == self.x_key:
                    x_data = {"value": value["value"]}
                elif value["alias"] == self.y_key or value["name"] == self.y_key:
                    y_data = {"value": value["value"]}

            if x_data and y_data:
                self.robot_data[robot_id] = {
                    "x": np.array(x_data["value"]),
                    "y": np.array(y_data["value"])
                }

        self.heatmap_collection = None
        self.colorbar = None
        self.current_frame = 0

        self._initialize()

    def _initialize(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel(f"X Position ({self.interpreter.get_units([self.x_key])[0]})")
        self.ax.set_ylabel(f"Y Position ({self.interpreter.get_units([self.y_key])[0]})")

        self.ax.set_xlim(self.map_limits["x"])
        self.ax.set_ylim(self.map_limits["y"])

        all_x = []
        all_y = []

        for robot_id in self.robot_data:
            all_x.extend(self.robot_data[robot_id]["x"])
            all_y.extend(self.robot_data[robot_id]["y"])

        if len(all_x) == 0:
            return

        heatmap, xedges, yedges = np.histogram2d(
            all_x, all_y,
            bins=self.grid_size,
            range=[[self.map_limits["x"][0], self.map_limits["x"][1]],
                    [self.map_limits["y"][0], self.map_limits["y"][1]]]
        )

        extent = [
            self.map_limits["x"][0], self.map_limits["x"][1],
            self.map_limits["y"][0], self.map_limits["y"][1]
        ]

        self.heatmap_collection = self.ax.imshow(
            heatmap.T, extent=extent, origin='lower', cmap=self.cmap, aspect='auto'
        )

        if self.show_colorbar:
            self.colorbar = self.ax.figure.colorbar(self.heatmap_collection, ax=self.ax)
            self.colorbar.set_label('Density')

        if self.mode == "animation":
            self._animation_setup()

    def _animation_setup(self):
        self.current_frame = 0

    def update(self, timestamp):
        artists = []

        if self.heatmap_collection is None:
            return artists

        all_x = []
        all_y = []

        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]
            ts = None
            for robot in self.interpreter.data:
                if robot["id"] == robot_id:
                    for value in robot["values"]:
                        if value["alias"] == self.x_key or value["name"] == self.x_key:
                            ts = np.array(value["timestamp"])
                            break
                    break

            if ts is not None:
                index = np.searchsorted(ts, timestamp)
                if index >= len(data["x"]):
                    index = len(data["x"]) - 1
                all_x.extend(data["x"][:index + 1])
                all_y.extend(data["y"][:index + 1])

        if len(all_x) > 0:
            heatmap, _, _ = np.histogram2d(
                all_x, all_y,
                bins=self.grid_size,
                range=[[self.map_limits["x"][0], self.map_limits["x"][1]],
                        [self.map_limits["y"][0], self.map_limits["y"][1]]]
            )
            self.heatmap_collection.set_data(heatmap.T)
            self.heatmap_collection.set_clim(vmin=0, vmax=heatmap.max())

        artists.append(self.heatmap_collection)
        return artists
