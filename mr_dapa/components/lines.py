from ..helpers.utils import *
from .base import BaseComponent


class LinesComponent(BaseComponent):
    def __init__(self, ax, interpreter, title, keys, mode='separate', **kwargs):
        self.ax = ax
        self.interpreter = interpreter
        self.title = title + self.interpreter.get_title_suffix()

        self.keys = keys
        self.units = self.interpreter.get_units(keys)
        self.single_unit = len(self.units) == 1

        self.mode = mode

        self.lines = {}
        self.markers = {}
        self.value_texts = {}

        marker_style = dict(marker='*', color='red', alpha=0.7, markersize=10)
        text_style = dict(color='red', alpha=0.8, fontsize=9, bbox=dict(facecolor='white', alpha=0.3, edgecolor='none'))

        for robot in self.interpreter.data:
            for value in robot["values"]:
                if value["alias"] not in keys and value["name"] not in keys:
                     continue
                marker, = self.ax.plot([np.nan], [np.nan], **marker_style)
                self.markers[self._make_label(robot["id"], value["name"])] = marker

                text = self.ax.text(
                    np.nan, np.nan, '', **text_style,
                    verticalalignment='center',
                    horizontalalignment='left'
                )
                self.value_texts[self._make_label(robot["id"], value["name"])] = text

        self._initialize()

    def _make_label(self, id, name):
        return f"{id}-{name}"

    def _initialize(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Values" + ((" (" + self.units[0] + ")") if self.single_unit else ""))

        self.ax.axhline(0, color='black', linestyle='--', alpha=0.3)

        for frame in self.interpreter.data:
            for value in frame["values"]:
                if value["alias"] not in self.keys and value["name"] not in self.keys:
                    continue
                label = value["name"] if self.mode == "separate" else value["alias"]
                if not self.single_unit:
                    label += f"({value['unit']})"
                if len(self.interpreter.id_list) > 1:
                    label += f", Robot #{frame['id']}"
                line, = self.ax.plot(
                    value["timestamp"], value["value"], label=label
                )
                self.lines[self._make_label(id, value["name"])] = line

        self.ax.legend(loc='best')

        if self.mode == "animation":
            self._animation_setup()

    def _animation_setup(self):
        self.y_limits = self.ax.get_ylim()
        self.vline = self.ax.plot(
            [self.runtime[self.index_range[0]], self.runtime[self.index_range[0]]],
            [self.y_limits[0], self.y_limits[1]],
            'r--', alpha=0.3
        )[0]

    def update(self, num):
        pass