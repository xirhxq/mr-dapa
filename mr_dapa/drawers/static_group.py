from .base import *


class StaticGroupPlotDrawer(BaseDrawer):
    def draw(self, plot_list, save=False, path=None):
        self._check_plot_list(plot_list)

        fig = plt.figure(figsize=self.FIGSIZE)
        fig.set_tight_layout(True)

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
            component = component_class(
                interpreter=sub_interp,
                **item
            )

        if save or path:
            filename = self._save_figure(fig, plot_list, grouped=True, path=path)
            plt.close(fig)
            print(f'Plot saved to {filename}')

        return fig
