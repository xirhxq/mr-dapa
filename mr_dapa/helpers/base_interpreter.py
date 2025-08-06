from ..helpers.utils import *

class BaseInterpreter:
    def __init__(self, data):
        self.origin = data
        self.data = data
        self._check_data()
        self.id_list = self.get_full_id_list()
        self.time_range = self.get_full_time_range()

    def get_robot_number(self):
        return len(self.data)

    def get_full_id_list(self):
        return [frame["id"] for frame in self.origin]

    def set_id_list(self, id_list):
        self.id_list = [id for id in id_list if id in self.get_full_id_list()]
        self._chop_from_origin()

    def get_full_time_range(self):
        timestamps = [frame["timestamp"] for frame in self.origin]
        return min(min(timestamps)), max(max(timestamps))

    def set_first_seconds(self, first_seconds):
        full_time_range = self.get_full_time_range()
        self.time_range = full_time_range[0], min(full_time_range[1], full_time_range[0] + first_seconds)
        self._chop_from_origin()

    def set_last_seconds(self, last_seconds):
        full_time_range = self.get_full_time_range()
        self.time_range = max(full_time_range[0], full_time_range[1] - last_seconds), full_time_range[1]
        self._chop_from_origin()

    def set_time_range(self, time_range):
        assert time_range[0] <= time_range[1], "time_range[0] should be less than time_range[1]"
        full_time_range = self.get_full_time_range()
        self.time_range = max(time_range[0], full_time_range[0]), min(time_range[1], full_time_range[1])
        self._chop_from_origin()

    def _chop_id(self):
        self.data = [frame for frame in self.data if frame["id"] in self.id_list]

    def _chop_time_range(self):
        for robot in self.data:
            for value in robot["values"]:
                index_range = np.searchsorted(value["timestamp"], self.time_range[0]), np.searchsorted(value["timestamp"], self.time_range[1], side="right")
                value["timestamp"] = value["timestamp"][index_range[0]:index_range[1]]
                value["value"] = value["value"][index_range[0]:index_range[1]]

    def _chop_from_origin(self):
        self.data = [frame for frame in self.origin if frame["id"] in self.id_list]
        self._chop_time_range()

    def _check_data(self):
        assert isinstance(self.data, list), f"self.data should be a list, but got {type(self.data)}"
        for data_index, dt in enumerate(self.data):
            assert isinstance(dt, dict), f"self.data[{data_index}] should be a dict, but got {type(dt)}"
            assert "values" in dt, f"self.data[{data_index}] should have a 'values' key, but got {dt.keys()}"
            assert "id" in dt, f"self.data[{data_index}] should have an 'id' key, but got {dt.keys()}"
            assert isinstance(dt["values"], list), \
                f"self.data[{data_index}]['values'] should be a list, but got {type(dt['values'])}"
            for value_index, value in enumerate(dt["values"]):
                prefix = f"self.data[{data_index}]['values'][{value_index}]"
                assert isinstance(value, dict), f"{prefix} should be a dict, but got {type(value)}"
                assert "name" in value, f"{prefix} should have a 'name' key, but got {value.keys()}"
                assert "alias" in value, f"{prefix} should have a 'alias' key, but got {value.keys()}"
                assert "unit" in value, f"{prefix} should have a 'unit' key, but got {value.keys()}"
                assert "timestamp" in value or "timestamp" in dt, \
                    f"{prefix} or self.data[{data_index}] should have a 'timestamp' key, " \
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

    def get_title_suffix(self):
        if self.id_list == self.get_full_id_list():
            return ', All Robots'
        else:
            return f', Robots [{", ".join([f"#{id}" for id in self.id_list])}]'

    def get_id_suffix(self, id_list=None):
        id_list = id_list if id_list is not None else self.id_list
        if id_list == self.get_full_id_list() and self.time_range == self.get_full_time_range():
            return ''
        suffix = ''
        if self.time_range != self.get_full_time_range():
            suffix += '-' + f'{self.time_range[0]:.2f}s' + '-' + f'{self.time_range[1]:.2f}s'
        if id_list != self.get_full_id_list():
            suffix += '-' + ''.join([f'#{id}' for id in id_list])
        return suffix

    def get_units(self, keys):
        units = set()
        for dt in self.data:
            for value in dt["values"]:
                if value["name"] or value["alias"] in keys and value["unit"] not in units:
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