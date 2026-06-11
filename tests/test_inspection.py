import pytest

from mr_dapa import (
    ParametricStudyAdapter,
    SimulationLogAdapter,
    inspect_data,
    suggest_components,
)


def _simulation_log_with_search_and_links():
    return {
        "para": {"gridWorld": {"xNum": 2, "yNum": 2}},
        "state": [
            {
                "runtime": 0.0,
                "update": [[0, 0]],
                "link_denial": {"certified": True, "max_epsilon": 0.4},
                "robots": [
                    {
                        "id": 1,
                        "state": {"x": 0.0, "y": 1.0, "battery": 4100.0},
                        "opt": {"result": {"vx": 1.0, "vy": 0.0}},
                        "link_denial": {"min_selected_quality": 0.9},
                    },
                    {
                        "id": 2,
                        "state": {"x": 2.0, "y": 3.0, "battery": 4200.0},
                        "opt": {"result": {"vx": 0.0, "vy": 1.0}},
                    },
                ],
            },
            {
                "runtime": 1.0,
                "update": [[1, 1]],
                "link_denial": {"certified": False, "max_epsilon": 0.8},
                "robots": [
                    {
                        "id": 1,
                        "state": {"x": 1.0, "y": 2.0, "battery": 4099.0},
                        "opt": {"result": {"vx": 1.5, "vy": 0.5}},
                        "link_denial": {"min_selected_quality": 0.7},
                    },
                    {
                        "id": 2,
                        "state": {"x": 3.0, "y": 4.0, "battery": 4199.0},
                        "opt": {"result": {"vx": 0.5, "vy": 1.5}},
                    },
                ],
            },
        ],
    }


def _parametric_summary():
    return {
        "parametric_study": {
            "parameter_name": "comm_range",
            "parameter_values": [650.0, 850.0],
            "results": [
                {"parameter_value": 650.0, "duration": 349.5, "final_coverage": 68.56},
                {"parameter_value": 850.0, "duration": 289.0, "final_coverage": 100.0},
            ],
        }
    }


class TestInspectData:
    def test_summarizes_robot_ids_time_range_and_aliases(self, sample_data):
        summary = inspect_data(sample_data)

        assert summary["robot_ids"] == [1, 2, 3]
        assert summary["time_range"] == pytest.approx([0.0, 5.0])
        assert summary["aliases"]["x"] == {
            "name": "X Position",
            "unit": "m",
            "robot_ids": [1, 2, 3],
            "samples": 300,
        }

    def test_suggests_starter_components_for_basic_multi_robot_data(self, sample_data):
        components = suggest_components(sample_data)

        assert components["map"]["class"] == "MapComponent"
        assert components["state"]["class"] == "LinesComponent"
        assert "batt" in components["state"]["keys"]
        assert components["pair_distance"]["class"] == "PairDistanceComponent"
        assert components["pair_distance"]["pairs"] == "all"

    def test_suggests_search_control_and_link_components_for_simulation_logs(self):
        data = SimulationLogAdapter().load(_simulation_log_with_search_and_links())

        components = suggest_components(data)

        assert components["coverage"]["keys"] == ["search_coverage"]
        assert components["search_heatmap"]["class"] == "SearchHeatmapComponent"
        assert components["control"]["keys"] == ["vx", "vy"]
        assert "link_quality" in components

    def test_suggests_parameter_sweep_components_for_summary_data(self):
        data = ParametricStudyAdapter().load(_parametric_summary())

        components = suggest_components(data)

        assert components["coverage"]["keys"] == ["final_coverage"]
        assert components["duration"]["keys"] == ["duration"]
