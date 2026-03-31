# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-03-31

### Added

- **Style System**: `StyleConfig` dataclass with presets, palettes, and export control
- **3 Presets**: `paper` (8x6, high DPI), `presentation` (16x9, bold), `dark` (dark background)
- **4 Palettes**: `default`, `colorblind` (Wong), `vivid`, `muted`
- **Chain API**: `drawer.set_style('paper').set_palette('colorblind').draw([...])`
- **SVG/PDF Export**: set `style.format = 'svg'` or `'pdf'` for vector output
- **Dark Theme**: applies dark background and light text colors to all axes
- 18 new tests (145 total)

## [0.3.0] - 2026-03-30

### Added

- **Component Registry**: dynamic registration via `register_component()`, `unregister_component()`, `get_component_class()`, `list_components()`
- **Config Validation**: `BaseComponent.validate_config()` checks `required_config_keys` at drawer init time
- **Fuzzy Error Messages**: unknown component class names suggest closest match (e.g. `'LinesCompnent'` → `'LinesComponent'`)
- **Custom Component Example**: `examples/custom_component/` with a BarComponent
- **Public API**: `__all__` with 18 exported symbols

### Changed

- `_COMPONENT_CLASSES` dict replaced by `mr_dapa/registry.py` module
- `GridLayout` uses registry instead of hardcoded imports
- `BaseDrawer.__init__` validates all component configs before any drawing

## [0.2.0] - 2026-03-30

### Added

- **Adapter System**: pluggable data loading via `DataAdapter` protocol
  - `JSONAdapter`: load from JSON files or lists (default)
  - `CSVAdapter`: parse CSV files into canonical format
  - `MultiFileAdapter`: merge multiple files (one robot per file)
  - `NumPyAdapter`: convert numpy arrays to canonical format
- **New Components**:
  - `ScatterComponent`: scatter/phase plots (two arbitrary keys vs each other)
  - `FillComponent`: filled area plots (uncertainty bands, confidence intervals)
- **Enhanced LinesComponent** config-driven features:
  - `fill`: fill between line and zero
  - `bounds`: horizontal reference lines
  - `show_zero_line`: y=0 dashed reference
  - `show_min`: annotate minimum value
  - `milestones`: vertical timestamp markers
- **Enhanced MapComponent**:
  - Trajectory trail lines
  - Robot ID annotations
  - Configurable `trail_style` and `marker_style`
  - `expand = False` class attribute (replaces GridLayout hardcoding)
- **Drawer improvements**:
  - `draw()` returns figure by default (no auto-save)
  - `save=True` or `path=` to trigger file output
  - `AnimationDrawer` supports blitting when components return artists
- **Testing System**: 127 tests covering interpreter, adapters, components, drawers, grid layout
- `pyproject.toml` replaces `setup.py`

### Changed

- **BaseInterpreter**: immutable view pattern — `for_robots()`, `for_time_range()`, `for_first_seconds()`, `for_last_seconds()` return new instances instead of mutating
- **GridLayout**: uses component `expand` class attribute instead of hardcoded `'map'` check
- **BaseComponent**: `expand` class attribute controls grid expansion behavior
- **Component `update()`**: returns list of matplotlib artists for blitting support
- All `from ... import *` star imports replaced with explicit imports

### Fixed

- File handle leak in `DataLoader` (`json.load(open(file))` → `with open()`)
- Operator precedence bug in `BaseInterpreter.get_units()`
- `globals()` lookup in `BaseDrawer._check_class()` → explicit `_COMPONENT_CLASSES` dict

## [0.1.0] - 2026-03-28

### Added

- Initial release with `LinesComponent` and `MapComponent`
- Four drawer modes: `StaticGlobalPlotDrawer`, `StaticSeparatePlotDrawer`, `StaticGroupPlotDrawer`, `AnimationDrawer`
- Chain API: `drawer.set_id_list([...]).set_time_range((...)).draw([...])`
- `BaseInterpreter` for data validation and filtering
- `GridLayout` for automatic subplot allocation
- Minimal example with data generation

[0.2.0]: https://github.com/xxx/mr-dapa/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/xxx/mr-dapa/releases/tag/v0.1.0
