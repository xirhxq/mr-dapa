from ..helpers.grid_layout import *
from ..helpers.loader import DataLoader
from ..helpers.utils import *
from ..helpers.base_interpreter import BaseInterpreter


class BaseDrawer:
    BAR_FORMAT = "{percentage:3.0f}%|{bar:50}| {n_fmt}/{total_fmt} [elap: {elapsed}s eta: {remaining}s]"
    DPI = 300
    FIGSIZE = (16, 9)
    REGISTERED_COMPONENTS = {}

    def __init__(self, files: list[str], components: json, interpreter=None):
        self.loader = DataLoader(files)
        self.data = self.loader.data
        self.folder = self.loader.folder

        self.REGISTERED_COMPONENTS.update(components)

        self.interpreter = BaseInterpreter(self.data) if interpreter is None else interpreter(self.data)

        plt.switch_backend('agg')

    def decide_sole_figsize(self, plot_list):
        if len(plot_list) > 1:
            return
        cls = self._check_class(self.REGISTERED_COMPONENTS[plot_list[0]]['class'])
        self.FIGSIZE = cls.FIGSIZE

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

    def _save_plot(self, fig, plot_list, id_list=None, grouped=False):
        filename = self._make_file(self._make_filename(plot_list, id_list))
        if grouped:
            filename += '-grouped'
        filename += '.png'
        fig.savefig(filename, dpi=self.DPI, bbox_inches='tight')
        return filename

    def _save_animation(self, ani, plot_list, id_list, time_ratio, fps):
        filename = self._make_file(self._make_filename(plot_list, id_list))
        fps_str = f'{fps:.1f}' if fps < 1 else f'{fps:.0f}'
        filename += f'-{time_ratio:.1g}x-{fps_str}fps.mp4'
        ani.save(filename, writer='ffmpeg', fps=fps, dpi=self.DPI)
        return filename

    def _make_filename(self, plot_list, id_list=None):
        filename = '-'.join([self.REGISTERED_COMPONENTS[plot_type]["filename"] if "filename" in self.REGISTERED_COMPONENTS[plot_type] else plot_type for plot_type in plot_list])
        return filename + self.interpreter.get_id_suffix(id_list=id_list)
