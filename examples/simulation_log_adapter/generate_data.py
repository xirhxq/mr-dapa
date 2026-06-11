"""Generate frame-based simulation log data for the adapter example."""

import json
import math
from pathlib import Path


def main():
    output = Path(__file__).with_name("data.json")
    frames = []
    searched = set()

    for step in range(80):
        runtime = step * 0.2
        robots = []
        updates = []

        for robot_id in [1, 2, 3]:
            phase = runtime + robot_id * 0.8
            x = math.cos(phase) * 3 + robot_id
            y = math.sin(phase) * 2
            vx = -math.sin(phase)
            vy = math.cos(phase)
            grid_cell = (min(19, max(0, int((x + 5) * 2))), min(19, max(0, int((y + 5) * 2))))
            if grid_cell not in searched:
                updates.append(list(grid_cell))
                searched.add(grid_cell)
            quality = max(0.45, 0.95 - 0.003 * step - 0.03 * robot_id)
            fail_safe = step > 60 and robot_id == 3

            robots.append({
                "id": robot_id,
                "state": {
                    "x": x,
                    "y": y,
                    "yawRad": math.atan2(vy, vx),
                    "battery": 4200 - runtime * (2 + robot_id * 0.2),
                },
                "opt": {
                    "result": {
                        "vx": vx,
                        "vy": vy,
                        "yawRateRad": 0.05 * math.sin(phase),
                    }
                },
                "cbfSlack": {
                    "coverageCBF": -0.1 * robot_id + 0.01 * step,
                },
                "cbfNoSlack": {
                    "distanceCBF": 1.0 + 0.1 * math.sin(phase),
                },
                "link_denial": {
                    "certified": not fail_safe,
                    "fail_safe": fail_safe,
                    "max_epsilon": 0.8 + 0.01 * step + 0.05 * robot_id,
                    "min_selected_quality": quality,
                },
            })

        frames.append({
            "runtime": runtime,
            "robots": robots,
            "update": updates,
            "link_denial": {
                "certified": all(robot["link_denial"]["certified"] for robot in robots),
                "fail_safe": any(robot["link_denial"]["fail_safe"] for robot in robots),
                "max_epsilon": max(robot["link_denial"]["max_epsilon"] for robot in robots),
                "min_selected_quality": min(
                    robot["link_denial"]["min_selected_quality"] for robot in robots
                ),
            },
        })

    data = {
        "config": {"num": 3},
        "para": {
            "gridWorld": {
                "xNum": 20,
                "yNum": 20,
                "xLim": [-5, 15],
                "yLim": [-5, 15],
            }
        },
        "state": frames,
    }

    output.write_text(json.dumps(data, indent=2))
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
