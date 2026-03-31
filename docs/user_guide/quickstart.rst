Quick Start Guide
=================

Installation
------------

Install from PyPI:

.. code-block:: bash

   pip install mr-dapa

Or install from source:

.. code-block:: bash

   git clone https://github.com/xirhxq/mr-dapa.git
   cd mr-dapa
   pip install -e .

Basic Usage
-----------

.. code-block:: python

   import mr_dapa as mrdp

   components = {
       'x': {'title': 'X Position', 'class': 'LinesComponent', 'keys': ['x']},
       'map': {'title': 'Trajectory', 'class': 'MapComponent'},
   }

   drawer = mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
   fig = drawer.draw(['x', 'map'], save=True)

Chain API for Filtering
-----------------------

.. code-block:: python

   # Filter by robot IDs
   drawer.set_id_list([1, 2]).draw(['x'])

   # Filter by time range
   drawer.set_time_range((1.0, 3.0)).draw(['x'])

   # First N seconds
   drawer.set_first_seconds(2.0).draw(['x'])

   # Combine filters
   (mrdp.StaticGlobalPlotDrawer(files=['data.json'], components=components)
       .set_id_list([1])
       .set_time_range((1.0, 3.0))
       .draw(['x', 'map']))

Animation
---------

.. code-block:: python

   drawer = mrdp.AnimationDrawer(files=['data.json'], components=components)
   drawer.draw(['map'], time_ratio=2, save=True)

Next Steps
----------

* Learn about the :doc:`data_format`
* Explore available :doc:`components`
* Try different :doc:`drawers`
