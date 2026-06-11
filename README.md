# mr-dapa — Multi-Robot Data Animation & Plotting Assistance

Rapid visualization of multi-agent time-series data. Researchers have N robots'
timestamped data and need to quickly generate static plots and animations.

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
| `HeatmapComponent` | 2D density heatmap |
| `Map3DComponent` | 3D position map with trajectories |
| `SearchHeatmapComponent` | First-search-time grid heatmap |
| `PairDistanceComponent` | Inter-robot distance and safety/communication range plots |

### Adapters

```python
from mr_dapa import CSVAdapter, MultiFileAdapter, NumPyAdapter, SimulationLogAdapter, ParametricStudyAdapter

loader = mrdp.StaticGlobalPlotDrawer(files=['data.csv'], components=components, adapter=CSVAdapter())
loader = mrdp.StaticGlobalPlotDrawer(files=['r1.json', 'r2.json'], components=components, adapter=MultiFileAdapter())
loader = mrdp.StaticGlobalPlotDrawer(files=['sim/data.json'], components=components, adapter=SimulationLogAdapter())
loader = mrdp.StaticGlobalPlotDrawer(files=['summary.json'], components=components, adapter=ParametricStudyAdapter())
```

`SimulationLogAdapter` is for frame-based simulation logs with
`state[*].runtime` and `state[*].robots[*]`. It extracts robot state,
control inputs, CBF-like metric dictionaries, link-denial metrics, and global
search coverage so existing line/map components can plot real simulation runs
quickly.

`ParametricStudyAdapter` is for parameter sweep summaries with a
`parametric_study` object. It maps parameter values onto the canonical x-axis
and exposes metrics such as `final_coverage` and `duration` for comparison
plots.

### Agent-Friendly Inspection

```python
data = mrdp.SimulationLogAdapter().load('sim/data.json')
summary = mrdp.inspect_data(data)
components = mrdp.suggest_components(data)

print(summary['robot_ids'])
mrdp.StaticGlobalPlotDrawer(
    files=['sim/data.json'],
    components=components,
    adapter=mrdp.SimulationLogAdapter(),
).draw(list(components), save=True)
```

### Interactive Menu

Install with `[menu]` extra and use `run_interactive_session()` for quick interactive visualization:

```python
from mr_dapa import run_interactive_session

run_interactive_session(data_folder="data", file_pattern="*.json")
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
pip install mr-dapa
pip install mr-dapa[menu]   # includes basic-interactive-menu for interactive CLI
pip install -e ".[dev]"    # development: pytest, ruff
```

## Testing

```bash
pytest tests/               # 168 tests
pytest tests/ -v             # verbose
pytest tests/ -k "adapter"   # filter by name
```

Test structure: `conftest.py` provides shared fixtures. Each `test_*.py`
covers one module.

## License

MIT
