# Simulation Log Adapter Example

This example shows how to plot a frame-based multi-robot simulation log with
`SimulationLogAdapter`.

```bash
python examples/simulation_log_adapter/generate_data.py
python examples/simulation_log_adapter/main.py
```

The generated figures include trajectory, first-search-time heatmap, battery,
control input, search coverage, formation distance, and link-denial status
plots from a single `data.json` simulation log.
