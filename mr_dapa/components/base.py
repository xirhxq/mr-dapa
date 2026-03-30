class BaseComponent:
    FIGSIZE = (6, 6)
    expand = True
    required_config_keys: dict[str, type] = {}

    def __init__(self, ax, interpreter, title="", mode='static', **kwargs):
        self.ax = ax
        self.interpreter = interpreter
        self.title = title
        self.mode = mode
        self.kwargs = kwargs

    @classmethod
    def validate_config(cls, name: str, config: dict) -> None:
        for key, expected_type in cls.required_config_keys.items():
            if key not in config:
                raise ValueError(
                    f"Component '{name}' ({cls.__name__}): missing required key '{key}'"
                )
            if expected_type is not None and not isinstance(config[key], expected_type):
                raise ValueError(
                    f"Component '{name}' ({cls.__name__}): key '{key}' must be "
                    f"{expected_type.__name__}, got {type(config[key]).__name__}"
                )

    def _initialize(self):
        raise NotImplementedError

    def update(self, timestamp):
        return []
