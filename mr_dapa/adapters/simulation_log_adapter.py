"""Adapter for frame-based multi-robot simulation logs."""

import json
import math
from numbers import Number
from pathlib import Path


class SimulationLogAdapter:
    """Load frame-based simulation logs into mr-dapa canonical format."""

    DEFAULT_UNITS = {
        "x": "m",
        "y": "m",
        "yaw": "rad",
        "yawRad": "rad",
        "battery": "mV",
        "vx": "m/s",
        "vy": "m/s",
        "yawRateRad": "rad/s",
        "uncertainty": "m",
        "cov_xx": "m^2",
        "cov_xy": "m^2",
        "cov_yy": "m^2",
    }

    def __init__(self, include_global_metrics=True, run_index=0, global_id="global"):
        self.include_global_metrics = include_global_metrics
        self.run_index = run_index
        self.global_id = global_id

    def load(self, source) -> list[dict]:
        data = self._load_source(source)
        data = self._select_run(data)

        if not isinstance(data, dict) or "state" not in data:
            raise ValueError("SimulationLogAdapter expects a dict with a 'state' key")

        result = self._convert_robot_series(data)
        if self.include_global_metrics:
            global_series = self._convert_global_metrics(data)
            if global_series is not None:
                result.append(global_series)
        return result

    def _load_source(self, source):
        if isinstance(source, (str, Path)):
            with open(source) as f:
                return json.load(f)

        if isinstance(source, list):
            if len(source) == 1 and isinstance(source[0], (str, Path)):
                return self._load_source(source[0])
            if source and all(isinstance(item, (str, Path)) for item in source):
                raise ValueError("SimulationLogAdapter expects one simulation log file")
            return source

        if isinstance(source, dict):
            return source

        raise TypeError(f"SimulationLogAdapter expects a path, dict, or list, got {type(source).__name__}")

    def _select_run(self, data):
        if isinstance(data, list) and data and all(isinstance(item, dict) and "state" in item for item in data):
            return data[self.run_index]
        return data

    def _convert_robot_series(self, data):
        robots = {}

        for frame_index, frame in enumerate(data["state"]):
            timestamp = float(frame.get("runtime", frame_index))
            for robot in frame.get("robots", []):
                robot_id = robot.get("id")
                if robot_id is None:
                    continue

                robot_data = robots.setdefault(robot_id, {"timestamps": [], "values": {}})
                robot_data["timestamps"].append(timestamp)
                frame_values = dict(self._iter_robot_values(robot))

                for alias, meta in frame_values.items():
                    if alias not in robot_data["values"]:
                        robot_data["values"][alias] = {
                            "name": meta["name"],
                            "alias": alias,
                            "unit": meta["unit"],
                            "value": [math.nan] * (len(robot_data["timestamps"]) - 1),
                        }

                for alias, series in robot_data["values"].items():
                    series["value"].append(frame_values.get(alias, {}).get("value", math.nan))

        result = []
        for robot_id, robot_data in robots.items():
            result.append({
                "id": robot_id,
                "timestamp": robot_data["timestamps"],
                "values": [
                    {
                        "name": item["name"],
                        "alias": item["alias"],
                        "unit": item["unit"],
                        "timestamp": robot_data["timestamps"],
                        "value": item["value"],
                    }
                    for item in robot_data["values"].values()
                ],
            })
        return result

    def _iter_robot_values(self, robot):
        for key, value in (robot.get("state") or {}).items():
            alias = "yaw" if key == "yawRad" else key
            yield alias, self._make_value(f"state.{key}", alias, value)

        for key, value in ((robot.get("opt") or {}).get("result") or {}).items():
            yield key, self._make_value(f"opt.result.{key}", key, value)

        for key, value in (robot.get("cbfSlack") or {}).items():
            yield key, self._make_value(f"cbfSlack.{key}", key, value)

        for key, value in (robot.get("cbfNoSlack") or {}).items():
            yield key, self._make_value(f"cbfNoSlack.{key}", key, value)

        if "uncertainty" in robot:
            yield "uncertainty", self._make_value("uncertainty", "uncertainty", robot["uncertainty"])

        for key, value in (robot.get("position_covariance") or {}).items():
            yield key, self._make_value(f"position_covariance.{key}", key, value)

        yield from self._iter_metric_values(robot.get("link_denial"), "link_denial")

    def _make_value(self, name, alias, value):
        if not self._is_number(value):
            return {"name": name, "unit": self.DEFAULT_UNITS.get(alias, ""), "value": math.nan}
        return {"name": name, "unit": self.DEFAULT_UNITS.get(alias, ""), "value": float(value)}

    def _iter_metric_values(self, metrics, prefix):
        for key, value in (metrics or {}).items():
            if not self._is_metric_number(value):
                continue
            alias = f"{prefix}_{key}"
            yield alias, {
                "name": f"{prefix}.{key}",
                "unit": self.DEFAULT_UNITS.get(alias, ""),
                "value": float(value),
            }

    def _convert_global_metrics(self, data):
        frames = data.get("state", [])
        grid_world = data.get("para", {}).get("gridWorld", {})
        x_num = grid_world.get("xNum")
        y_num = grid_world.get("yNum")
        if not frames:
            return None

        has_grid = bool(x_num and y_num)
        valid_cells = self._valid_cells(grid_world, int(x_num), int(y_num)) if has_grid else set()
        total_cells = len(valid_cells)
        searched_cells = set()
        timestamps = []
        coverage = []
        searched_counts = []
        event_times = []
        event_x = []
        event_y = []
        link_denial_values = {}

        for frame_index, frame in enumerate(frames):
            timestamp = float(frame.get("runtime", frame_index))
            timestamps.append(timestamp)

            if has_grid:
                for cell in frame.get("update", []):
                    if len(cell) < 2:
                        continue
                    cell_id = (int(cell[0]), int(cell[1]))
                    if cell_id in valid_cells and cell_id not in searched_cells:
                        searched_cells.add(cell_id)
                        event_times.append(timestamp)
                        event_x.append(float(cell_id[0]))
                        event_y.append(float(cell_id[1]))
                searched_counts.append(len(searched_cells))
                coverage.append(len(searched_cells) / total_cells * 100 if total_cells else 0.0)

            frame_values = dict(self._iter_metric_values(frame.get("link_denial"), "link_denial"))
            for alias, meta in frame_values.items():
                if alias not in link_denial_values:
                    link_denial_values[alias] = {
                        "name": meta["name"],
                        "alias": alias,
                        "unit": meta["unit"],
                        "value": [math.nan] * (len(timestamps) - 1),
                    }
            for alias, series in link_denial_values.items():
                series["value"].append(frame_values.get(alias, {}).get("value", math.nan))

        values = []
        if has_grid:
            values.extend([
                {
                    "name": "search.coverage",
                    "alias": "search_coverage",
                    "unit": "%",
                    "timestamp": timestamps,
                    "value": coverage,
                },
                {
                    "name": "search.searched_cells",
                    "alias": "searched_cells",
                    "unit": "cells",
                    "timestamp": timestamps,
                    "value": searched_counts,
                },
                {
                    "name": "search.cell_x",
                    "alias": "search_cell_x",
                    "unit": "cell",
                    "timestamp": event_times,
                    "value": event_x,
                },
                {
                    "name": "search.cell_y",
                    "alias": "search_cell_y",
                    "unit": "cell",
                    "timestamp": event_times,
                    "value": event_y,
                },
                {
                    "name": "search.cell_time",
                    "alias": "search_cell_time",
                    "unit": "s",
                    "timestamp": event_times,
                    "value": event_times,
                },
            ])

        values.extend([
            {
                "name": item["name"],
                "alias": item["alias"],
                "unit": item["unit"],
                "timestamp": timestamps,
                "value": item["value"],
            }
            for item in link_denial_values.values()
        ])

        if not values:
            return None

        return {
            "id": self.global_id,
            "timestamp": timestamps,
            "values": values,
        }

    def _valid_cells(self, grid_world, x_num, y_num):
        valid = grid_world.get("valid")
        if valid is None:
            return {(x, y) for y in range(y_num) for x in range(x_num)}

        cells = set()
        for y in range(y_num):
            for x in range(x_num):
                if y < len(valid) and x < len(valid[y]) and valid[y][x]:
                    cells.add((x, y))
        return cells

    def _is_number(self, value):
        return isinstance(value, Number) and not isinstance(value, bool)

    def _is_metric_number(self, value):
        return isinstance(value, Number)
