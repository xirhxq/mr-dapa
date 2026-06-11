"""mr-dapa: Multi-Robot Data Animation & Plotting Assistance.

A Python library for rapid visualization of multi-agent time-series data.
Researchers can load data from various formats (JSON, CSV, NumPy), filter
by robot IDs and time ranges, and generate static plots or animations
with multiple visualization components.

Main exports:
    Drawers: StaticGlobalPlotDrawer, StaticSeparatePlotDrawer,
        StaticGroupPlotDrawer, AnimationDrawer
    Components: LinesComponent, MapComponent, ScatterComponent,
        FillComponent, HeatmapComponent, Map3DComponent, SearchHeatmapComponent,
        PairDistanceComponent, BaseComponent
    Adapters: DataAdapter, JSONAdapter, CSVAdapter, MultiFileAdapter,
        NumPyAdapter, SimulationLogAdapter, ParametricStudyAdapter
    Registry: register_component, unregister_component,
        get_component_class, list_components
    Inspection: inspect_data, suggest_components
    Style: StyleConfig, get_style, get_palette
    Menu: run_interactive_session (requires [menu] extra)
"""

from .drawers.drawers import (
    StaticGlobalPlotDrawer,
    StaticSeparatePlotDrawer,
    StaticGroupPlotDrawer,
    AnimationDrawer,
)

from .components.components import (
    LinesComponent,
    MapComponent,
    ScatterComponent,
    FillComponent,
    HeatmapComponent,
    Map3DComponent,
    SearchHeatmapComponent,
    PairDistanceComponent,
)

from .adapters import (
    DataAdapter,
    JSONAdapter,
    MultiFileAdapter,
    CSVAdapter,
    NumPyAdapter,
    SimulationLogAdapter,
    ParametricStudyAdapter,
)

from .registry import (
    register_component,
    unregister_component,
    get_component_class,
    list_components,
)

from .components.base import BaseComponent

from .inspection import inspect_data, suggest_components

from .style import StyleConfig, get_style, get_palette

try:
    from .menu import run_interactive_session  # noqa: F401
    _menu_available = True
except ImportError:
    _menu_available = False

__version__ = '1.0.1'

__all__ = [
    'StaticGlobalPlotDrawer',
    'StaticSeparatePlotDrawer',
    'StaticGroupPlotDrawer',
    'AnimationDrawer',
    'LinesComponent',
    'MapComponent',
    'ScatterComponent',
    'FillComponent',
    'HeatmapComponent',
    'Map3DComponent',
    'SearchHeatmapComponent',
    'PairDistanceComponent',
    'BaseComponent',
    'DataAdapter',
    'JSONAdapter',
    'MultiFileAdapter',
    'CSVAdapter',
    'NumPyAdapter',
    'SimulationLogAdapter',
    'ParametricStudyAdapter',
    'register_component',
    'unregister_component',
    'get_component_class',
    'list_components',
    'inspect_data',
    'suggest_components',
    'StyleConfig',
    'get_style',
    'get_palette',
]

if _menu_available:
    __all__.extend(['run_interactive_session'])
