Drawers
=======

Drawers determine how to arrange components and generate figures.

Drawer Types
------------

StaticGlobalPlotDrawer
~~~~~~~~~~~~~~~~~~~~~~~

All robots are plotted in shared subplots. Each component type gets one
subplot, and all robots' data is overlaid.

.. code-block:: python

   from mr_dapa import StaticGlobalPlotDrawer

   drawer = StaticGlobalPlotDrawer(files=['data.json'], components=components)
   fig = drawer.draw(['x', 'map'], save=True)

*Use case*: Comparing robot behavior on the same scale*

StaticSeparatePlotDrawer
~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a separate figure for each robot, with all components displayed
in that figure.

.. code-block:: python

   from mr_dapa import StaticSeparatePlotDrawer

   drawer = StaticSeparatePlotDrawer(files=['data.json'], components=components)
   figs = drawer.draw(['x', 'map'], save=True)

*Use case*: Individual robot analysis, separate files per robot*

StaticGroupPlotDrawer
~~~~~~~~~~~~~~~~~~~~~

Each robot gets its own set of subplots (one per component), arranged
in a grid within a single figure.

.. code-block:: python

   from mr_dapa import StaticGroupPlotDrawer

   drawer = StaticGroupPlotDrawer(files=['data.json'], components=components)
   fig = drawer.draw(['x', 'map'], save=True)

*Use case*: Side-by-side comparison of multiple robots*

AnimationDrawer
~~~~~~~~~~~~~~~~

Generates MP4 animations showing data evolution over time.

.. code-block:: python

   from mr_dapa import AnimationDrawer

   drawer = AnimationDrawer(files=['data.json'], components=components)
   drawer.draw(['map'], time_ratio=2, fps=30, save=True)

*Use case*: Visualizing time evolution, creating presentation videos*
