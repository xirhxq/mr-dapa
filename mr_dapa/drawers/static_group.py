from .base import *


class StaticGroupPlotDrawer(BaseDrawer):
    def draw(self,
             plot_list,
             first_seconds=None, last_seconds=None, time_range=None,
             id_list=None
             ):
        self._check_plot_list(plot_list)
        fig = plt.figure(figsize=self.FIGSIZE)
        fig.set_tight_layout(True)

        axes_map = GridLayout(fig, plot_list, id_list=range(self.data["config"]["num"])).allocate_axes()

        components = []

        for item in axes_map:
            component_class = self._check_class(item["class"])
            item["mode"] = 'group'
            components.append(
                component_class(
                    data=self.data,
                    **item
                )
            )

        suffix = '-'.join([REGISTRIED_COMPONENTS[plot_type]["filename"] for plot_type in plot_list])
        filename = os.path.join(self.folder, suffix + '-all.png')
        fig.savefig(filename, dpi=self.DPI, bbox_inches='tight')
        plt.close(fig)
        print(f"Plot saved to {filename}")
