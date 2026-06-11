"""Adapter for parametric study summary files."""

import json
from numbers import Number
from pathlib import Path


class ParametricStudyAdapter:
    """Load parametric study summaries into mr-dapa canonical format."""

    DEFAULT_UNITS = {
        "duration": "s",
        "final_coverage": "%",
        "run_index": "",
        "parameter_value": "",
    }

    def __init__(self, id_key="parameter_name", summary_key="parametric_study"):
        self.id_key = id_key
        self.summary_key = summary_key

    def load(self, source) -> list[dict]:
        data = self._load_source(source)
        if not isinstance(data, dict) or self.summary_key not in data:
            raise ValueError(f"ParametricStudyAdapter expects a dict with a '{self.summary_key}' key")

        study = data[self.summary_key]
        results = study.get("results", [])
        parameter_values = self._parameter_values(study, results)
        study_id = study.get(self.id_key, self.summary_key)

        metrics = {
            "parameter_value": list(parameter_values),
            "run_index": [float(index) for index in range(len(parameter_values))],
        }

        for result in results:
            for key, value in result.items():
                if key == "parameter_value" or not self._is_number(value):
                    continue
                metrics.setdefault(key, []).append(float(value))

        values = []
        for key, series in metrics.items():
            if len(series) != len(parameter_values):
                continue
            values.append({
                "name": key,
                "alias": key,
                "unit": self.DEFAULT_UNITS.get(key, ""),
                "timestamp": list(parameter_values),
                "value": series,
            })

        return [{
            "id": study_id,
            "timestamp": list(parameter_values),
            "values": values,
        }]

    def _load_source(self, source):
        if isinstance(source, (str, Path)):
            with open(source) as f:
                return json.load(f)

        if isinstance(source, list):
            if len(source) == 1 and isinstance(source[0], (str, Path)):
                return self._load_source(source[0])
            raise ValueError("ParametricStudyAdapter expects one summary file")

        if isinstance(source, dict):
            return source

        raise TypeError(f"ParametricStudyAdapter expects a path, dict, or list, got {type(source).__name__}")

    def _parameter_values(self, study, results):
        if results:
            return [float(result.get("parameter_value", index)) for index, result in enumerate(results)]
        return [float(value) for value in study.get("parameter_values", [])]

    def _is_number(self, value):
        return isinstance(value, Number) and not isinstance(value, bool)
