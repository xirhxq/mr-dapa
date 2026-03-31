"""Base drawer class for all visualization modes.

This module defines BaseDrawer, the abstract base class for all drawer
types (StaticGlobal, StaticSeparate, StaticGroup, Animation). Drawers
coordinate data loading, component configuration, style application,
and figure saving.
"""

import os

from ..helpers.loader import DataLoader
from ..helpers.base_interpreter import BaseInterpreter
from ..registry import get_component_class, list_components
from ..style import StyleConfig, get_style, get_palette

import matplotlib.pyplot as plt


class BaseDrawer:
    """Base class for all visualization drawers.

    Drawers load data, configure components, apply styles, and generate
    figures. Subclasses implement the draw() method for specific
    visualization modes (global, separate, grouped, animation).

    Attributes:
        BAR_FORMAT: Progress bar format string for tqdm.
        REGISTERED_COMPONENTS: Dict mapping component names to configs.

    Args:
        files: List of file paths to load data from.
        components: Dict mapping component names to configuration dicts.
            Each config must have a 'class' key with the component class name.
        interpreter: Optional BaseInterpreter subclass. If None, uses
            BaseInterpreter directly.
        adapter: Optional DataAdapter for custom data loading.
    """

    BAR_FORMAT = "{percentage:3.0f}%|{bar:50}| {n_fmt}/{total_fmt} [elap: {elapsed}s eta: {remaining}s]"
    REGISTERED_COMPONENTS = {}

    def __init__(self, files: list[str], components: dict, interpreter=None, adapter=None):
        self.loader = DataLoader(files, adapter=adapter)
        self.data = self.loader.data
        self.folder = self.loader.folder

        self.REGISTERED_COMPONENTS.update(components)
        self._validate_components(components)

        self.interpreter = BaseInterpreter(self.data) if interpreter is None else interpreter(self.data)
        self.style = StyleConfig()

        plt.switch_backend('agg')

    def set_style(self, name: str):
        """Apply a named style preset to the visualization.

        Args:
            name: Style preset name ('paper', 'presentation', 'dark').

        Returns:
            self, for method chaining.
        """
        self.style = get_style(name)
        return self

    def set_palette(self, name: str):
        """Apply a named color palette to the visualization.

        Args:
            name: Palette name ('default', 'colorblind', 'vivid', 'muted').

        Returns:
            self, for method chaining.
        """
        self.style.palette = get_palette(name)
        return self

    def _validate_components(self, components: dict) -> None:
        for name, config in components.items():
            if 'class' not in config:
                raise ValueError(
                    f"Component '{name}': missing required key 'class'. "
                    f"Available components: {list(list_components().keys())}"
                )
            cls = get_component_class(config['class'])
            cls.validate_config(name, config)

    def decide_sole_figsize(self, plot_list):
        if len(plot_list) > 1:
            return
        cls = get_component_class(self.REGISTERED_COMPONENTS[plot_list[0]]['class'])
        self.style.figsize = cls.FIGSIZE

    def set_id_list(self, id_list):
        """Filter data to only include specified robot IDs.

        Args:
            id_list: List of robot IDs to include.

        Returns:
            self, for method chaining.
        """
        self.interpreter = self.interpreter.for_robots(id_list)
        return self

    def set_first_seconds(self, first_seconds):
        """Filter data to only include the first N seconds.

        Args:
            first_seconds: Number of seconds from start to include.

        Returns:
            self, for method chaining.
        """
        self.interpreter = self.interpreter.for_first_seconds(first_seconds)
        return self

    def set_last_seconds(self, last_seconds):
        """Filter data to only include the last N seconds.

        Args:
            last_seconds: Number of seconds from end to include.

        Returns:
            self, for method chaining.
        """
        self.interpreter = self.interpreter.for_last_seconds(last_seconds)
        return self

    def set_time_range(self, time_range):
        """Filter data to only include a specific time range.

        Args:
            time_range: Tuple of (start_time, end_time).

        Returns:
            self, for method chaining.
        """
        self.interpreter = self.interpreter.for_time_range(time_range)
        return self

    def _check_plot_type(self, plot_type):
        if plot_type not in self.REGISTERED_COMPONENTS:
            raise ValueError(
                f"Plot type '{plot_type}' is not registered. "
                f"Available types: {list(self.REGISTERED_COMPONENTS.keys())}"
            )

    def _check_plot_list(self, plot_list):
        if any(plot_type not in self.REGISTERED_COMPONENTS for plot_type in plot_list):
            raise ValueError(
                f"Some plot types in {plot_list} are not registered. "
                f"Available types: {list(self.REGISTERED_COMPONENTS.keys())}"
            )

    def _check_class(self, class_name):
        return get_component_class(class_name)

    def _make_file(self, plot_name):
        filename = self.loader.file.split('/')[-1].split('.')[0]
        folder = os.path.join(self.folder, filename + '-plots')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder, plot_name)

    def _get_export_extension(self):
        fmt = self.style.format
        if fmt in ('svg', 'pdf'):
            return f'.{fmt}'
        return '.png'

    def _save_figure(self, fig, plot_list, id_list=None, grouped=False, path=None):
        ext = self._get_export_extension()
        if path:
            filename = path
        else:
            filename = self._make_file(self._make_filename(plot_list, id_list))
            if grouped:
                filename += '-grouped'
            filename += ext
        fig.savefig(filename, dpi=self.style.dpi, bbox_inches='tight', format=self.style.format)
        return filename

    def _save_animation(self, ani, plot_list, id_list, time_ratio, fps, path=None):
        if path:
            filename = path
        else:
            filename = self._make_file(self._make_filename(plot_list, id_list))
            fps_str = f'{fps:.1f}' if fps < 1 else f'{fps:.0f}'
            filename += f'-{time_ratio:.1g}x-{fps_str}fps.mp4'
        ani.save(filename, writer='ffmpeg', fps=fps, dpi=self.style.dpi)
        return filename

    def _make_filename(self, plot_list, id_list=None):
        filename = '-'.join([self.REGISTERED_COMPONENTS[plot_type]["filename"] if "filename" in self.REGISTERED_COMPONENTS[plot_type] else plot_type for plot_type in plot_list])
        return filename + self.interpreter.get_id_suffix(id_list=id_list)

    def _apply_style_to_fig(self, fig):
        if self.style.background != 'white':
            fig.set_facecolor(self.style.background)
        if self.style.tight_layout:
            fig.set_tight_layout(True)

    def _apply_style_to_ax(self, ax):
        ax.title.set_fontsize(self.style.title_size)
        ax.xaxis.label.set_fontsize(self.style.label_size)
        ax.yaxis.label.set_fontsize(self.style.label_size)
        ax.tick_params(labelsize=self.style.tick_size)
        if self.style.background != 'white':
            ax.set_facecolor(self.style.background)
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')

    def _get_robot_color(self, robot_index):
        if self.style.palette:
            return self.style.palette[robot_index % len(self.style.palette)]
        return None
