# All Draw Modes Example

This example demonstrates all four mr-dapa visualization modes.

## Drawer types

1. **StaticGlobalPlotDrawer** - All robots in shared subplots
2. **StaticSeparatePlotDrawer** - One figure per robot
3. **StaticGroupPlotDrawer** - Per-robot subplots in one figure
4. **AnimationDrawer** - Time-based MP4 animation

## Running the example

```bash
python generate_data.py
python main.py
```

## Output

- `static_global.png` - All robots overlaid on same axes
- Multiple separate figures (one per robot)
- `static_group.png` - Grid of robot-specific subplots
- `animation.mp4` - Animated visualization

## When to use each mode

- **StaticGlobal**: Comparing robot behavior on same scale
- **StaticSeparate**: Individual robot analysis, export to separate files
- **StaticGroup**: Side-by-side comparison of multiple robots
- **Animation**: Visualizing time evolution
