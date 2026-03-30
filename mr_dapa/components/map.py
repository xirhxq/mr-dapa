import numpy as np

from .base import BaseComponent


class MapComponent(BaseComponent):
    expand = False

    def __init__(self, ax, interpreter, title="", mode='static', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)

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
                if value["alias"] == "x" or value["name"] == "x":
                    x_data = {"timestamp": value["timestamp"], "value": value["value"]}
                elif value["alias"] == "y" or value["name"] == "y":
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
        self.ax.set_xlabel(f"X Position ({self.interpreter.get_units(['x'])[0]})")
        self.ax.set_ylabel(f"Y Position ({self.interpreter.get_units(['y'])[0]})")

        self.ax.set_xlim(self.map_limits["x"])
        self.ax.set_ylim(self.map_limits["y"])

        self.ax.set_aspect('equal', adjustable='box')

        trail_style = self.kwargs.get('trail_style', {})
        marker_style = self.kwargs.get('marker_style', {})

        self.trail_lines = {}
        self.robot_markers = {}
        self.robot_annotations = {}

        default_marker = dict(marker='*', markersize=10)
        default_marker.update(marker_style)

        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]

            trail_line, = self.ax.plot(data["x"], data["y"], '-', alpha=0.4, **trail_style)
            self.trail_lines[robot_id] = trail_line

            marker, = self.ax.plot(
                [data["x"][-1]], [data["y"][-1]],
                label=f'Robot #{robot_id}', **default_marker
            )
            self.robot_markers[robot_id] = marker

            annotation = self.ax.annotate(
                f'#{robot_id}',
                xy=(data["x"][-1], data["y"][-1]),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=8,
                alpha=0.7
            )
            self.robot_annotations[robot_id] = annotation

        if len(self.robot_data) > 1:
            self.ax.legend(loc='best')

        if self.mode == "animation":
            self._animation_setup()

    def _animation_setup(self):
        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]
            self.trail_lines[robot_id].set_data([], [])
            self.robot_markers[robot_id].set_data([np.nan], [np.nan])
            self.robot_annotations[robot_id].set_position((np.nan, np.nan))
            self.robot_annotations[robot_id].xy = (np.nan, np.nan)

    def update(self, timestamp):
        artists = []

        for robot_id in self.robot_data:
            data = self.robot_data[robot_id]
            index = np.searchsorted(data["timestamps"], timestamp)
            if index >= len(data["x"]):
                index = len(data["x"]) - 1

            trail_x = data["x"][:index + 1]
            trail_y = data["y"][:index + 1]
            self.trail_lines[robot_id].set_data(trail_x, trail_y)
            artists.append(self.trail_lines[robot_id])

            self.robot_markers[robot_id].set_data([data["x"][index]], [data["y"][index]])
            artists.append(self.robot_markers[robot_id])

            self.robot_annotations[robot_id].xy = (data["x"][index], data["y"][index])
            artists.append(self.robot_annotations[robot_id])

        return artists
