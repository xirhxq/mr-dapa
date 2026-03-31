import numpy as np
import tqdm
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from .base import BaseDrawer
from ..helpers.grid_layout import GridLayout


class AnimationDrawer(BaseDrawer):

    def draw(self, plot_list, time_ratio=1, fps=50, save=False, path=None):
        self._check_plot_list(plot_list)
        self.decide_sole_figsize(plot_list)

        fps = min(self.interpreter.get_fps(), fps)

        fig = plt.figure(figsize=self.style.figsize)
        self._apply_style_to_fig(fig)

        axes_map = GridLayout(
            fig,
            plot_list,
            self.REGISTERED_COMPONENTS,
            id_list=self.interpreter.id_list
        ).allocate_axes()

        components = []

        for item in axes_map:
            sub_interp = self.interpreter.for_robots(item["id_list"])
            component_class = self._check_class(item["class"])
            components.append(
                component_class(
                    interpreter=sub_interp,
                    mode='animation',
                    **item
                )
            )
            self._apply_style_to_ax(item.get("ax"))

        interval = 1 / fps * time_ratio
        interval_ms = int(interval * 1000)
        total_length = int((self.interpreter.time_range[1] - self.interpreter.time_range[0]) / interval) + 1

        timestamps = np.linspace(self.interpreter.time_range[0], self.interpreter.time_range[1], total_length)

        pbar = tqdm.tqdm(total=total_length, bar_format=self.BAR_FORMAT)

        can_blit = self._check_blit_support(components, timestamps)

        if can_blit and not (save or path):
            def _update_frame(num):
                pbar.update(1)
                artists = []
                for comp in components:
                    result = comp.update(timestamps[num])
                    if result:
                        artists.extend(result)
                return artists

            ani = animation.FuncAnimation(
                fig, _update_frame,
                frames=total_length,
                interval=interval_ms,
                blit=True
            )
        else:
            def _update_frame(num):
                pbar.update(1)
                for comp in components:
                    comp.update(timestamps[num])

            ani = animation.FuncAnimation(
                fig, _update_frame,
                frames=total_length,
                interval=interval_ms,
                blit=False
            )

        if save or path:
            filename = self._save_animation(
                ani, plot_list,
                id_list=self.interpreter.id_list,
                time_ratio=time_ratio, fps=fps,
                path=path
            )
            print(f"Animation saved to {filename}")
            pbar.close()

        return fig

    def _check_blit_support(self, components, timestamps):
        try:
            artists = []
            for comp in components:
                result = comp.update(timestamps[0])
                if result:
                    artists.extend(result)
            return len(artists) > 0
        except (TypeError, AttributeError):
            return False
