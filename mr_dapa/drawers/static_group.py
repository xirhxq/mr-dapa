"""Static group plot drawer."""

import matplotlib.pyplot as plt

from .base import BaseDrawer
from ..helpers.grid_layout import GridLayout


class StaticGroupPlotDrawer(BaseDrawer):
    """Drawer for static plots with per-robot subplots in one figure.

    Each robot gets its own set of subplots (one per component),
    arranged in a grid within a single figure. Useful for comparing
    multiple robots side-by-side.
    """

    def draw(self, plot_list, save=False, path=None):
        self._check_plot_list(plot_list)

        fig = plt.figure(figsize=self.style.figsize)
        self._apply_style_to_fig(fig)

        axes_map = GridLayout(
            fig,
            plot_list,
            self.REGISTERED_COMPONENTS,
            expand=True,
            id_list=self.interpreter.id_list,
        ).allocate_axes()

        for item in axes_map:
            sub_interp = self.interpreter.for_robots(item["id_list"])
            component_class = self._check_class(item["class"])
            item["mode"] = 'group'
            component_class(
                interpreter=sub_interp,
                **item
            )
            self._apply_style_to_ax(item.get("ax"))

        if save or path:
            filename = self._save_figure(fig, plot_list, grouped=True, path=path)
            plt.close(fig)
            print(f'Plot saved to {filename}')

        return fig
