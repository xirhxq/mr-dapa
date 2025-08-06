from .base import *


class AnimationDrawer(BaseDrawer):

    def draw(self, plot_list, time_ratio=1, fps=50):
        self._check_plot_list(plot_list)

        fps = min(self.interpreter.get_fps(), fps)

        fig = plt.figure(figsize=self.FIGSIZE)
        fig.set_tight_layout(True)

        axes_map = GridLayout(
            fig,
            plot_list,
            self.REGISTERED_COMPONENTS,
            id_list=self.interpreter.id_list
        ).allocate_axes()

        original_id_list = self.interpreter.id_list

        components = []

        for item in axes_map:
            self.interpreter.set_id_list(item["id_list"])
            component_class = self._check_class(item["class"])
            components.append(
                component_class(
                    data=self.data,
                    interpreter=self.interpreter,
                    mode='animation',
                    **item
                )
            )

        interval = 1 / fps * time_ratio
        interval_ms = int(interval * 1000)
        total_length = int((self.interpreter.time_range[1] - self.interpreter.time_range[0]) / interval) + 1

        timestamps = np.linspace(self.interpreter.time_range[0], self.interpreter.time_range[1], total_length)

        pbar = tqdm.tqdm(total=total_length, bar_format=self.BAR_FORMAT)

        def update(num):
            pbar.update(1)
            for comp in components:
                comp.update(timestamps[num])

        ani = animation.FuncAnimation(
            fig, update,
            frames=total_length,
            interval=interval_ms,
            blit=False
        )

        self.interpreter.set_id_list(original_id_list)

        filename = self._save_animation(ani, plot_list, id_list=self.interpreter.id_list, time_ratio=time_ratio, fps=fps)

        print(f"Animation with {time_ratio:.1g}x speed & {fps:.1g} fps saved to {filename}")

        pbar.close()
