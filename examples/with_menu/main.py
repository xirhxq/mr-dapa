"""Interactive menu example for exploring different visualizations.

This example demonstrates the new menu integration using basic-interactive-menu.

Install dependencies:
    pip install mr-dapa[menu]
"""

from mr_dapa import run_interactive_session

if __name__ == '__main__':
    run_interactive_session(
        data_folder="data",
        file_pattern="data_*.json"
    )
