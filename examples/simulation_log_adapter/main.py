"""Draw basic plots from a frame-based simulation log."""

from pathlib import Path

import mr_dapa as mrdp


def main():
    folder = Path(__file__).parent
    data_file = folder / "data.json"

    components = {
        "map": {
            "title": "Trajectory",
            "class": "MapComponent",
            "limits": {"x": [-5, 8], "y": [-4, 4]},
        },
        "battery": {
            "title": "Battery",
            "class": "LinesComponent",
            "keys": ["battery"],
        },
        "control": {
            "title": "Control Input",
            "class": "LinesComponent",
            "keys": ["vx", "vy"],
        },
        "coverage": {
            "title": "Search Coverage",
            "class": "LinesComponent",
            "keys": ["search_coverage"],
            "show_zero_line": False,
        },
        "search_heatmap": {
            "title": "First Search Time",
            "class": "SearchHeatmapComponent",
            "grid_shape": (20, 20),
            "limits": {"x": [-5, 15], "y": [-5, 15]},
        },
        "pair_distance": {
            "title": "Formation Distance",
            "class": "PairDistanceComponent",
            "pairs": [(1, 2), (2, 3)],
            "min_distance": 0.5,
            "max_distance": 7.0,
        },
        "link_quality": {
            "title": "Link Quality",
            "class": "LinesComponent",
            "keys": ["link_denial_min_selected_quality"],
            "ylabel": "Selected Link Quality",
            "show_zero_line": False,
            "show_legend": False,
        },
        "link_status": {
            "title": "Link Status",
            "class": "LinesComponent",
            "keys": ["link_denial_certified", "link_denial_fail_safe"],
            "ylabel": "Status",
            "show_zero_line": False,
            "show_legend": False,
        },
    }

    drawer = mrdp.StaticGlobalPlotDrawer(
        files=[str(data_file)],
        components=components,
        adapter=mrdp.SimulationLogAdapter(),
    )
    drawer.set_style("paper").draw(["map", "search_heatmap", "battery", "control", "coverage"], save=True)
    drawer.draw(["pair_distance", "link_quality", "link_status"], save=True)


if __name__ == "__main__":
    main()
