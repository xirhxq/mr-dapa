from ..helpers.grid_layout import *
from ..helpers.loader import DataLoader
from ..helpers.utils import *
from ..helpers.base_interpreter import BaseInterpreter


class BaseDrawer:
    BAR_FORMAT = "{percentage:3.0f}%|{bar:50}| {n_fmt}/{total_fmt} [elap: {elapsed}s eta: {remaining}s]"
    DPI = 300
    FIGSIZE = (16, 9)
    REGISTERED_COMPONENTS = {}

    def __init__(self, files, interpreter=None):
        self.loader = DataLoader(files)
        self.data = self.loader.data
        self.folder = self.loader.folder

        self.interpreter = BaseInterpreter(self.data) if interpreter is None else interpreter(self.data)

        plt.switch_backend('agg')

    def register_components(self, components):
        self.REGISTERED_COMPONENTS.update(components)
        return self

    def set_id_list(self, id_list):
        self.interpreter.set_id_list(id_list)
        return self

    def set_first_seconds(self, first_seconds):
        self.interpreter.set_first_seconds(first_seconds)
        return self

    def set_last_seconds(self, last_seconds):
        self.interpreter.set_last_seconds(last_seconds)
        return self

    def set_time_range(self, time_range):
        self.interpreter.set_time_range(time_range)
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
        if class_name not in globals():
            raise ValueError(f"Component class '{class_name}' not found. ")
        return globals()[class_name]

    def _make_file(self, plot_name):
        filename = self.loader.file.split('/')[-1].split('.')[0]
        folder = os.path.join(self.folder, filename + '-plots')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder, plot_name)

    def _save_plot(self, fig, plot_name):
        filename = self._make_file(plot_name) + '.png'
        fig.savefig(filename, dpi=self.DPI, bbox_inches='tight')
        print(f"Plot saved to {filename}")

    def _save_animation(self, ani, plot_name, fps):
        filename = self._make_file(plot_name) + '.mp4'
        ani.save(filename, writer='ffmpeg', fps=fps, dpi=self.DPI)
        print(f"Animation saved to {filename}")

    def _make_filename(self, plot_list, id_list=None, grouped=False):
        filename = '-'.join([self.REGISTERED_COMPONENTS[plot_type]["filename"] for plot_type in plot_list])
        if grouped:
            filename += '-grouped'
        return filename + self.interpreter.get_filename_suffix(id_list=id_list)
