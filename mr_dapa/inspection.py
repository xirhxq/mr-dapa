"""Data inspection helpers for agent-assisted integrations."""

import math
from numbers import Number


def inspect_data(data):
    """Summarize canonical mr-dapa data for integration agents."""
    canonical_data = _as_canonical_data(data)
    robot_ids = []
    aliases = {}
    timestamps = []

    for robot in canonical_data:
        robot_id = robot.get("id")
        robot_ids.append(robot_id)
        timestamps.extend(_numeric_values(robot.get("timestamp", [])))

        for value in robot.get("values", []):
            alias = value.get("alias") or value.get("name")
            if not alias:
                continue

            item = aliases.setdefault(alias, {
                "name": value.get("name", alias),
                "unit": value.get("unit", ""),
                "robot_ids": [],
                "samples": 0,
            })
            if robot_id not in item["robot_ids"]:
                item["robot_ids"].append(robot_id)
            item["samples"] += _sample_count(value.get("value", []))
            timestamps.extend(_numeric_values(value.get("timestamp", [])))

    return {
        "robot_ids": robot_ids,
        "time_range": [min(timestamps), max(timestamps)] if timestamps else None,
        "aliases": aliases,
    }


def suggest_components(data):
    """Build a conservative starter component config from canonical data."""
    summary = inspect_data(data)
    aliases = summary["aliases"]
    alias_names = set(aliases)
    components = {}

    if {"x", "y"} <= alias_names:
        components["map"] = {
            "title": "Trajectory",
            "class": "MapComponent",
        }

    state_keys = _present_keys(aliases, [
        "battery",
        "batt",
        "yaw",
        "z",
        "altitude",
        "speed",
        "uncertainty",
    ])
    if state_keys:
        components["state"] = {
            "title": "Core State",
            "class": "LinesComponent",
            "keys": state_keys,
        }

    control_keys = _present_keys(aliases, ["vx", "vy", "yawRateRad", "yaw_rate"])
    if control_keys:
        components["control"] = {
            "title": "Control Input",
            "class": "LinesComponent",
            "keys": control_keys,
            "show_zero_line": False,
        }

    metric_keys = _algorithm_metric_keys(aliases)
    if metric_keys:
        components["algorithm_metrics"] = {
            "title": "Algorithm Metrics",
            "class": "LinesComponent",
            "keys": metric_keys,
            "show_zero_line": False,
        }

    if "search_coverage" in aliases:
        components["coverage"] = {
            "title": "Search Coverage",
            "class": "LinesComponent",
            "keys": ["search_coverage"],
            "ylabel": "Coverage (%)",
            "show_zero_line": False,
        }
    elif "final_coverage" in aliases:
        components["coverage"] = {
            "title": "Final Coverage",
            "class": "LinesComponent",
            "keys": ["final_coverage"],
            "ylabel": "Final Coverage (%)",
            "show_zero_line": False,
        }

    if {"search_cell_x", "search_cell_y", "search_cell_time"} <= alias_names:
        components["search_heatmap"] = {
            "title": "First Search Time",
            "class": "SearchHeatmapComponent",
        }

    if {"x", "y"} <= alias_names and len(_ids_with_aliases(aliases, ["x", "y"])) >= 2:
        components["pair_distance"] = {
            "title": "Pair Distance",
            "class": "PairDistanceComponent",
            "pairs": "all",
        }

    link_quality_keys = _present_keys(aliases, [
        "link_denial_min_selected_quality",
        "link_denial_max_epsilon",
        "link_denial_certified",
        "link_denial_fail_safe",
    ])
    if link_quality_keys:
        components["link_quality"] = {
            "title": "Link Quality",
            "class": "LinesComponent",
            "keys": link_quality_keys,
            "show_zero_line": False,
        }

    if "duration" in aliases:
        components["duration"] = {
            "title": "Duration",
            "class": "LinesComponent",
            "keys": ["duration"],
            "ylabel": "Duration (s)",
            "show_zero_line": False,
        }

    return components


def _as_canonical_data(data):
    if hasattr(data, "data"):
        data = data.data
    if not isinstance(data, list):
        raise TypeError(f"Expected canonical data list, got {type(data).__name__}")
    return data


def _numeric_values(values):
    if isinstance(values, (str, bytes)) or values is None:
        return []
    if not isinstance(values, (list, tuple)):
        values = [values]

    result = []
    for value in values:
        if isinstance(value, Number) and not isinstance(value, bool) and math.isfinite(float(value)):
            result.append(float(value))
    return result


def _sample_count(values):
    if values is None:
        return 0
    if isinstance(values, (str, bytes)):
        return 1
    if isinstance(values, (list, tuple)):
        return len(values)
    return 1


def _present_keys(aliases, candidates):
    return [key for key in candidates if key in aliases]


def _algorithm_metric_keys(aliases):
    keywords = ("cbf", "constraint", "loss", "reward", "error")
    return [
        alias for alias in aliases
        if any(keyword in alias.lower() for keyword in keywords)
        and not alias.startswith("link_denial_")
    ]


def _ids_with_aliases(aliases, required_aliases):
    ids = None
    for alias in required_aliases:
        alias_ids = set(aliases[alias]["robot_ids"])
        ids = alias_ids if ids is None else ids & alias_ids
    return ids or set()
