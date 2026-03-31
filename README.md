# mr-dapa — Multi-Robot Data Animation & Plotting Assistance

Rapid visualization of multi-agent time-series data. Researchers have N robots' timestamped data (possibly async, possibly from different sources) and need to quickly generate static plots and animations.

## Quick Start

```bash
pip install -e .
python examples/minimal/generate_data.py
python examples/minimal/main.py
```

## API Overview

```python
import mr_dapa as mrdp

components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'map': {'title': 'Map', 'class': 'MapComponent', 'limits': {"x": [-3, 7], "y": [-3, 7]}},
}

# Static plot — returns figure (no file saved)
fig = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components).draw(['x', 'map'])

# Chain API for filtering
mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components) \
    .set_id_list([1, 3]) \
    .set_time_range((0.2, 0.5)) \
    .draw(['x'], save=True)                # save=True writes to file

# Animation
mrdp.AnimationDrawer(files=['data.json'], components=components) \
    .draw(['x', 'map'], time_ratio=2, save=True)
```

### Draw Modes

| Drawer | Behavior |
|--------|----------|
| `StaticGlobalPlotDrawer` | All robots in shared subplots |
| `StaticSeparatePlotDrawer` | One figure per robot |
| `StaticGroupPlotDrawer` | All robots, per-robot subplots in one figure |
| `AnimationDrawer` | Time-based MP4 animation |

### Components

| Component | Description |
|-----------|-------------|
| `LinesComponent` | Time-series line plots |
| `MapComponent` | 2D position map with trails |
| `ScatterComponent` | Scatter/phase plot (x vs y) |
| `FillComponent` | Filled area between values |

### Adapters

```python
from mr_dapa import CSVAdapter, MultiFileAdapter, NumPyAdapter

loader = mrdp.StaticGlobalPlotDrawer(files=['data.csv'], components=components, adapter=CSVAdapter())
loader = mrdp.StaticGlobalPlotDrawer(files=['r1.json', 'r2.json'], components=components, adapter=MultiFileAdapter())
```

## Data Format

Canonical JSON format (each robot has its own timestamp array — supports async data):

```json
[
  {
    "id": 1,
    "timestamp": [0.0, 0.02, 0.04],
    "values": [
      {"name": "X Position", "alias": "x", "unit": "m", "value": [1.0, 1.1, 1.2]},
      {"name": "Y Position", "alias": "y", "unit": "m", "value": [2.0, 2.1, 2.2]}
    ]
  }
]
```

## Requirements

- Python >= 3.9
- numpy, matplotlib, tqdm
- ffmpeg (for animation export)

## Installation

```bash
pip install -e .
pip install -e ".[dev]"   # includes pytest, ruff
```

## Testing

```bash
pytest tests/               # 145 tests
pytest tests/ -v             # verbose
pytest tests/ -k "adapter"   # filter by name
```

Test structure: `conftest.py` provides shared fixtures (sample_data, interpreter, components_config). Each `test_*.py` covers one module.

## License

MIT
