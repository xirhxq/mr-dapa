from .base import *


class StaticSeparatePlotDrawer(BaseDrawer):
    def draw(self, plot_list):
        self._check_plot_list(plot_list)

        pbar = tqdm.tqdm(total=len(self.interpreter.id_list), bar_format=self.BAR_FORMAT)

        if len(plot_list) == 1:
            self.FIGSIZE = self.REGISTERED_COMPONENTS[plot_list[0]]["figsize"]

        filenames = []

        for id in self.interpreter.id_list:
            fig = plt.figure(figsize=self.FIGSIZE)
            fig.set_tight_layout(True)

            axes_map = GridLayout(
                fig,
                plot_list,
                self.REGISTERED_COMPONENTS,
                expand=False,
                id_list=[id]
            ).allocate_axes()

            for item in axes_map:
                self.interpreter.set_id_list(item["id_list"])
                component_class = self._check_class(item["class"])
                item["mode"] = 'separate'
                component = component_class(
                    data=self.data,
                    interpreter=self.interpreter,
                    **item,
                )

            filenames.append(self._save_plot(fig, plot_list, id_list=[id]))

            plt.close(fig)
            pbar.update(1)

        pbar.close()

        print(f'Plots saved to {filenames}')
