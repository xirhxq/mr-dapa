class BaseComponent:
    FIGSIZE = (6, 6)
    expand = True

    def __init__(self, ax, interpreter, title="", mode='static', **kwargs):
        self.ax = ax
        self.interpreter = interpreter
        self.title = title
        self.mode = mode
        self.kwargs = kwargs

    def _initialize(self):
        raise NotImplementedError

    def update(self, timestamp):
        return []
