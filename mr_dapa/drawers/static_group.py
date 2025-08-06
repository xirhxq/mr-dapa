from .base import *


class StaticGroupPlotDrawer(BaseDrawer):
    def draw(self, plot_list):
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

        original_id_list = self.interpreter.id_list

        for item in axes_map:
            self.interpreter.set_id_list(item["id_list"])
            component_class = self._check_class(item["class"])
            item["mode"] = 'group'
            component = component_class(
                data=self.data,
                interpreter=self.interpreter,
                **item
            )

        self.interpreter.set_id_list(original_id_list)

        filename = self._save_plot(fig, plot_list, grouped=True)

        plt.close(fig)

        print(f'Plot saved to {filename}')
