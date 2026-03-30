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
