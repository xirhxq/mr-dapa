"""Interactive menu helpers for mr-dapa visualizations.

This module provides convenience functions for building interactive
menus using basic-interactive-menu, specifically designed for
selecting visualization options.

Requires: pip install mr-dapa[menu]
"""

from typing import Dict, Optional
from pathlib import Path

try:
    from basic_interactive_menu import InteractiveMenu
except ImportError:
    raise ImportError(
        "basic-interactive-menu is required for menu functionality. "
        "Install it with: pip install mr-dapa[menu]"
    )


def get_drawer_class(viz_type: str) -> tuple:
    """Get drawer class from visualization type string.

    Args:
        viz_type: Visualization type description.

    Returns:
        Tuple of (drawer_class, plot_list).

    Raises:
        ValueError: If viz_type is not recognized.
    """
    from .drawers.drawers import (
        StaticGlobalPlotDrawer,
        StaticSeparatePlotDrawer,
        StaticGroupPlotDrawer,
        AnimationDrawer,
    )

    mapping = {
        "X Position (Global)": (StaticGlobalPlotDrawer, ["x"]),
        "X & Y Positions (Global)": (StaticGlobalPlotDrawer, ["x", "y"]),
        "Map (Global)": (StaticGlobalPlotDrawer, ["map"]),
        "X Position (Separate)": (StaticSeparatePlotDrawer, ["x"]),
        "X & Y & Map (Separate)": (StaticSeparatePlotDrawer, ["x", "y", "map"]),
        "X Position (Group)": (StaticGroupPlotDrawer, ["x"]),
        "X & Y & Map (Group)": (StaticGroupPlotDrawer, ["x", "y", "map"]),
        "Animation - Map": (AnimationDrawer, ["map"]),
        "Animation - X & Y & Map": (AnimationDrawer, ["x", "y", "map"]),
    }

    if viz_type not in mapping:
        raise ValueError(f"Unknown visualization type: {viz_type}")

    return mapping[viz_type]


def run_interactive_session(
    data_folder: str = "data",
    file_pattern: str = "data_*.json",
    components: Optional[Dict[str, Dict]] = None,
) -> None:
    """Run a complete interactive visualization session.

    This function provides a quick way to start an interactive session
    for selecting data files and visualization types.

    Args:
        data_folder: Path to folder containing data files.
        file_pattern: Glob pattern for matching data files.
        components: Component configuration dict. Uses default if None.

    Example::
        run_interactive_session(
            data_folder="my_data",
            file_pattern="*.json"
        )
    """
    import glob
    import os

    if components is None:
        components = {
            'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
            'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
            'map': {'title': 'Map', 'class': 'MapComponent'},
        }

    if not os.path.exists(data_folder):
        print(f"Data directory '{data_folder}' not found.")
        return

    files = sorted(glob.glob(os.path.join(data_folder, file_pattern)))
    if not files:
        print(f"No files found matching '{file_pattern}' in {data_folder}/")
        return

    print(f"Found {len(files)} file(s): {[Path(f).name for f in files]}")

    while True:
        menu = (
            InteractiveMenu(multiple_allowed=True)
            .set_title("Select Data File(s)")
            .add_options([Path(f).name for f in files])
            .ask("Select Data File(s)", "files")
        )

        result = menu.get_all_results()

        if result is None or isinstance(result, InteractiveMenu):
            print("Cancelled.")
            return

        selected_names = result.get("files", [])
        selected_files = [f for f in files if Path(f).name in selected_names]

        viz_menu = (
            InteractiveMenu()
            .set_title("Select Visualization")
            .add_option("X Position (Global)")
            .add_option("X & Y Positions (Global)")
            .add_option("Map (Global)")
            .add_option("X Position (Separate)")
            .add_option("X & Y & Map (Separate)")
            .add_option("X Position (Group)")
            .add_option("X & Y & Map (Group)")
            .add_option("Animation - Map")
            .add_option("Animation - X & Y & Map")
            .ask("Visualization Type", "viz_type")
        )

        viz_result = viz_menu.get_all_results()

        if viz_result is None or isinstance(viz_result, InteractiveMenu):
            continue

        viz_type = viz_result.get("viz_type")
        if viz_type:
            drawer_class, plot_list = get_drawer_class(viz_type)
            drawer = drawer_class(selected_files, components)

            save = "Animation" in viz_type
            drawer.draw(plot_list, save=save)
            print(f"Generated: {viz_type}")

        again = input("\nGenerate another visualization? (y/n): ").strip().lower()
        if again != 'y':
            break
