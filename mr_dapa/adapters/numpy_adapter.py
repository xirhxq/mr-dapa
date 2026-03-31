"""NumPy adapter for loading data from NumPy arrays."""

import numpy as np


class NumPyAdapter:
    """Adapter for converting NumPy arrays to canonical format.

    Expects a dict mapping robot IDs to data arrays. Each robot's data
    should have 'timestamps' and 'values' keys.

    Example::
        adapter = NumPyAdapter()
        data = adapter.load({
            1: {'timestamps': np.array([0, 1]), 'values': {'x': np.array([1, 2])}}
        })
    """

    def load(self, source) -> list[dict]:
        """Convert NumPy arrays to canonical format.

        Args:
            source: Dict mapping robot IDs to data dicts with arrays.

        Returns:
            List of dictionaries in canonical mr-dapa format.
        """
        if not isinstance(source, dict):
            raise TypeError(f"NumPyAdapter expects a dict, got {type(source)}")

import numpy as np


class NumPyAdapter:
    def load(self, source) -> list[dict]:
        if not isinstance(source, dict):
            raise TypeError(f"NumPyAdapter expects a dict, got {type(source)}")

        result = []
        for robot_id, robot_data in source.items():
            robot_id = int(robot_id)
            timestamp = robot_data.get('timestamp')
            if timestamp is not None:
                timestamp = np.asarray(timestamp).tolist()

            values = []
            for key, arr in robot_data.get('values', {}).items():
                val_arr = np.asarray(arr).tolist()
                ts = timestamp if timestamp is not None else list(range(len(val_arr)))
                if isinstance(ts, np.ndarray):
                    ts = ts.tolist()
                values.append({
                    'name': key,
                    'alias': key,
                    'unit': robot_data.get('units', {}).get(key, ''),
                    'timestamp': ts,
                    'value': val_arr,
                })

            entry = {'id': robot_id, 'values': values}
            if timestamp is not None:
                entry['timestamp'] = timestamp
            result.append(entry)
        return result
