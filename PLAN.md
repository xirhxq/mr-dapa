# mr-dapa Development Plan

## Context

`scripts/draw` is a visualization framework evolved from the CBF multi-UAV project, with 25+ specialized components, 4 drawing modes, and animation support. `mr-dapa` is the generalized extraction.

**Core Problem**: mr-dapa solves rapid visualization of multi-agent time-series data — researchers have N robots' timestamped data (possibly async, possibly from different files) and need to quickly generate multiple chart formats (global/grouped/separate/animation) for analysis and papers.

**Design Principles** (confirmed through discussion):
1. Interpreter view — `interpreter.for_robots([1])` returns an immutable view, no mutation
2. Full Adapter layer — support multi-file merge, CSV and other formats
3. Class attribute + config override — expand and other behavior decisions
4. Figure generation vs saving separation — `draw()` returns figure, saving is optional
5. Timestamp-based update — support async data (different robots, different timestamps)
6. Config-driven components — variants via config dict, not deep inheritance

---

## Phase 1: Architecture Refactoring ~~(Critical)~~ ✅

- [x] Bug fixes: file handle leak, operator precedence, globals()
- [x] BaseInterpreter immutable view with `for_*` factory methods
- [x] Components receive only interpreter (no `data` param)
- [x] Package modernization: pyproject.toml, clean imports

## Phase 2: Adapter System ~~(High)~~ ✅

- [x] DataAdapter Protocol
- [x] JSONAdapter, CSVAdapter, MultiFileAdapter, NumPyAdapter
- [x] DataLoader accepts adapter parameter
- [x] Canonical data format in README

## Phase 3: Component System ~~(High)~~ ✅

- [x] BaseComponent with `expand` class attribute
- [x] GridLayout uses expand attribute (no hardcoded 'map' check)
- [x] Enhanced LinesComponent: fill, bounds, show_zero_line, show_min, milestones
- [x] Enhanced MapComponent: trail lines, robot ID annotations, expand=False
- [x] New ScatterComponent
- [x] New FillComponent

## Phase 4: Drawer Improvements ~~(High)~~ ✅

- [x] `draw()` returns figure, no auto-save
- [x] `save=True` / `path=` for file output
- [x] AnimationDrawer blitting support

## Phase 5: Testing System ~~(High)~~ ✅

- [x] 127 tests: interpreter, adapters, components, drawers, grid layout
- [x] conftest.py with deterministic fixtures
- [x] All tests pass under `agg` backend

## Phase 7: Extensibility ~~(Medium)~~ ✅ (0.3.0)

- [x] `registry.py` with register/unregister/get/list functions
- [x] `BaseComponent.validate_config()` with `required_config_keys`
- [x] `BaseDrawer._validate_components()` early error detection with fuzzy matching
- [x] Public API: `__all__`, type hints, 18 exports
- [x] Custom component example (`examples/custom_component/`)
- [x] Developer guide in `.claude/CLAUDE.md`
- [ ] Entry-points based auto-discovery via `pyproject.toml` (deferred)

---

## Phase 6: Styling & Themes ~~(Medium)~~ ✅ (0.4.0)

- [x] StyleConfig dataclass with figure, font, line, color, export params
- [x] 3 presets: paper, presentation, dark
- [x] 4 palettes: default, colorblind (Wong), vivid, muted
- [x] `set_style()` / `set_palette()` chain API on BaseDrawer
- [x] SVG/PDF export via `style.format`
- [x] Dark theme with background/text color application
- [x] 18 new tests

---

## Phase 8: CI/CD & Release ~~(Medium)~~ ✅ (0.4.0)

- [x] GitHub Actions CI: test matrix (3.9-3.12) + ruff lint + pytest-cov
- [x] PyPI publish workflow with Trusted Publisher (OIDC)
- [x] Published to https://pypi.org/project/mr-dapa/

---

## Phase 9: Documentation & Examples ~~(Medium)~~ ✅ (0.5.0)

- [x] Google-style docstrings on all 20 public modules
- [x] Sphinx documentation with API reference and user guides
- [x] 7 new examples: csv_adapter, numpy_adapter, multi_file, all_components, all_draw_modes, publication_style, chain_api
- [x] Fixed with_menu example with proper error handling
- [x] docs CI workflow for GitHub Pages deployment

---

## Phase 10: Component Enhancements ~~(Low)~~ ✅ (0.6.0)

- [x] MapComponent `show_trail` toggle for trajectory visibility
- [x] HeatmapComponent for 2D density visualization
- [x] Map3DComponent for 3D position visualization

## Phase 11: InteractiveMenu Integration (Low)

- Integrate `basic-interactive-menu` as `mr_dapa.menu` subpackage

---

## Remaining TODO (from original README)

- [x] Toggle trace showing in 2D map (MapComponent `trail_style` toggle) ✅ Phase 10
- [x] Heatmap component ✅ Phase 10
- [x] Example with data transforming from other formats (CSV/NumPy adapter examples) ✅ Phase 9
- [x] 3D map ✅ Phase 10

---

## Dependencies

```
Phase 1-10 ✅ COMPLETE
Phase 11 (InteractiveMenu) ← Next
```

**Next: Phase 11 (InteractiveMenu Integration)**

---

## Verification

After each Phase:
1. `pytest tests/` all pass
2. `examples/minimal/main.py` generates correct plots
3. `pip install -e .` installs without error
