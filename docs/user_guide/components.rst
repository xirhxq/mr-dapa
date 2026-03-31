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
       'fill': True,           # Fill between line and zero
       'bounds': [-1, 0, 1],   # Horizontal reference lines
       'show_zero_line': True  # y=0 reference line
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
~~~~~~~~~~~

Filled area plots for showing uncertainty ranges or value spans.

.. code-block:: python

   'range': {
       'title': 'Value Range',
       'class': 'FillComponent',
       'keys': ['x', 'y']
   }

Custom Components
-----------------

To create your own component, subclass :class:`~mr_dapa.BaseComponent`
and implement the ``_initialize()`` method.

See :doc:`custom_components` for a complete guide.
