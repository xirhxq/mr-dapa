from .base import *


class StaticGlobalPlotDrawer(BaseDrawer):
    def draw(self, plot_list):
        self._check_plot_list(plot_list)

        if len(plot_list) == 1:
            self.FIGSIZE = self.REGISTERED_COMPONENTS[plot_list[0]]["figsize"]

        fig = plt.figure(figsize=self.FIGSIZE)
        fig.set_tight_layout(True)

        axes_map = GridLayout(
            fig,
            plot_list,
            self.REGISTERED_COMPONENTS,
            expand=False,
            id_list=self.interpreter.id_list
        ).allocate_axes()

        for item in axes_map:
            component_class = self._check_class(item["class"])
            item["mode"] = 'global'
            component = component_class(
                data=self.data,
                interpreter=self.interpreter,
                **item
            )

        filename = self._save_plot(fig, plot_list)

        plt.close(fig)

        print(f'Plot saved to {filename}')
