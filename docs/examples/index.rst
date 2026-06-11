Examples
========

The mr-dapa package includes several examples demonstrating different features.

.. toctree::
   :maxdepth: 2

   minimal
   csv_adapter
   numpy_adapter
   simulation_log_adapter
   parametric_study_adapter
   multi_file
   all_components
   all_draw_modes
   publication_style
   chain_api
   custom_component
   with_menu

Example Overview
----------------

**minimal** - Basic usage with JSON data and core components.

**csv_adapter** - Loading data from CSV files.

**numpy_adapter** - Loading data from NumPy arrays.

**simulation_log_adapter** - Loading frame-based multi-robot simulator logs.

**parametric_study_adapter** - Plotting metrics from parameter sweep summaries.

**multi_file** - Merging data from multiple JSON files.

**all_components** - Demonstrating all four component types.

**all_draw_modes** - Using all four drawer types.

**publication_style** - Style customization for publications.

**chain_api** - Filter and configuration patterns.

**custom_component** - Creating and registering custom components.

**with_menu** - Interactive CLI menu for visualization exploration.

Running Examples
-----------------

Each example directory contains:

* ``generate_data.py`` - Generate sample data
* ``main.py`` - Run the example
* ``README.md`` - Description

To run an example:

.. code-block:: bash

   cd examples/minimal
   python generate_data.py
   python main.py
