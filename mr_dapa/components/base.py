"""Base component class for all visualization components.

This module defines BaseComponent, the abstract base class that all
mr-dapa visualization components must inherit from. Components are
responsible for rendering a specific type of visualization on a given
matplotlib axis.
"""

class BaseComponent:
    """Base class for all visualization components.

    Components render visualizations on a matplotlib Axes using data
    from a BaseInterpreter. Each component type (Lines, Map, Scatter, etc.)
    inherits from this class and implements _initialize() and optionally
    update().

    Attributes:
        FIGSIZE: Default figure size (width, height) in inches.
        expand: Whether this component should be expanded by robot in
            GridLayout. True for most components, False for global views.
        required_config_keys: Dict mapping config key names to expected types.
            Validated at drawer initialization time.

    Args:
        ax: Matplotlib Axes to render on.
        interpreter: BaseInterpreter instance containing filtered data.
        title: Title for the plot.
        mode: 'static' or 'animation'. Animation mode enables update() method.
        **kwargs: Additional component-specific configuration.
    """

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
        """Validate component configuration against required keys.

        Checks that all keys in required_config_keys are present in config
        and have the correct type. Raises ValueError if validation fails.

        Args:
            name: Component name (for error messages).
            config: Configuration dictionary to validate.

        Raises:
            ValueError: If a required key is missing or has wrong type.
        """
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
        """Initialize the visualization component.

        Subclasses must implement this method to set up the initial
        state of the visualization (create lines, markers, etc.).
        Called during __init__.
        """
        raise NotImplementedError

    def update(self, timestamp):
        """Update visualization for animation at given timestamp.

        Args:
            timestamp: Time value to update visualization to.

        Returns:
            List of matplotlib artists that were modified. Used for
            blitting optimization in animations. Empty list if no artists
            were updated or component doesn't support animation.
        """
        return []
