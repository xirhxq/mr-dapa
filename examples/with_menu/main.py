"""Interactive menu example for exploring different visualizations.

This example provides an interactive CLI menu for generating various
types of plots and animations.
"""

import os
import glob
from mr_dapa.drawers.drawers import *

# Default components configuration
components = {
    'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
    'y': {'title': 'Y Position', 'class': 'LinesComponent', 'keys': ['y']},
    'map': {'title': 'Map', 'class': 'MapComponent'},
}

def find_files(folder: str, ptn: str, max_num: int = 1):
    """Find files matching a pattern."""
    if not os.path.exists(folder):
        print(f"Data directory '{folder}' not found.")
        print(f"Please run generate_data.py in the {folder}/ directory first.")
        return []

    files = glob.glob(os.path.join(folder, ptn))
    if not files:
        print(f"No files found matching pattern '{ptn}' in {folder}/")
        return []

    print(f"Found {len(files)} file(s): {sorted(files)}")
    max_num = min(max_num, len(files))
    return sorted(files)[:max_num]

def interactive_menu(options):
    """Display interactive menu and execute selected actions."""
    while True:
        print("\n" + "-" * 40)
        print("MR-DAPA Visualization Menu")
        print("-" * 40)
        for idx, option in enumerate(options):
            print(f"[{idx}]: {option['name']}")
        print("[q]: Quit")
        print("[a]: Run All")
        choice = input("\nChoose an option: ").strip().lower()

        if choice == 'q':
            print("Exiting...")
            break
        elif choice == 'a':
            print("\nRunning all options...\n")
            for option in options:
                print(f"Running: {option['name']}...")
                try:
                    option['action']()
                    print("  -> Done")
                except Exception as e:
                    print(f"  -> Error: {e}")
            print("\nAll tasks completed.")
            break
        elif choice.isdigit() and 0 <= int(choice) < len(options):
            selected = options[int(choice)]
            print(f"\nRunning: {selected['name']}...")
            try:
                selected['action']()
                print("  -> Done")
            except Exception as e:
                print(f"  -> Error: {e}")
        else:
            print("Invalid input. Please try again.")

def interactive_selection(options):
    """Interactive selection from a list of options."""
    print("Select options:")
    for idx, option in enumerate(options):
        print(f"[{idx}]: {option}")
    choice = input("Choose options (comma-separated): ").strip()
    if not choice.isdigit():
        return options
    selected_indices = [int(c) for c in choice.split(',')]
    return [options[i] for i in selected_indices if i < len(options)]

def main_with_interactive_menu():
    """Main function with interactive menu."""
    # Find data files
    files = find_files('data', 'data_*.json', 10)
    if not files:
        print("\nNo data files found. Please run data/generate_data.py first.")
        return

    # Let user select which files to use
    selected_files = interactive_selection(files)
    print(f"\nUsing {len(selected_files)} file(s)")

    # Menu options with updated API
    menu_options = [
        {
            'name': 'X Position, All Robots (Global)',
            'action': lambda: StaticGlobalPlotDrawer(selected_files, components).draw(['x'])
        },
        {
            'name': 'X & Y Positions, All Robots (Global)',
            'action': lambda: StaticGlobalPlotDrawer(selected_files, components).draw(['x', 'y'])
        },
        {
            'name': 'Map, All Robots (Global)',
            'action': lambda: StaticGlobalPlotDrawer(selected_files, components).draw(['map'])
        },
        {
            'name': 'X Position, Per Robot (Separate)',
            'action': lambda: StaticSeparatePlotDrawer(selected_files, components).draw(['x'])
        },
        {
            'name': 'X & Y & Map, Per Robot (Separate)',
            'action': lambda: StaticSeparatePlotDrawer(selected_files, components).draw(['x', 'y', 'map'])
        },
        {
            'name': 'X Position, Per Robot (Group)',
            'action': lambda: StaticGroupPlotDrawer(selected_files, components).draw(['x'])
        },
        {
            'name': 'X & Y & Map, Per Robot (Group)',
            'action': lambda: StaticGroupPlotDrawer(selected_files, components).draw(['x', 'y', 'map'])
        },
        {
            'name': 'Animation - Map',
            'action': lambda: AnimationDrawer(selected_files, components).draw(['map'], save=True)
        },
        {
            'name': 'Animation - X & Y & Map',
            'action': lambda: AnimationDrawer(selected_files, components).draw(['x', 'y', 'map'], save=True)
        },
    ]

    interactive_menu(menu_options)

if __name__ == '__main__':
    main_with_interactive_menu()
