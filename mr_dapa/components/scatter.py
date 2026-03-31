"""Scatter component for phase plots and scatter visualizations."""

import numpy as np

from .base import BaseComponent


class ScatterComponent(BaseComponent):
    """Scatter plot component for visualizing relationships between values.

    Creates scatter plots of one value versus another (phase plots) with
    separate colors for each robot.
    """

    FIGSIZE = (8, 8)
    expand = False
    required_config_keys = {'x_key': str, 'y_key': str}

    def __init__(self, ax, interpreter, title="", x_key='x', y_key='y', mode='static', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
        self.x_key = x_key
        self.y_key = y_key

        self.robot_data = {}
        for robot in self.interpreter.data:
            robot_id = robot["id"]
            x_data = None
            y_data = None

            for value in robot["values"]:
                if value["alias"] == x_key or value["name"] == x_key:
                    x_data = {"timestamp": value["timestamp"], "value": value["value"]}
                elif value["alias"] == y_key or value["name"] == y_key:
                    y_data = {"timestamp": value["timestamp"], "value": value["value"]}

            if x_data and y_data:
                self.robot_data[robot_id] = {
                    "x": x_data["value"],
                    "y": y_data["value"],
                    "timestamps": x_data["timestamp"]
                }

        self._initialize()

    def _initialize(self):
        self.ax.set_title(self.title)

        x_units = self.interpreter.get_units([self.x_key])
        y_units = self.interpreter.get_units([self.y_key])
        self.ax.set_xlabel(f"{self.x_key} ({x_units[0]})" if x_units else self.x_key)
        self.ax.set_ylabel(f"{self.y_key} ({y_units[0]})" if y_units else self.y_key)

        marker = self.kwargs.get('marker', '.')

        self.scatter_plots = {}
        self.scatter_markers = {}

        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]
            label = f'Robot #{robot_id}' if len(self.robot_data) > 1 else None
            scatter, = self.ax.plot(
                data["x"], data["y"],
                marker=marker, linestyle='none',
                label=label, alpha=0.6
            )
            self.scatter_plots[robot_id] = scatter

        if len(self.robot_data) > 1:
            self.ax.legend(loc='best')

        if self.mode == "animation":
            self._animation_setup()

    def _animation_setup(self):
        self.anim_markers = {}
        for robot_id in self.robot_data:
            anim_marker, = self.ax.plot(
                [np.nan], [np.nan], 'o', markersize=8, color='red', alpha=0.8
            )
            self.anim_markers[robot_id] = anim_marker

            self.scatter_plots[robot_id].set_data([], [])

    def update(self, timestamp):
        artists = []

        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]
            index = np.searchsorted(data["timestamps"], timestamp)
            if index >= len(data["x"]):
                index = len(data["x"]) - 1

            self.scatter_plots[robot_id].set_data(
                data["x"][:index + 1], data["y"][:index + 1]
            )
            artists.append(self.scatter_plots[robot_id])

            if self.mode == "animation" and robot_id in self.anim_markers:
                self.anim_markers[robot_id].set_data(
                    [data["x"][index]], [data["y"][index]]
                )
                artists.append(self.anim_markers[robot_id])

        return artists
