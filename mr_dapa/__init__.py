"""mr-dapa: Multi-Robot Data Animation & Plotting Assistance.

A Python library for rapid visualization of multi-agent time-series data.
Researchers can load data from various formats (JSON, CSV, NumPy), filter
by robot IDs and time ranges, and generate static plots or animations
with multiple visualization components.

Main exports:
    Drawers: StaticGlobalPlotDrawer, StaticSeparatePlotDrawer,
        StaticGroupPlotDrawer, AnimationDrawer
    Components: LinesComponent, MapComponent, ScatterComponent,
        FillComponent, HeatmapComponent, Map3DComponent, BaseComponent
    Adapters: DataAdapter, JSONAdapter, CSVAdapter, MultiFileAdapter,
        NumPyAdapter
    Registry: register_component, unregister_component,
        get_component_class, list_components
    Style: StyleConfig, get_style, get_palette
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
)

from .adapters import (
    DataAdapter,
    JSONAdapter,
    MultiFileAdapter,
    CSVAdapter,
    NumPyAdapter,
)

from .registry import (
    register_component,
    unregister_component,
    get_component_class,
    list_components,
)

from .components.base import BaseComponent

from .style import StyleConfig, get_style, get_palette

__version__ = '0.6.0'

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
    'BaseComponent',
    'DataAdapter',
    'JSONAdapter',
    'MultiFileAdapter',
    'CSVAdapter',
    'NumPyAdapter',
    'register_component',
    'unregister_component',
    'get_component_class',
    'list_components',
    'StyleConfig',
    'get_style',
    'get_palette',
]
