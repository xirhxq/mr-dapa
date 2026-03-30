from .base import *


class StaticSeparatePlotDrawer(BaseDrawer):
    def draw(self, plot_list, save=False, path=None):
        self._check_plot_list(plot_list)

        self.decide_sole_figsize(plot_list)

        figs = []

        for id in self.interpreter.id_list:
            fig = plt.figure(figsize=self.FIGSIZE)
            fig.set_tight_layout(True)

            sub_interp = self.interpreter.for_robots([id])

            axes_map = GridLayout(
                fig,
                plot_list,
                self.REGISTERED_COMPONENTS,
                expand=False,
                id_list=[id]
            ).allocate_axes()

            for item in axes_map:
                item_interp = sub_interp.for_robots(item["id_list"])
                component_class = self._check_class(item["class"])
                item["mode"] = 'separate'
                component = component_class(
                    interpreter=item_interp,
                    **item,
                )

            figs.append(fig)

        if save or path:
            filenames = []
            for idx, (fig, id) in enumerate(zip(figs, self.interpreter.id_list)):
                fig_path = path if path and len(figs) == 1 else None
                filenames.append(self._save_figure(fig, plot_list, id_list=[id], path=fig_path))
                plt.close(fig)
            if len(filenames) == 1:
                print(f'Plot saved to {filenames[0]}')
            else:
                print(f'Plots saved to {filenames}')

        return figs
