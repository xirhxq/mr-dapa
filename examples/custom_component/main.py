import numpy as np
import matplotlib.pyplot as plt

import mr_dapa as mrdp
from mr_dapa import BaseComponent, register_component


class BarComponent(BaseComponent):
    FIGSIZE = (8, 5)
    expand = False

    required_config_keys = {'keys': list}

    def __init__(self, ax, interpreter, title="", keys=None, mode='static', **kwargs):
        super().__init__(ax, interpreter, title=title, mode=mode, **kwargs)
        self.keys = keys or []
        self.bar_width = kwargs.get('bar_width', 0.15)
        self._initialize()

    def _initialize(self):
        self.ax.set_title(self.title)

        robot_ids = self.interpreter.id_list
        n_robots = len(robot_ids)
        x = np.arange(len(self.keys))

        for i, robot in enumerate(self.interpreter.data):
            values = []
            for key in self.keys:
                for v in robot["values"]:
                    if v["alias"] == key or v["name"] == key:
                        values.append(v["value"][-1])
                        break
            offset = (i - n_robots / 2 + 0.5) * self.bar_width
            self.ax.bar(x + offset, values, self.bar_width, label=f'Robot #{robot["id"]}')

        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.keys)
        self.ax.set_ylabel("Final Value")
        if n_robots > 1:
            self.ax.legend(loc='best')

    def update(self, timestamp):
        return []


register_component('BarComponent', BarComponent)


def main():
    from examples.minimal.generate_data import data

    components = {
        'final-bars': {
            'title': 'Final Values Comparison',
            'class': 'BarComponent',
            'keys': ['x', 'y', 'batt'],
        },
        'x': {
            'title': 'X Position',
            'class': 'LinesComponent',
            'keys': ['x'],
        },
    }

    fig = mrdp.StaticGlobalPlotDrawer(files=['examples/minimal/data.json'], components=components) \
        .draw(['final-bars', 'x'], save=True)

    print('Custom component example completed.')


if __name__ == '__main__':
    main()
