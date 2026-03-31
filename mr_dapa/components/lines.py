"""Lines component for time-series line plots."""

import numpy as np
from .base import BaseComponent


class LinesComponent(BaseComponent):
    """Time-series line plot component.

    Draws line plots of values over time for each robot. Supports
    multiple value keys on the same axes, fill between line and zero,
    horizontal reference lines (bounds), and more.
    """

    FIGSIZE = (12, 6)
    required_config_keys = {'keys': list}

    def __init__(self, ax, interpreter, title="", keys=None, mode='static', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
        self.keys = keys or []
        self.units = self.interpreter.get_units(self.keys)
        self.single_unit = len(self.units) == 1

        self.lines = {}
        self.markers = {}
        self.value_texts = {}
        self.vline = None
        self.y_limits = None

        self._initialize()

    def _make_label(self, robot_id, name):
        return f"{robot_id}-{name}"

    def _initialize(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Time (s)")
        ylabel = "Values" + ((" (" + self.units[0] + ")") if self.single_unit else "")
        self.ax.set_ylabel(ylabel)

        if 'bounds' in self.kwargs:
            for b in self.kwargs['bounds']:
                self.ax.axhline(b, color='black', linestyle='--', alpha=0.3)

        if 'range' in self.kwargs:
            self.ax.axhspan(self.kwargs['range'][0], self.kwargs['range'][1], alpha=0.1, color='grey')

        if 'show_zero_line' in self.kwargs and self.kwargs.get('show_zero_line', True):
            self.ax.axhline(0, color='black', alpha=0.3, linestyle='--')

        if 'milestones' in self.kwargs:
            for m in self.kwargs['milestones']:
                self.ax.axvline(m, color='grey', alpha=0.3, linestyle='--')

        if 'bars' in self.kwargs:
            for bar in self.kwargs['bars']:
                self.ax.axhline(bar, color='black', linestyle='--', alpha=0.3)

        marker_style = dict(marker='*', color='red', alpha=0.7, markersize=10)
        text_style = dict(
            color='red', alpha=0.8, fontsize=9,
            bbox=dict(facecolor='white', alpha=0.3, edgecolor='none')
        )

        for robot in self.interpreter.data:
            for value in robot["values"]:
                if value["alias"] not in self.keys and value["name"] not in self.keys:
                    continue
                marker, = self.ax.plot([np.nan], [np.nan], **marker_style)
                self.markers[self._make_label(robot["id"], value["name"])] = marker

                text = self.ax.text(
                    np.nan, np.nan, '', **text_style,
                    verticalalignment='center',
                    horizontalalignment='left'
                )
                self.value_texts[self._make_label(robot["id"], value["name"])] = text

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

        if self.kwargs.get('fill', False):
            for frame in self.interpreter.data:
                for value in frame["values"]:
                    if value["alias"] not in self.keys and value["name"] not in self.keys:
                        continue
                    self.ax.fill_between(
                        value["timestamp"], value["value"], 0, alpha=0.15
                    )

        if self.kwargs.get('show_min', False):
            for frame in self.interpreter.data:
                for value in frame["values"]:
                    if value["alias"] not in self.keys and value["name"] not in self.keys:
                        continue
                    min_idx = np.argmin(value["value"])
                    min_x = value["timestamp"][min_idx]
                    min_y = value["value"][min_idx]
                    self.ax.annotate(
                        f'min: {min_y:.2f}',
                        xy=(min_x, min_y),
                        xytext=(5, 5),
                        textcoords='offset points',
                        fontsize=8,
                        color='blue',
                        alpha=0.7
                    )

        if len(self.lines) > 1:
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
        artists = []

        if self.vline is not None:
            self.vline.set_data([timestamp, timestamp], self.y_limits)
            artists.append(self.vline)

        timespan = self.interpreter.time_range[1] - self.interpreter.time_range[0]
        time_offset = timespan * 0.015
        x_limits = self.ax.get_xlim()

        for label, line in self.lines.items():
            index = np.searchsorted(line.get_xdata(), timestamp)

            self.markers[label].set_data([timestamp], [line.get_ydata()[index]])
            artists.append(self.markers[label])

            if timestamp < (x_limits[0] + x_limits[1]) / 2:
                self.value_texts[label].set_horizontalalignment('left')
                self.value_texts[label].set_position(
                    (timestamp + time_offset, line.get_ydata()[index])
                )
            else:
                self.value_texts[label].set_horizontalalignment('right')
                self.value_texts[label].set_position(
                    (timestamp - time_offset, line.get_ydata()[index])
                )

            if len(self.lines) > 1:
                self.value_texts[label].set_text(f"{label}: {line.get_ydata()[index]:.4f}")
            else:
                self.value_texts[label].set_text(f"{line.get_ydata()[index]:.4f}")
            artists.append(self.value_texts[label])

        if len(self.lines) > 1:
            self.ax.legend(loc='best')

        return artists
