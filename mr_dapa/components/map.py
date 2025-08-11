from ..helpers.utils import *
from .base import BaseComponent


class MapComponent(BaseComponent):
    def __init__(self, ax, interpreter, title="", **kwargs):
        self.ax = ax
        self.interpreter = interpreter
        self.title = title + self.interpreter.get_title_suffix()

        if 'limits' in kwargs:
            self.map_limits = kwargs.pop('limits')
        elif hasattr(self.interpreter, 'get_map_limits'):
            self.map_limits = self.interpreter.get_map_limits()
        else:
            self.map_limits =  {"x": [-10, 10], "y": [-10, 10]}

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

        self.robots_plot = {}
        for robot_id in self.robot_data:
            line, = self.ax.plot([], [], '*', markersize=10, label=f'Robot #{robot_id}')
            self.robots_plot[robot_id] = line

        self._initialize()

    def _get_map_limits(self):
        if hasattr(self.interpreter, 'get_map_limits'):
            return self.interpreter.get_map_limits()
        else:
            return {"x": [-10, 10], "y": [-10, 10]}

    def _initialize(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel(f"X Position ({self.interpreter.get_units(['x'])[0]})")
        self.ax.set_ylabel(f"Y Position ({self.interpreter.get_units(['y'])[0]})")

        self.ax.set_xlim(self.map_limits["x"])
        self.ax.set_ylim(self.map_limits["y"])

        self.ax.set_aspect('equal', adjustable='box')

        if len(self.robots_plot) > 1:
            self.ax.legend(loc='best')

    def update(self, timestamp):
        for robot_id, plot in self.robots_plot.items():
            if robot_id in self.robot_data:
                data = self.robot_data[robot_id]
                index = np.searchsorted(data["timestamps"], timestamp)
                if index >= len(data["x"]):
                    index = len(data["x"]) - 1

                plot.set_data([data["x"][index]], [data["y"][index]])

        if len(self.robots_plot) > 1:
            self.ax.legend(loc='best')
