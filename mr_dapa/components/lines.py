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
                self.lines[self._make_label(frame['id'], value["name"])] = line

        self.ax.legend(loc='best')

        if self.mode == "animation":
            self._animation_setup()

    def _animation_setup(self):
        self.y_limits = self.ax.get_ylim()
        self.vline = self.ax.plot(
            [self.interpreter.time_range[0], self.interpreter.time_range[1]],
            [self.y_limits[0], self.y_limits[1]],
            'r--', alpha=0.3
        )[0]

    def update(self, timestamp):
        self.vline.set_data([timestamp, timestamp], self.y_limits)
        timespan = self.interpreter.time_range[1] - self.interpreter.time_range[0]
        time_offset = timespan * 0.015
        x_limits = self.ax.get_xlim()

        for label, line in self.lines.items():
            index = np.searchsorted(line.get_xdata(), timestamp)

            self.markers[label].set_data([timestamp], [line.get_ydata()[index]])

            if timestamp < (x_limits[0] + x_limits[1]) / 2:
                self.value_texts[label].set_horizontalalignment('left')
                self.value_texts[label].set_position((timestamp + time_offset, line.get_ydata()[index]))
            else:
                self.value_texts[label].set_horizontalalignment('right')
                self.value_texts[label].set_position((timestamp - time_offset, line.get_ydata()[index]))

            self.value_texts[label].set_text(f"{label}: {line.get_ydata()[index]:.4f}")

        self.ax.legend(loc='best')