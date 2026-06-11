Simulation Log Adapter Example
==============================

Location
--------

``examples/simulation_log_adapter/``

Run
---

.. code-block:: bash

   python examples/simulation_log_adapter/generate_data.py
   python examples/simulation_log_adapter/main.py

This example draws trajectory, first-search-time heatmap, battery, control
input, search coverage, formation distance, and link-denial status plots from
a frame-based multi-robot simulation log using ``SimulationLogAdapter``.
