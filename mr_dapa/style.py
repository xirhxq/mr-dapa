"""Style configuration for plot appearance."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StyleConfig:
    """Configuration for plot styling and export.

    Attributes:
        figsize: Figure size (width, height) in inches.
        dpi: DPI for saved figures.
        title_size: Font size for plot titles.
        label_size: Font size for axis labels.
        tick_size: Font size for tick labels.
        line_width: Line width for plots.
        palette: Color palette as list of hex codes.
        format: Export format ('png', 'svg', 'pdf').
        background: Background color ('white' or color name).
        tight_layout: Whether to use tight layout.
        bbox_inches: Matplotlib bbox_inches value for saved figures.
    """

    figsize: tuple = (16, 9)
    dpi: int = 300
    tight_layout: bool = True

    title_size: int = 14
    label_size: int = 12
    legend_size: int = 10
    tick_size: int = 10

    line_width: float = 1.5
    grid_alpha: float = 0.3

    palette: list = field(default_factory=list)
    background: str = 'white'

    format: str = 'png'
    bbox_inches: Optional[str] = 'tight'


PALETTES = {
    'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
    'colorblind': ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#999999', '#444444'],
    'vivid': ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4'],
    'muted': ['#4878d0', '#ee854a', '#6acc64', '#d65f5f', '#956cb4', '#8c613c', '#dc7ec0', '#797979', '#d5bb67', '#82c6e2'],
}

PRESETS = {
    'paper': StyleConfig(
        figsize=(8, 6),
        dpi=300,
        tight_layout=True,
        title_size=16,
        label_size=14,
        legend_size=12,
        tick_size=12,
        line_width=1.5,
        grid_alpha=0.2,
        palette=PALETTES['default'],
        background='white',
        format='png',
    ),
    'presentation': StyleConfig(
        figsize=(16, 9),
        dpi=150,
        tight_layout=True,
        title_size=20,
        label_size=16,
        legend_size=14,
        tick_size=14,
        line_width=2.5,
        grid_alpha=0.3,
        palette=PALETTES['vivid'],
        background='white',
        format='png',
    ),
    'dark': StyleConfig(
        figsize=(16, 9),
        dpi=150,
        tight_layout=True,
        title_size=18,
        label_size=14,
        legend_size=12,
        tick_size=12,
        line_width=2.0,
        grid_alpha=0.2,
        palette=PALETTES['vivid'],
        background='#1a1a2e',
        format='png',
    ),
}


def get_style(name: str) -> StyleConfig:
    if name not in PRESETS:
        raise ValueError(f"Unknown style '{name}'. Available: {list(PRESETS.keys())}")
    from dataclasses import asdict
    return StyleConfig(**asdict(PRESETS[name]))


def get_palette(name: str) -> list:
    if name not in PALETTES:
        raise ValueError(f"Unknown palette '{name}'. Available: {list(PALETTES.keys())}")
    return list(PALETTES[name])
