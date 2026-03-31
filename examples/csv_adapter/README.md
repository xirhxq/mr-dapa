# CSV Adapter Example

This example demonstrates how to load multi-robot data from CSV files using the `CSVAdapter`.

## Running the example

```bash
python generate_data.py
python main.py
```

## What it demonstrates

- Loading data from CSV format
- Custom column name configuration (robot_id, time, etc.)
- Using CSVAdapter with all drawer types

## CSV Format

The CSV file should have columns for:
- Robot ID (configurable via `id_col`)
- Timestamp (configurable via `timestamp_col`)
- Value columns (one or more)
