"""Static global plot drawer."""

import matplotlib.pyplot as plt

from .base import BaseDrawer
from ..helpers.grid_layout import GridLayout


class StaticGlobalPlotDrawer(BaseDrawer):
    """Drawer for static plots with all robots in shared subplots.

    Each component type gets one subplot, and all robots' data is
    overlaid on that subplot. Useful for comparing robot behavior.
    """

    def draw(self, plot_list, save=False, path=None):
        self._check_plot_list(plot_list)
        self.decide_sole_figsize(plot_list)

        fig = plt.figure(figsize=self.style.figsize)
        self._apply_style_to_fig(fig)

        axes_map = GridLayout(
            fig,
            plot_list,
            self.REGISTERED_COMPONENTS,
            expand=False,
            id_list=self.interpreter.id_list
        ).allocate_axes()

        for item in axes_map:
            sub_interp = self.interpreter.for_robots(item["id_list"])
            component_class = self._check_class(item["class"])
            item["mode"] = 'global'
            component_class(
                interpreter=sub_interp,
                **item
            )
            self._apply_style_to_ax(item.get("ax"))

        if save or path:
            filename = self._save_figure(fig, plot_list, path=path)
            plt.close(fig)
            print(f'Plot saved to {filename}')

        return fig
