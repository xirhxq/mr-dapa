"""Component registry for dynamic component registration."""

from typing import Type, Dict


_COMPONENT_REGISTRY: Dict[str, Type] = {}
"""Global registry of component classes."""


def register_component(name: str, cls: Type) -> None:
    """Register a component class.

    Args:
        name: Name to register the component under.
        cls: Component class (must inherit from BaseComponent).
    """

from difflib import get_close_matches
from typing import Type

_COMPONENT_REGISTRY: dict[str, Type] = {}


def register_component(name: str, cls: Type) -> None:
    if not isinstance(name, str) or not name:
        raise ValueError(f"Component name must be a non-empty string, got {name!r}")
    if not isinstance(cls, type):
        raise TypeError(f"Component must be a class, got {type(cls).__name__}")
    from .components.base import BaseComponent
    if not issubclass(cls, BaseComponent):
        raise TypeError(f"Component must be a BaseComponent subclass, got {cls.__name__}")
    _COMPONENT_REGISTRY[name] = cls


def unregister_component(name: str) -> None:
    if name not in _COMPONENT_REGISTRY:
        raise KeyError(f"Component '{name}' is not registered")
    del _COMPONENT_REGISTRY[name]


def get_component_class(name: str) -> Type:
    if name in _COMPONENT_REGISTRY:
        return _COMPONENT_REGISTRY[name]
    suggestions = get_close_matches(name, _COMPONENT_REGISTRY.keys(), n=3, cutoff=0.6)
    msg = f"Component '{name}' is not registered."
    if suggestions:
        msg += f" Did you mean: {', '.join(suggestions)}?"
    msg += f" Available: {list(_COMPONENT_REGISTRY.keys())}"
    raise KeyError(msg)


def list_components() -> dict[str, Type]:
    return dict(_COMPONENT_REGISTRY)


def _register_builtins() -> None:
    from .components.lines import LinesComponent
    from .components.map import MapComponent
    from .components.scatter import ScatterComponent
    from .components.fill import FillComponent

    for cls in [LinesComponent, MapComponent, ScatterComponent, FillComponent]:
        register_component(cls.__name__, cls)


_register_builtins()
