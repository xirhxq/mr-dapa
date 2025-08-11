# Mr. Dapa - Multi-Robot Data Animation & Plot Assistance

A simple Python-based tool to assist with data animation and plotting for multi-robot simulation/experiment data.

## File Structure
The project follows a standard Python package structure:

```
mr-dapa/
 ├── mr_dapa/ # Core source code 
 ├── examples/ # Example scripts and data 
 │ └── minimal/ # Minimal usage example 
 │   ├── main.py # Main script for minimal example 
 │   └── data.json/ # Sample data file
 └── README.md # Project documentation
```

## Overview

Mr. Dapa is a powerful visualization tool designed to help researchers and engineers working with multi-robot systems to easily create static plots and animations from their experimental or simulation data. It provides a fluent API for generating various types of visualizations with minimal code.

The library supports multiple visualization modes:
- Static global plots (data from all robots in single or multiple subplots)
- Static separate plots (individual plots per robot)
- Static group plots (grouped data visualization)
- Animated visualizations (time-based animations)

For further details, we strongly recommend the users to try with the [minimal example](examples/minimal/main.py).

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

## Usage Example

For basic usage patterns, see the [minimal example](examples/minimal/main.py) that demonstrates:
- Data visualization configuration through component registration
- Fluent API for plot customization (time ranges, robot IDs, display parameters)
- Various plot types including static plots and animations

The visualization configuration is defined in `examples/minimal/main.py` through component registration and method chaining.

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
 - Toggle trace showing in 2D map
 - Heatmap component
 - Example with data transforming from other  formats
 - 3D map