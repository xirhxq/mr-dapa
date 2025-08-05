# Mr. Dapa - Multi-Robot Data Animation & Plot Assistance

A simple Python-based tool to assist with data animation and plotting for multi-robot simulation/experiment data.

## Overview

To be completed.

## Requirements

- **Python 3.6 or higher** (due to use of f-strings syntax)
- **numpy>=1.24.0**
- **matplotlib>=3.0.0**
- **ffmpeg**
- **tqdm**

## Installation

For development, we recommend installing the package in editable mode:

```bash
# Install the package in development mode
pip install -e .
```

To uninstall:

```bash
pip uninstall mr-dapa
 ```

This allows you to use standard Python imports in all project files.

## Further Development

If you want to develop this project, we recommend creating a separate environment with [conda](https://docs.conda.io/en/latest/) or [venv](https://docs.python.org/3/library/venv.html).

### Create a conda environment

```bash
conda create -n mr-dapa python=3.11
conda activate mr-dapa
pip install -r requirements.txt
pip install -e .
```

### Create a venv environment

```bash
python3 -m venv mr-dapa
source mr-dapa/bin/activate
pip install -r requirements.txt
pip install -e .
```

## License

MIT License - see the [LICENSE](LICENSE) file for details

## To-do List
 - Support for customisable plotting
 - Support for 3D plots