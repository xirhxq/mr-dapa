"""3D map component for 3D position visualization."""

import numpy as np
from .base import BaseComponent


class Map3DComponent(BaseComponent):
    """3D position map component.

    Visualizes robot positions and trajectories in 3D space.
    Requires 'x', 'y', and 'z' value keys in data.

    Config options:
        x_key: Key name for x position data (default: 'x')
        y_key: Key name for y position data (default: 'y')
        z_key: Key name for z position data (default: 'z')
        show_trail: Whether to show trajectory trails (default: True)
        trail_style: Dict of line style options for trails
        marker_style: Dict of marker style options for robot positions
        limits: Dict with 'x', 'y', 'z' limits [[min, max], [min, max], [min, max]]
        elevation: Camera elevation angle (default: 30)
        azimuth: Camera azimuth angle (default: 45)
    """

    FIGSIZE = (10, 8)
    expand = True

    def __init__(self, ax, interpreter, title="", mode='static', x_key='x', y_key='y', z_key='z', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)

        self.x_key = x_key
        self.y_key = y_key
        self.z_key = z_key
        self.show_trail = self.kwargs.get('show_trail', True)
        self.elevation = self.kwargs.get('elevation', 30)
        self.azimuth = self.kwargs.get('azimuth', 45)

        if 'limits' in self.kwargs:
            self.map_limits = self.kwargs['limits']
        else:
            self.map_limits = {"x": [-10, 10], "y": [-10, 10], "z": [0, 10]}

        self.robot_data = {}
        for robot in self.interpreter.data:
            robot_id = robot["id"]
            x_data = None
            y_data = None
            z_data = None

            for value in robot["values"]:
                if value["alias"] == self.x_key or value["name"] == self.x_key:
                    x_data = {"timestamp": value["timestamp"], "value": value["value"]}
                elif value["alias"] == self.y_key or value["name"] == self.y_key:
                    y_data = {"timestamp": value["timestamp"], "value": value["value"]}
                elif value["alias"] == self.z_key or value["name"] == self.z_key:
                    z_data = {"timestamp": value["timestamp"], "value": value["value"]}

            if x_data and y_data and z_data:
                self.robot_data[robot_id] = {
                    "x": x_data["value"],
                    "y": y_data["value"],
                    "z": z_data["value"],
                    "timestamps": x_data["timestamp"]
                }

        self.trail_lines = {}
        self.robot_markers = {}
        self.robot_annotations = {}

        self._initialize()

    def _initialize(self):
        fig = self.ax.figure
        position = self.ax.get_position()
        self.ax.remove()

        self.ax = fig.add_subplot(
            position,
            projection='3d'
        )

        self.ax.set_title(self.title)
        self.ax.set_xlabel(f"X ({self.interpreter.get_units([self.x_key])[0]})")
        self.ax.set_ylabel(f"Y ({self.interpreter.get_units([self.y_key])[0]})")
        self.ax.set_zlabel(f"Z ({self.interpreter.get_units([self.z_key])[0]})")

        self.ax.set_xlim(self.map_limits["x"])
        self.ax.set_ylim(self.map_limits["y"])
        self.ax.set_zlim(self.map_limits["z"])

        self.ax.view_init(elev=self.elevation, azim=self.azimuth)

        trail_style = self.kwargs.get('trail_style', {})
        marker_style = self.kwargs.get('marker_style', {})

        default_marker = dict(marker='*', markersize=8)
        default_marker.update(marker_style)

        colors = self._get_colors()

        for idx, robot_id in enumerate(self.robot_data):
            data = self.robot_data[robot_id]
            color = colors[idx % len(colors)]

            if self.show_trail:
                trail_line = self.ax.plot(
                    data["x"], data["y"], data["z"],
                    '-', alpha=0.4, color=color, **trail_style
                )[0]
                self.trail_lines[robot_id] = trail_line
            else:
                self.trail_lines[robot_id] = None

            marker = self.ax.plot(
                [data["x"][-1]], [data["y"][-1]], [data["z"][-1]],
                label=f'Robot #{robot_id}', color=color, **default_marker
            )[0]
            self.robot_markers[robot_id] = marker

        if len(self.robot_data) > 1:
            self.ax.legend(loc='best')

        if self.mode == "animation":
            self._animation_setup()

    def _get_colors(self):
        from ..style import PALETTES
        palette = self.kwargs.get('palette', PALETTES['default'])
        return palette

    def _animation_setup(self):
        for robot_id in self.robot_data:
            if self.trail_lines[robot_id] is not None:
                self.trail_lines[robot_id].set_data([], [])
                self.trail_lines[robot_id].set_3d_properties([])
            self.robot_markers[robot_id].set_data([], [])
            self.robot_markers[robot_id].set_3d_properties([])

    def update(self, timestamp):
        artists = []

        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]
            index = np.searchsorted(data["timestamps"], timestamp)
            if index >= len(data["x"]):
                index = len(data["x"]) - 1

            if self.trail_lines[robot_id] is not None:
                trail_x = data["x"][:index + 1]
                trail_y = data["y"][:index + 1]
                trail_z = data["z"][:index + 1]
                self.trail_lines[robot_id].set_data(trail_x, trail_y)
                self.trail_lines[robot_id].set_3d_properties(trail_z)
                artists.append(self.trail_lines[robot_id])

            self.robot_markers[robot_id].set_data([data["x"][index]], [data["y"][index]])
            self.robot_markers[robot_id].set_3d_properties([data["z"][index]])
            artists.append(self.robot_markers[robot_id])

        return artists
