import json
import math

import pytest

from mr_dapa.adapters.simulation_log_adapter import SimulationLogAdapter
from mr_dapa.helpers.base_interpreter import BaseInterpreter
from mr_dapa.helpers.loader import DataLoader


def _simulation_log():
    return {
        "config": {"num": 2},
        "para": {
            "gridWorld": {
                "xNum": 2,
                "yNum": 2,
                "valid": [
                    [True, False],
                    [True, True],
                ],
            }
        },
        "state": [
            {
                "runtime": 0.0,
                "update": [[0, 0], [1, 0]],
                "robots": [
                    {
                        "id": 1,
                        "state": {"x": 0.0, "y": 1.0, "yawRad": 0.1, "battery": 4100.0},
                        "opt": {"result": {"vx": 1.0, "vy": 0.0, "yawRateRad": 0.01}},
                        "cbfSlack": {"cvtCBF": -1.0},
                        "cbfNoSlack": {"fixedCommCBF(base-0)": 2.0},
                    },
                    {
                        "id": 2,
                        "state": {"x": 2.0, "y": 3.0, "yawRad": 0.2, "battery": 4200.0},
                        "opt": {"result": {"vx": 0.0, "vy": 1.0, "yawRateRad": 0.02}},
                        "cbfSlack": {"cvtCBF": -2.0},
                        "cbfNoSlack": {"fixedCommCBF(base-0)": 3.0},
                    },
                ],
            },
            {
                "runtime": 1.0,
                "update": [[1, 1]],
                "robots": [
                    {
                        "id": 1,
                        "state": {"x": 1.0, "y": 2.0, "yawRad": 0.3, "battery": 4099.0},
                        "opt": {"result": {"vx": 1.5, "vy": 0.5, "yawRateRad": 0.03}},
                        "cbfSlack": {"cvtCBF": -0.5},
                        "cbfNoSlack": {"fixedCommCBF(base-0)": 4.0},
                    },
                    {
                        "id": 2,
                        "state": {"x": 3.0, "y": 4.0, "yawRad": 0.4, "battery": 4199.0},
                        "opt": {"result": {"vx": 0.5, "vy": 1.5, "yawRateRad": 0.04}},
                        "cbfSlack": {"cvtCBF": -1.5},
                        "cbfNoSlack": {"fixedCommCBF(base-0)": 5.0},
                    },
                ],
            },
        ],
    }


def _value(robot, alias):
    for item in robot["values"]:
        if item["alias"] == alias:
            return item
    raise AssertionError(f"missing value alias {alias}")


class TestSimulationLogAdapter:
    def test_converts_frame_log_to_canonical_robot_series(self):
        adapter = SimulationLogAdapter(include_global_metrics=False)

        result = adapter.load(_simulation_log())

        assert [robot["id"] for robot in result] == [1, 2]
        assert _value(result[0], "x")["value"] == [0.0, 1.0]
        assert _value(result[0], "yaw")["unit"] == "rad"
        assert _value(result[0], "vx")["value"] == [1.0, 1.5]
        assert _value(result[0], "cvtCBF")["value"] == [-1.0, -0.5]
        assert _value(result[0], "fixedCommCBF(base-0)")["value"] == [2.0, 4.0]
        assert BaseInterpreter(result).get_robot_number() == 2

    def test_adds_global_search_coverage_from_grid_updates(self):
        adapter = SimulationLogAdapter()

        result = adapter.load(_simulation_log())

        global_series = result[-1]
        assert global_series["id"] == "global"
        coverage = _value(global_series, "search_coverage")
        assert coverage["unit"] == "%"
        assert coverage["value"] == pytest.approx([100 / 3, 200 / 3])

    def test_adds_first_search_cell_events(self):
        adapter = SimulationLogAdapter()

        result = adapter.load(_simulation_log())

        global_series = result[-1]
        assert _value(global_series, "search_cell_x")["value"] == [0.0, 1.0]
        assert _value(global_series, "search_cell_y")["value"] == [0.0, 1.0]
        assert _value(global_series, "search_cell_time")["value"] == [0.0, 1.0]

    def test_adds_global_link_denial_metrics(self):
        data = _simulation_log()
        data["state"][0]["link_denial"] = {
            "certified": True,
            "fail_safe": False,
            "max_epsilon": 1.5,
            "mode": "adaptive_greedy",
        }
        data["state"][1]["link_denial"] = {
            "certified": False,
            "fail_safe": True,
            "max_epsilon": 2.5,
            "mode": "adaptive_greedy",
        }

        result = SimulationLogAdapter().load(data)

        global_series = result[-1]
        assert _value(global_series, "link_denial_certified")["value"] == [1.0, 0.0]
        assert _value(global_series, "link_denial_fail_safe")["value"] == [0.0, 1.0]
        assert _value(global_series, "link_denial_max_epsilon")["value"] == [1.5, 2.5]

    def test_adds_robot_link_denial_metrics(self):
        data = _simulation_log()
        data["state"][0]["robots"][0]["link_denial"] = {
            "certified": True,
            "fail_safe": False,
            "min_selected_quality": 0.8,
        }
        data["state"][1]["robots"][0]["link_denial"] = {
            "certified": False,
            "fail_safe": True,
            "min_selected_quality": 0.6,
        }

        result = SimulationLogAdapter(include_global_metrics=False).load(data)

        robot = result[0]
        assert _value(robot, "link_denial_certified")["value"] == [1.0, 0.0]
        assert _value(robot, "link_denial_fail_safe")["value"] == [0.0, 1.0]
        assert _value(robot, "link_denial_min_selected_quality")["value"] == [0.8, 0.6]

    def test_ignores_missing_optional_metric_dicts(self):
        data = _simulation_log()
        data["state"][0]["robots"][0]["cbfSlack"] = None
        data["state"][0]["robots"][0]["cbfNoSlack"] = None

        result = SimulationLogAdapter(include_global_metrics=False).load(data)

        assert _value(result[0], "x")["value"] == [0.0, 1.0]
        cvt_values = _value(result[0], "cvtCBF")["value"]
        assert math.isnan(cvt_values[0])
        assert cvt_values[1] == -0.5

    def test_loads_single_file_list_from_data_loader(self, tmp_path):
        data_file = tmp_path / "data.json"
        data_file.write_text(json.dumps(_simulation_log()))

        loader = DataLoader(str(data_file), adapter=SimulationLogAdapter())

        assert [robot["id"] for robot in loader.data] == [1, 2, "global"]
