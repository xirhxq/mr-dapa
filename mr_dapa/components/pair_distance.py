"""Pair distance component for inter-robot distance plots."""

import itertools

import numpy as np

from .base import BaseComponent


class PairDistanceComponent(BaseComponent):
    """Plot distances between configured robot pairs over time."""

    FIGSIZE = (12, 6)
    expand = False
    required_config_keys = {}

    def __init__(self, ax, interpreter, title="", pairs=None, mode='static', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
        self.pairs = pairs or []
        self.x_key = self.kwargs.get('x_key', 'x')
        self.y_key = self.kwargs.get('y_key', 'y')
        self.uncertainty_key = self.kwargs.get('uncertainty_key', 'uncertainty')
        self.show_uncertainty = self.kwargs.get('show_uncertainty', False)
        self.show_legend = self.kwargs.get('show_legend', True)

        self.lines = {}
        self.uncertainty_bands = []
        self.pair_data = {}

        self._initialize()

    @classmethod
    def validate_config(cls, name: str, config: dict) -> None:
        if 'pairs' not in config:
            raise ValueError(
                f"Component '{name}' ({cls.__name__}): missing required key 'pairs'"
            )
        pairs = config['pairs']
        if pairs != 'all' and not isinstance(pairs, list):
            raise ValueError(
                f"Component '{name}' ({cls.__name__}): key 'pairs' must be list or 'all'"
            )

    def _initialize(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.kwargs.get('xlabel', 'Time (s)'))
        self.ax.set_ylabel(self.kwargs.get('ylabel', self._default_ylabel()))

        for value, label in [
            (self.kwargs.get('min_distance'), 'Minimum distance'),
            (self.kwargs.get('max_distance'), 'Maximum distance'),
        ]:
            if value is not None:
                self.ax.axhline(value, color='black', linestyle='--', alpha=0.35, label=label)

        robot_data = self._collect_robot_data()
        for pair in self._normalize_pairs(robot_data):
            series = self._make_pair_series(robot_data, pair)
            if series is None:
                continue

            line_kwargs = {}
            if pair["color"] is not None:
                line_kwargs["color"] = pair["color"]

            line, = self.ax.plot(
                series["timestamp"],
                series["distance"],
                label=pair["label"],
                **line_kwargs,
            )
            self.lines[pair["label"]] = line
            self.pair_data[pair["label"]] = series

            if self.show_uncertainty and series["uncertainty"] is not None:
                band = self.ax.fill_between(
                    series["timestamp"],
                    series["distance"],
                    series["distance"] + series["uncertainty"],
                    alpha=0.18,
                    color=line.get_color(),
                )
                self.uncertainty_bands.append(band)

        if self.lines and self.show_legend:
            self.ax.legend(loc='best')

    def _default_ylabel(self):
        units = self.interpreter.get_units([self.x_key, self.y_key])
        unit = units[0] if len(units) == 1 and units[0] else ''
        return f"Distance ({unit})" if unit else "Distance"

    def _collect_robot_data(self):
        robots = {}
        for robot in self.interpreter.data:
            values = {
                value["alias"]: value
                for value in robot["values"]
            }
            values.update({
                value["name"]: value
                for value in robot["values"]
            })

            x = values.get(self.x_key)
            y = values.get(self.y_key)
            if x is None or y is None:
                continue

            robots[robot["id"]] = {
                "x": self._as_series(x),
                "y": self._as_series(y),
                "uncertainty": self._as_series(values.get(self.uncertainty_key))
                if values.get(self.uncertainty_key) is not None else None,
            }
        return robots

    def _normalize_pairs(self, robot_data):
        if self.pairs == 'all':
            return [
                {"id1": id1, "id2": id2, "label": f"{id1}-{id2}", "color": None}
                for id1, id2 in itertools.combinations(sorted(robot_data), 2)
            ]

        normalized = []
        for pair in self.pairs:
            if isinstance(pair, dict):
                ids = pair["ids"]
                normalized.append({
                    "id1": ids[0],
                    "id2": ids[1],
                    "label": pair.get("label", f"{ids[0]}-{ids[1]}"),
                    "color": pair.get("color"),
                })
            else:
                normalized.append({
                    "id1": pair[0],
                    "id2": pair[1],
                    "label": f"{pair[0]}-{pair[1]}",
                    "color": None,
                })
        return normalized

    def _make_pair_series(self, robot_data, pair):
        first = robot_data.get(pair["id1"])
        second = robot_data.get(pair["id2"])
        if first is None or second is None:
            return None

        start = max(first["x"]["timestamp"][0], first["y"]["timestamp"][0], second["x"]["timestamp"][0], second["y"]["timestamp"][0])
        end = min(first["x"]["timestamp"][-1], first["y"]["timestamp"][-1], second["x"]["timestamp"][-1], second["y"]["timestamp"][-1])
        if end < start:
            return None

        timestamps = self._merged_timestamps([first["x"], first["y"], second["x"], second["y"]], start, end)
        if len(timestamps) == 0:
            return None

        x1 = np.interp(timestamps, first["x"]["timestamp"], first["x"]["value"])
        y1 = np.interp(timestamps, first["y"]["timestamp"], first["y"]["value"])
        x2 = np.interp(timestamps, second["x"]["timestamp"], second["x"]["value"])
        y2 = np.interp(timestamps, second["y"]["timestamp"], second["y"]["value"])
        distance = np.hypot(x2 - x1, y2 - y1)

        uncertainty = None
        if first["uncertainty"] is not None and second["uncertainty"] is not None:
            u1 = np.interp(timestamps, first["uncertainty"]["timestamp"], first["uncertainty"]["value"])
            u2 = np.interp(timestamps, second["uncertainty"]["timestamp"], second["uncertainty"]["value"])
            uncertainty = u1 + u2

        return {
            "timestamp": timestamps,
            "distance": distance,
            "uncertainty": uncertainty,
        }

    def _merged_timestamps(self, series_list, start, end):
        timestamps = np.concatenate([
            series["timestamp"][(series["timestamp"] >= start) & (series["timestamp"] <= end)]
            for series in series_list
        ])
        return np.unique(timestamps)

    def _as_series(self, value):
        return {
            "timestamp": np.array(value["timestamp"], dtype=float),
            "value": np.array(value["value"], dtype=float),
        }
