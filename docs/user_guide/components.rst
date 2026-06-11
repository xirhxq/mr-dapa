Components
==========

Components define what type of visualization to render. Each component
is rendered on a matplotlib Axes.

Built-in Components
-------------------

LinesComponent
~~~~~~~~~~~~~~~

Time-series line plots for tracking values over time.

.. code-block:: python

   'x': {
       'title': 'X Position',
       'class': 'LinesComponent',
       'keys': ['x'],
       'xlabel': 'Time (s)',
       'ylabel': 'X Position (m)',
       'fill': True,           # Fill between line and zero
       'bounds': [-1, 0, 1],   # Horizontal reference lines
       'show_zero_line': True, # y=0 reference line
       'show_legend': True     # Set False for dense diagnostic plots
   }

MapComponent
~~~~~~~~~~~~

2D position map with trajectory trails and robot ID annotations.

.. code-block:: python

   'map': {
       'title': 'Trajectory',
       'class': 'MapComponent',
       'limits': {'x': [-10, 10], 'y': [-10, 10]},  # Axis limits
       'trail_style': {'alpha': 0.3},                  # Trail appearance
       'marker_style': {'markersize': 8}                # Marker size
   }

ScatterComponent
~~~~~~~~~~~~~~~~

Scatter/phase plots showing relationships between two values.

.. code-block:: python

   'phase': {
       'title': 'Phase Plot',
       'class': 'ScatterComponent',
       'x_key': 'x',
       'y_key': 'y'
   }

FillComponent
~~~~~~~~~~~~~

Filled area plots for showing uncertainty ranges or value spans.

.. code-block:: python

   'range': {
       'title': 'Value Range',
       'class': 'FillComponent',
       'keys': ['x', 'y']
   }

SearchHeatmapComponent
~~~~~~~~~~~~~~~~~~~~~~

First-search-time grids from event series such as ``search_cell_x``,
``search_cell_y``, and ``search_cell_time``. ``SimulationLogAdapter`` creates
these series when frame logs contain grid ``update`` cells.

.. code-block:: python

   'search_heatmap': {
       'title': 'First Search Time',
       'class': 'SearchHeatmapComponent',
       'grid_shape': (100, 100),
       'limits': {'x': [-1500, 1500], 'y': [-1500, 1500]}
   }

PairDistanceComponent
~~~~~~~~~~~~~~~~~~~~~

Inter-robot distance plots for formation, safety, and communication-range
diagnostics. It reads ``x`` and ``y`` from canonical robot series, supports
asynchronous robot timestamps through interpolation, and can show reference
distance bounds.

.. code-block:: python

   'pair_distance': {
       'title': 'Formation Distance',
       'class': 'PairDistanceComponent',
       'pairs': [(1, 2), (2, 3)],
       'min_distance': 10.0,
       'max_distance': 850.0,
       'show_uncertainty': True
   }

Use ``pairs: 'all'`` for a quick diagnostic over every robot pair in the
filtered interpreter view.

Custom Components
-----------------

To create your own component, subclass :class:`~mr_dapa.BaseComponent`
and implement the ``_initialize()`` method.

See :doc:`custom_components` for a complete guide.
