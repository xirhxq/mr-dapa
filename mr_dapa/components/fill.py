import numpy as np

from .base import BaseComponent


class FillComponent(BaseComponent):
    FIGSIZE = (6, 6)
    expand = True
    required_config_keys = {'keys': list}

    def __init__(self, ax, interpreter, title="", keys=None, mode='static', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
        self.keys = keys or []
        self.units = self.interpreter.get_units(self.keys)
        self.single_unit = len(self.units) == 1

        self.lines = {}
        self.fill_collections = {}
        self.markers = {}
        self.value_texts = {}
        self.vline = None
        self.y_limits = None

        self._initialize()

    def _initialize(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Time (s)")
        ylabel = "Values" + ((" (" + self.units[0] + ")") if self.single_unit else "")
        self.ax.set_ylabel(ylabel)

        fill_color = self.kwargs.get('fill_color', 'blue')
        fill_alpha = self.kwargs.get('fill_alpha', 0.2)

        for frame in self.interpreter.data:
            upper_data = None
            lower_data = None

            for value in frame["values"]:
                if value["alias"] in self.keys or value["name"] in self.keys:
                    if upper_data is None:
                        upper_data = value
                    else:
                        lower_data = value

            if upper_data is not None and lower_data is not None:
                label_suffix = f", Robot #{frame['id']}" if len(self.interpreter.id_list) > 1 else ""
                line_upper, = self.ax.plot(
                    upper_data["timestamp"], upper_data["value"],
                    label=upper_data["alias"] + label_suffix, alpha=0.7
                )
                line_lower, = self.ax.plot(
                    lower_data["timestamp"], lower_data["value"],
                    label=lower_data["alias"] + label_suffix, alpha=0.7
                )
                self.lines[f"{frame['id']}-upper"] = line_upper
                self.lines[f"{frame['id']}-lower"] = line_lower

                fill = self.ax.fill_between(
                    upper_data["timestamp"],
                    upper_data["value"],
                    lower_data["value"],
                    color=fill_color,
                    alpha=fill_alpha
                )
                self.fill_collections[frame['id']] = fill

            elif upper_data is not None:
                label_suffix = f", Robot #{frame['id']}" if len(self.interpreter.id_list) > 1 else ""
                line, = self.ax.plot(
                    upper_data["timestamp"], upper_data["value"],
                    label=upper_data["alias"] + label_suffix
                )
                self.lines[f"{frame['id']}-single"] = line

                fill = self.ax.fill_between(
                    upper_data["timestamp"],
                    upper_data["value"], 0,
                    color=fill_color,
                    alpha=fill_alpha
                )
                self.fill_collections[frame['id']] = fill

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

        marker_style = dict(marker='*', color='red', alpha=0.7, markersize=10)
        text_style = dict(
            color='red', alpha=0.8, fontsize=9,
            bbox=dict(facecolor='white', alpha=0.3, edgecolor='none')
        )

        for label_key, line in self.lines.items():
            marker, = self.ax.plot([np.nan], [np.nan], **marker_style)
            self.markers[label_key] = marker

            text = self.ax.text(
                np.nan, np.nan, '', **text_style,
                verticalalignment='center',
                horizontalalignment='left'
            )
            self.value_texts[label_key] = text

    def update(self, timestamp):
        artists = []

        if self.vline is not None:
            self.vline.set_data([timestamp, timestamp], self.y_limits)
            artists.append(self.vline)

        timespan = self.interpreter.time_range[1] - self.interpreter.time_range[0]
        time_offset = timespan * 0.015
        x_limits = self.ax.get_xlim()

        for label_key, line in self.lines.items():
            if label_key not in self.markers:
                continue
            index = np.searchsorted(line.get_xdata(), timestamp)

            self.markers[label_key].set_data([timestamp], [line.get_ydata()[index]])
            artists.append(self.markers[label_key])

            if timestamp < (x_limits[0] + x_limits[1]) / 2:
                self.value_texts[label_key].set_horizontalalignment('left')
                self.value_texts[label_key].set_position(
                    (timestamp + time_offset, line.get_ydata()[index])
                )
            else:
                self.value_texts[label_key].set_horizontalalignment('right')
                self.value_texts[label_key].set_position(
                    (timestamp - time_offset, line.get_ydata()[index])
                )
            self.value_texts[label_key].set_text(f"{line.get_ydata()[index]:.4f}")
            artists.append(self.value_texts[label_key])

        return artists
