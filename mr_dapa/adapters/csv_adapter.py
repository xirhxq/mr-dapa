import csv


class CSVAdapter:
    def __init__(self, id_col='id', timestamp_col='timestamp', separator=','):
        self.id_col = id_col
        self.timestamp_col = timestamp_col
        self.separator = separator

    def load(self, source) -> list[dict]:
        if not isinstance(source, str):
            raise TypeError(f"CSVAdapter expects a file path, got {type(source)}")

        robots = {}
        with open(source, newline='') as f:
            reader = csv.DictReader(f, delimiter=self.separator)
            for row in reader:
                robot_id = int(row[self.id_col])
                if robot_id not in robots:
                    robots[robot_id] = {'timestamps': [], 'values': {}}

                ts = float(row[self.timestamp_col])
                robots[robot_id]['timestamps'].append(ts)

                for col in row:
                    if col in (self.id_col, self.timestamp_col):
                        continue
                    if col not in robots[robot_id]['values']:
                        robots[robot_id]['values'][col] = {'timestamps': [], 'value': []}
                    robots[robot_id]['values'][col]['timestamps'].append(ts)
                    robots[robot_id]['values'][col]['value'].append(float(row[col]))

        result = []
        for robot_id in sorted(robots.keys()):
            r = robots[robot_id]
            values = []
            for name, v in r['values'].items():
                values.append({
                    'name': name,
                    'alias': name,
                    'unit': '',
                    'timestamp': v['timestamps'],
                    'value': v['value'],
                })
            result.append({
                'id': robot_id,
                'timestamp': r['timestamps'],
                'values': values,
            })
        return result
