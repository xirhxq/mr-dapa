"""Draw plots from a parametric study summary."""

from pathlib import Path

import mr_dapa as mrdp


def main():
    folder = Path(__file__).parent
    summary_file = folder / "summary.json"

    components = {
        "coverage": {
            "title": "Final Coverage",
            "class": "LinesComponent",
            "keys": ["final_coverage"],
            "xlabel": "Communication Range",
            "ylabel": "Final Coverage (%)",
            "show_zero_line": False,
        },
        "duration": {
            "title": "Completion Time",
            "class": "LinesComponent",
            "keys": ["duration"],
            "xlabel": "Communication Range",
            "ylabel": "Duration (s)",
            "show_zero_line": False,
        },
    }

    mrdp.StaticGlobalPlotDrawer(
        files=[str(summary_file)],
        components=components,
        adapter=mrdp.ParametricStudyAdapter(),
    ).set_style("paper").draw(["coverage", "duration"], save=True)


if __name__ == "__main__":
    main()
