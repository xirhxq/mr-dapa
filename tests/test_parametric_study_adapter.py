import json

import pytest

from mr_dapa.adapters.parametric_study_adapter import ParametricStudyAdapter
from mr_dapa.helpers.base_interpreter import BaseInterpreter
from mr_dapa.helpers.loader import DataLoader


def _summary():
    return {
        "parametric_study": {
            "parameter_name": "cbfs.without-slack.comm-fixed.max-range",
            "parameter_values": [650.0, 850.0, 1050.0],
            "num_runs": 3,
            "timestamp": "2026-01-29_17-32-03",
            "results": [
                {
                    "parameter_value": 650.0,
                    "duration": 349.5,
                    "final_coverage": 68.56,
                    "data_folder": "2026-01-29_17-31-07",
                },
                {
                    "parameter_value": 850.0,
                    "duration": 289.0,
                    "final_coverage": 100.0,
                    "data_folder": "2026-01-29_17-31-26",
                },
                {
                    "parameter_value": 1050.0,
                    "duration": 300.0,
                    "final_coverage": 100.0,
                    "data_folder": "2026-01-29_17-31-45",
                },
            ],
        }
    }


def _value(summary, alias):
    for item in summary["values"]:
        if item["alias"] == alias:
            return item
    raise AssertionError(f"missing value alias {alias}")


class TestParametricStudyAdapter:
    def test_converts_summary_to_canonical_metric_series(self):
        result = ParametricStudyAdapter().load(_summary())

        assert len(result) == 1
        summary = result[0]
        assert summary["id"] == "cbfs.without-slack.comm-fixed.max-range"
        assert summary["timestamp"] == [650.0, 850.0, 1050.0]
        assert _value(summary, "final_coverage")["unit"] == "%"
        assert _value(summary, "final_coverage")["value"] == [68.56, 100.0, 100.0]
        assert _value(summary, "duration")["unit"] == "s"
        assert _value(summary, "duration")["value"] == [349.5, 289.0, 300.0]
        assert _value(summary, "run_index")["value"] == [0.0, 1.0, 2.0]
        assert BaseInterpreter(result).get_robot_number() == 1

    def test_loads_single_file_list_from_data_loader(self, tmp_path):
        summary_file = tmp_path / "summary.json"
        summary_file.write_text(json.dumps(_summary()))

        loader = DataLoader(str(summary_file), adapter=ParametricStudyAdapter())

        assert loader.data[0]["id"] == "cbfs.without-slack.comm-fixed.max-range"
        assert _value(loader.data[0], "final_coverage")["value"] == [68.56, 100.0, 100.0]

    def test_rejects_summary_without_parametric_study(self):
        with pytest.raises(ValueError, match="parametric_study"):
            ParametricStudyAdapter().load({"results": []})
