# Chain API Example

This example demonstrates the chain API for filtering and configuration.

## Chain methods

- `set_id_list([ids])` - Filter to specific robot IDs
- `set_first_seconds(n)` - Show first n seconds
- `set_last_seconds(n)` - Show last n seconds
- `set_time_range((start, end))` - Show specific time range
- `set_style(name)` - Apply style preset
- `set_palette(name)` - Apply color palette

## Usage pattern

Methods can be chained for fluent configuration:

```python
drawer = (StaticGlobalPlotDrawer(files=['data.json'], components=components)
    .set_id_list([1, 2])
    .set_time_range((1.0, 3.0))
    .set_palette('colorblind')
    .draw(['x', 'y'], save=True))
```

## Running the example

```bash
python generate_data.py
python main.py
```

## Examples included

1. Filter by robot IDs
2. First N seconds only
3. Last N seconds only
4. Custom time range
5. Multiple filters + palette
6. Style + palette customization
