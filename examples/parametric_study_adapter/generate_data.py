"""Generate a sample parametric study summary."""

import json
from pathlib import Path


def main():
    folder = Path(__file__).parent
    summary_file = folder / "summary.json"

    summary = {
        "parametric_study": {
            "parameter_name": "cbfs.without-slack.comm-fixed.max-range",
            "parameter_values": [650.0, 850.0, 1050.0],
            "num_runs": 3,
            "timestamp": "2026-01-29_17-32-03",
            "results": [
                {
                    "parameter_value": 650.0,
                    "duration": 349.5,
                    "final_coverage": 68.56,
                    "data_folder": "2026-01-29_17-31-07",
                },
                {
                    "parameter_value": 850.0,
                    "duration": 289.0,
                    "final_coverage": 100.0,
                    "data_folder": "2026-01-29_17-31-26",
                },
                {
                    "parameter_value": 1050.0,
                    "duration": 300.0,
                    "final_coverage": 100.0,
                    "data_folder": "2026-01-29_17-31-45",
                },
            ],
        }
    }

    summary_file.write_text(json.dumps(summary, indent=2))
    print(f"Wrote {summary_file}")


if __name__ == "__main__":
    main()
