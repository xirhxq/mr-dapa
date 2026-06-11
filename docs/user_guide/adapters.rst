Adapters
========

Adapters load data from various sources and convert them to the canonical
mr-dapa format.

Built-in Adapters
-----------------

JSONAdapter (default)
~~~~~~~~~~~~~~~~~~~~~

Loads data from JSON files or pre-loaded lists. This is the default adapter
if no adapter is specified.

.. code-block:: python

   from mr_dapa import JSONAdapter

   adapter = JSONAdapter()
   data = adapter.load('data.json')

CSVAdapter
~~~~~~~~~~

Loads data from CSV files. Configure column names for robot ID and timestamp.

.. code-block:: python

   from mr_dapa import CSVAdapter

   adapter = CSVAdapter(id_col='robot_id', timestamp_col='time')
   data = adapter.load('data.csv')

MultiFileAdapter
~~~~~~~~~~~~~~~~

Merges multiple JSON files into a single dataset. Useful when each file
contains data for one robot.

.. code-block:: python

   from mr_dapa import MultiFileAdapter

   adapter = MultiFileAdapter()
   data = adapter.load(['robot1.json', 'robot2.json'])

NumPyAdapter
~~~~~~~~~~~~~

Converts NumPy arrays to canonical format. Useful for in-memory data
processing pipelines.

.. code-block:: python

   from mr_dapa import NumPyAdapter
   import numpy as np

   data_dict = {
       1: {
           'timestamps': np.array([0, 1, 2]),
           'values': {'x': np.array([1, 2, 3])}
       }
   }

   adapter = NumPyAdapter()
   data = adapter.load(data_dict)

SimulationLogAdapter
~~~~~~~~~~~~~~~~~~~~

Loads frame-based multi-robot simulation logs. This is useful when a simulator
writes one JSON object with ``state[*].runtime`` and ``state[*].robots[*]``
rather than one canonical series per robot.

The adapter extracts numeric values from common simulation fields:

* ``robot.state`` values such as ``x``, ``y``, ``yawRad``, and ``battery``
* ``robot.opt.result`` values such as ``vx`` and ``vy``
* ``robot.cbfSlack`` and ``robot.cbfNoSlack`` metric dictionaries
* ``robot.position_covariance`` and ``robot.uncertainty`` when present
* ``robot.link_denial`` values such as ``link_denial_certified``,
  ``link_denial_fail_safe``, ``link_denial_max_epsilon``, and
  ``link_denial_min_selected_quality``
* global ``search_coverage`` and ``searched_cells`` when ``para.gridWorld`` and
  frame ``update`` cells are present
* global ``frame.link_denial`` values using the same ``link_denial_*`` aliases

Boolean link-denial values are encoded as ``1.0`` for true and ``0.0`` for
false so they can be plotted directly with ``LinesComponent``.

.. code-block:: python

   from mr_dapa import SimulationLogAdapter, StaticGlobalPlotDrawer

   components = {
       'map': {
           'title': 'Trajectory',
           'class': 'MapComponent',
           'limits': {'x': [-1500, 1500], 'y': [-1500, 1500]},
       },
       'battery': {
           'title': 'Battery',
           'class': 'LinesComponent',
           'keys': ['battery'],
       },
       'control': {
           'title': 'Control Inputs',
           'class': 'LinesComponent',
           'keys': ['vx', 'vy'],
       },
       'coverage': {
           'title': 'Search Coverage',
           'class': 'LinesComponent',
           'keys': ['search_coverage'],
       },
       'link_quality': {
           'title': 'Link Quality',
           'class': 'LinesComponent',
           'keys': ['link_denial_min_selected_quality'],
           'show_legend': False,
       },
   }

   StaticGlobalPlotDrawer(
       files=['data.json'],
       components=components,
       adapter=SimulationLogAdapter(),
   ).draw(['map', 'battery', 'control', 'coverage', 'link_quality'], save=True)

ParametricStudyAdapter
~~~~~~~~~~~~~~~~~~~~~~

Loads parameter sweep summaries with a top-level ``parametric_study`` object.
This is useful for plotting experiment-level metrics such as final coverage or
duration across parameter values.

Expected summary shape:

.. code-block:: json

   {
     "parametric_study": {
       "parameter_name": "cbfs.without-slack.comm-fixed.max-range",
       "parameter_values": [650.0, 850.0, 1050.0],
       "results": [
         {"parameter_value": 650.0, "duration": 349.5, "final_coverage": 68.56},
         {"parameter_value": 850.0, "duration": 289.0, "final_coverage": 100.0}
       ]
     }
   }

The adapter maps ``parameter_value`` to the canonical ``timestamp`` axis and
creates values for numeric result fields. Use ``xlabel`` and ``ylabel`` in
``LinesComponent`` configs when the x-axis represents a parameter rather than
time.

.. code-block:: python

   from mr_dapa import ParametricStudyAdapter, StaticGlobalPlotDrawer

   components = {
       'coverage': {
           'title': 'Final Coverage',
           'class': 'LinesComponent',
           'keys': ['final_coverage'],
           'xlabel': 'Communication Range',
           'ylabel': 'Final Coverage (%)',
           'show_zero_line': False,
       },
       'duration': {
           'title': 'Completion Time',
           'class': 'LinesComponent',
           'keys': ['duration'],
           'xlabel': 'Communication Range',
           'ylabel': 'Duration (s)',
           'show_zero_line': False,
       },
   }

   StaticGlobalPlotDrawer(
       files=['summary.json'],
       components=components,
       adapter=ParametricStudyAdapter(),
   ).set_style('paper').draw(['coverage', 'duration'], save=True)

Using Adapters with Drawers
-----------------------------

Pass the adapter to the drawer constructor:

.. code-block:: python

   from mr_dapa import StaticGlobalPlotDrawer, CSVAdapter

   drawer = StaticGlobalPlotDrawer(
       files=['data.csv'],
       components=components,
       adapter=CSVAdapter(id_col='robot_id')
   )
