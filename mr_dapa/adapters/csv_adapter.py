"""CSV adapter for loading data from CSV files."""

import csv


class CSVAdapter:
    """Adapter for loading CSV files into mr-dapa canonical format.

    Expects a CSV with columns for robot ID, timestamp, and one or more
    value columns. By default, looks for 'id' and 'timestamp' columns,
    with all other columns treated as value series.

    Example::
        adapter = CSVAdapter(id_col='robot_id', timestamp_col='time')
        data = adapter.load('data.csv')
    """

    def __init__(self, id_col='id', timestamp_col='timestamp', separator=','):
        """Initialize CSV adapter.

        Args:
            id_col: Name of column containing robot IDs.
            timestamp_col: Name of column containing timestamps.
            separator: CSV delimiter character.
        """
        self.id_col = id_col
        self.timestamp_col = timestamp_col
        self.separator = separator

    def load(self, source) -> list[dict]:
        """Load data from CSV file.

        Args:
            source: Path to CSV file.

        Returns:
            List of dictionaries in canonical mr-dapa format.

        Raises:
            TypeError: If source is not a string.
        """
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
