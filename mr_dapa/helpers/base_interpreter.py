"""Base interpreter for data validation and filtering.

This module provides BaseInterpreter, which validates data in canonical
mr-dapa format and provides immutable filtered views via factory methods.
"""

import numpy as np


class BaseInterpreter:
    """Validates data and provides immutable filtered views.

    The interpreter loads data in canonical mr-dapa format, validates it,
    and provides factory methods for creating filtered views. All filtering
    methods (for_robots, for_time_range, etc.) return new BaseInterpreter
    instances rather than modifying the current one.

    Attributes:
        data: Filtered data in canonical format.
        id_list: List of robot IDs in the filtered view.
        time_range: Tuple of (start_time, end_time) for filtered view.

    Args:
        data: Data in canonical mr-dapa format.
        id_list: Optional list of robot IDs to filter to.
        time_range: Optional tuple of (start, end) times to filter to.
    """

    def __init__(self, data, id_list=None, time_range=None):
        self._origin = data
        self._check_data(data)
        self._full_id_list = [frame["id"] for frame in data]
        self._full_time_range = self._compute_full_time_range(data)

        self.id_list = [i for i in (id_list or self._full_id_list) if i in self._full_id_list]
        if time_range is not None:
            self.time_range = (
                max(time_range[0], self._full_time_range[0]),
                min(time_range[1], self._full_time_range[1]),
            )
        else:
            self.time_range = self._full_time_range
        self.data = self._filter_data(data, self.id_list, self.time_range)

    def for_robots(self, id_list):
        """Return a new interpreter filtered to specified robot IDs.

        Args:
            id_list: List of robot IDs to include.

        Returns:
            New BaseInterpreter instance with filtered data.
        """
        return BaseInterpreter(self._origin, id_list=id_list, time_range=self.time_range)

    def for_time_range(self, time_range):
        """Return a new interpreter filtered to specified time range.

        Args:
            time_range: Tuple of (start_time, end_time).

        Returns:
            New BaseInterpreter instance with filtered data.
        """
        return BaseInterpreter(self._origin, id_list=self.id_list, time_range=time_range)

    def for_first_seconds(self, seconds):
        """Return a new interpreter for the first N seconds of data.

        Args:
            seconds: Number of seconds from the start to include.

        Returns:
            New BaseInterpreter instance with filtered data.
        """
        full = self._full_time_range
        return self.for_time_range((full[0], min(full[1], full[0] + seconds)))

    def for_last_seconds(self, seconds):
        """Return a new interpreter for the last N seconds of data.

        Args:
            seconds: Number of seconds from the end to include.

        Returns:
            New BaseInterpreter instance with filtered data.
        """
        full = self._full_time_range
        return self.for_time_range((max(full[0], full[1] - seconds), full[1]))

    def get_robot_number(self):
        return len(self.data)

    def get_full_id_list(self):
        return list(self._full_id_list)

    def get_full_time_range(self):
        return self._full_time_range

    def get_title_suffix(self):
        if self.id_list == self._full_id_list:
            return ', All Robots'
        elif len(self.id_list) == 1:
            return f', Robot #{self.id_list[0]}'
        else:
            return f', Robots [{", ".join([f"#{i}" for i in self.id_list])}]'

    def get_id_suffix(self, id_list=None):
        id_list = id_list if id_list is not None else self.id_list
        if id_list == self._full_id_list and self.time_range == self._full_time_range:
            return ''
        suffix = ''
        if self.time_range != self._full_time_range:
            suffix += '-' + f'{self.time_range[0]:.2f}s' + '-' + f'{self.time_range[1]:.2f}s'
        if id_list != self._full_id_list:
            suffix += '-' + ''.join([f'#{i}' for i in id_list])
        return suffix

    def get_units(self, keys):
        units = set()
        for dt in self.data:
            for value in dt["values"]:
                if (value["name"] in keys or value["alias"] in keys) and value["unit"] not in units:
                    units.add(value["unit"])
                    break
        return list(units)

    def get_fps(self):
        fps_list = []
        for dt in self.data:
            for frame in dt["values"]:
                fps = (frame["timestamp"][-1] - frame["timestamp"][0]) / (len(frame["timestamp"]) - 1)
                fps_list.append(fps)
        return 1 / float(np.mean(fps_list))

    def _compute_full_time_range(self, data):
        timestamps = [frame["timestamp"] for frame in data if frame.get("timestamp")]
        if not timestamps:
            return (0.0, 0.0)
        return min(min(timestamps)), max(max(timestamps))

    def _filter_data(self, data, id_list, time_range):
        filtered = []
        for frame in data:
            if frame["id"] not in id_list:
                continue
            robot_ts = frame.get("timestamp", None)
            new_values = []
            for value in frame["values"]:
                ts = value.get("timestamp", robot_ts)
                if ts is None:
                    continue
                s = np.searchsorted(ts, time_range[0])
                e = np.searchsorted(ts, time_range[1], side="right")
                new_values.append({
                    "name": value["name"],
                    "alias": value["alias"],
                    "unit": value["unit"],
                    "timestamp": ts[s:e],
                    "value": value["value"][s:e],
                })
            filtered.append({"id": frame["id"], "values": new_values})
        return filtered

    def _check_data(self, data):
        assert isinstance(data, list), f"data should be a list, but got {type(data)}"
        for data_index, dt in enumerate(data):
            assert isinstance(dt, dict), f"data[{data_index}] should be a dict, but got {type(dt)}"
            assert "values" in dt, f"data[{data_index}] should have a 'values' key, but got {dt.keys()}"
            assert "id" in dt, f"data[{data_index}] should have an 'id' key, but got {dt.keys()}"
            assert isinstance(dt["values"], list), \
                f"data[{data_index}]['values'] should be a list, but got {type(dt['values'])}"
            for value_index, value in enumerate(dt["values"]):
                prefix = f"data[{data_index}]['values'][{value_index}]"
                assert isinstance(value, dict), f"{prefix} should be a dict, but got {type(value)}"
                assert "name" in value, f"{prefix} should have a 'name' key, but got {value.keys()}"
                assert "alias" in value, f"{prefix} should have a 'alias' key, but got {value.keys()}"
                assert "unit" in value, f"{prefix} should have a 'unit' key, but got {value.keys()}"
                assert "timestamp" in value or "timestamp" in dt, \
                    f"{prefix} or data[{data_index}] should have a 'timestamp' key, " \
                    f"but got {value.keys()} and {dt.keys()}"
                assert "value" in value, f"{prefix} should have a 'value' key, but got {value.keys()}"
                assert isinstance(value["value"], list), \
                    f"{prefix} should be a list, but got {type(value['value'])}"
                if "timestamp" not in value:
                    value["timestamp"] = dt["timestamp"]
                assert isinstance(value["timestamp"], list), \
                    f"{prefix}['timestamp'] should be a list, but got {type(value['timestamp'])}"
                assert len(value["timestamp"]) == len(value["value"]), \
                    f"{prefix}['timestamp'] should have the same length as {prefix}['value'], " \
                    f"but got {len(value['timestamp'])} and {len(value['value'])}"
