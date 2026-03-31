# NumPy Adapter Example

This example demonstrates how to load multi-robot data from NumPy arrays using the `NumPyAdapter`.

## Running the example

```bash
python main.py
```

## What it demonstrates

- Loading data from NumPy arrays in memory
- Using NumPyAdapter for direct array-to-visualization workflow
- No intermediate file storage needed

## NumPy Format

The NumPy data should be a dict mapping robot IDs to data dicts:
```python
{
    1: {
        'timestamps': np.array([...]),
        'values': {
            'x': np.array([...]),
            'y': np.array([...])
        }
    }
}
```
