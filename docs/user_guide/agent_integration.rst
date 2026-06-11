Agent Integration Guide
=======================

This guide is written for coding agents that need to connect a user's
multi-agent algorithm or simulator to mr-dapa with minimal back-and-forth.

Integration Goal
----------------

The first working integration should produce at least one static figure from a
real run without changing the user's simulator. Prefer adapting data at the
boundary over asking the simulator to emit mr-dapa's canonical format on the
first pass.

Decision Tree
-------------

Use the canonical JSON format directly when the data is already shaped like
``[{id, timestamp, values}]``.

Use ``CSVAdapter`` when the data is a table with robot id, timestamp, and value
columns.

Use ``ParametricStudyAdapter`` when the data is an experiment summary shaped
like this:

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

Use ``SimulationLogAdapter`` when the data is a frame log shaped like this:

.. code-block:: json

   {
     "state": [
       {
         "runtime": 0.0,
         "robots": [
           {
             "id": 1,
             "state": {"x": 0.0, "y": 1.0, "battery": 4100.0},
             "opt": {"result": {"vx": 1.0, "vy": 0.0}},
             "cbfSlack": {"cvtCBF": -1.0},
             "cbfNoSlack": {"fixedCommCBF(base-0)": 2.0},
             "link_denial": {"certified": true, "min_selected_quality": 0.86}
           }
         ],
         "link_denial": {"certified": true, "fail_safe": false},
         "update": [[0, 0]]
       }
     ],
     "para": {"gridWorld": {"xNum": 10, "yNum": 10}}
   }

Minimum Plot Set
----------------

For a new algorithm, start with a small set of plots that proves the data path:

* trajectory map: ``MapComponent`` with ``x`` and ``y``
* core state lines: ``LinesComponent`` with ``battery`` or another scalar state
* command lines: ``LinesComponent`` with ``vx`` and ``vy`` when controls exist
* algorithm metrics: ``LinesComponent`` with CBF, loss, reward, or constraint
  aliases found in the adapted data
* coverage line: ``LinesComponent`` with ``search_coverage`` when grid updates
  exist
* first-search-time grid: ``SearchHeatmapComponent`` when ``search_cell_x``,
  ``search_cell_y``, and ``search_cell_time`` exist
* formation or link distance: ``PairDistanceComponent`` with explicit pairs or
  ``pairs: 'all'`` when ``x`` and ``y`` exist
* link-denial status: ``LinesComponent`` with ``link_denial_certified`` and
  ``link_denial_fail_safe`` when link-denial metrics exist
* link-denial quality: ``LinesComponent`` with
  ``link_denial_min_selected_quality`` or ``link_denial_max_epsilon``
* parameter sweep metrics: ``LinesComponent`` with ``final_coverage`` and
  ``duration`` when a ``summary.json`` file exists

Working Template
----------------

.. code-block:: python

   import mr_dapa as mrdp

   data_file = 'data.json'

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
           'title': 'Control Input',
           'class': 'LinesComponent',
           'keys': ['vx', 'vy'],
       },
       'coverage': {
           'title': 'Search Coverage',
           'class': 'LinesComponent',
           'keys': ['search_coverage'],
       },
       'search_heatmap': {
           'title': 'First Search Time',
           'class': 'SearchHeatmapComponent',
           'grid_shape': (100, 100),
           'limits': {'x': [-1500, 1500], 'y': [-1500, 1500]},
       },
       'pair_distance': {
           'title': 'Formation Distance',
           'class': 'PairDistanceComponent',
           'pairs': [(1, 2), (2, 3)],
           'min_distance': 10.0,
           'max_distance': 850.0,
       },
       'link_quality': {
           'title': 'Link Quality',
           'class': 'LinesComponent',
           'keys': ['link_denial_min_selected_quality'],
           'ylabel': 'Selected Link Quality',
           'show_zero_line': False,
           'show_legend': False,
       },
   }

   drawer = mrdp.StaticGlobalPlotDrawer(
       files=[data_file],
       components=components,
       adapter=mrdp.SimulationLogAdapter(),
   )

   drawer.set_style('paper').draw(
       ['map', 'search_heatmap', 'battery', 'control', 'coverage', 'pair_distance', 'link_quality'],
       save=True,
   )

Parameter Sweep Template
------------------------

.. code-block:: python

   import mr_dapa as mrdp

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

   mrdp.StaticGlobalPlotDrawer(
       files=['summary.json'],
       components=components,
       adapter=mrdp.ParametricStudyAdapter(),
   ).set_style('paper').draw(['coverage', 'duration'], save=True)

Inspecting Available Keys
-------------------------

When a plot key is unknown, load the data once and inspect aliases before
choosing components. ``inspect_data`` returns a compact summary, while
``suggest_components`` returns a starter ``components`` dictionary that can be
passed directly to a drawer.

.. code-block:: python

   import mr_dapa as mrdp

   data = mrdp.SimulationLogAdapter().load('data.json')
   summary = mrdp.inspect_data(data)
   components = mrdp.suggest_components(data)

   print(summary['robot_ids'])
   print(summary['time_range'])
   print(sorted(summary['aliases']))

   drawer = mrdp.StaticGlobalPlotDrawer(
       files=['data.json'],
       components=components,
       adapter=mrdp.SimulationLogAdapter(),
   )
   drawer.draw(list(components), save=True)

For summaries, replace the adapter and file name. The same helpers work on the
adapted canonical data:

.. code-block:: python

   data = mrdp.ParametricStudyAdapter().load('summary.json')
   components = mrdp.suggest_components(data)

Pride Versioning
----------------

From version ``1.0.0`` onward, mr-dapa uses the project's Pride versioning
convention for public releases. For AGENT work, treat a Pride release as a
coherent capability milestone: the code should be tested, documented, usable by
another agent without hidden context, and something the maintainers are
comfortable presenting publicly.

Use ``MAJOR.MINOR.PATCH`` numbers with these rules:

* bump ``MAJOR`` when the public API, canonical data format, drawer/component
  contracts, or adapter behavior changes in a way that downstream integrations
  must actively adjust to
* bump ``MINOR`` when adding compatible adapters, components, drawers, styles,
  examples, or AGENT helper APIs
* bump ``PATCH`` for compatible bug fixes, documentation corrections, packaging
  fixes, and small behavior repairs

Before recommending a release, verify the version in ``pyproject.toml`` and
``mr_dapa.__version__`` match, update ``CHANGELOG.md``, run the full test and
documentation checks, and keep local handoff or generated visual assets out of
the commit.

Validation Checklist
--------------------

Before presenting the integration as done, verify these points:

* the adapter loads the user's real data file without modifying that file
* at least one map or trajectory plot renders when ``x`` and ``y`` exist
* pair-distance plots use real robot IDs from the data, not assumed indices
* scalar plots use aliases printed from the adapted data, not guessed names
* generated figures are written outside source-controlled example data folders
* time filters and robot filters still work through drawer chain methods
* publication outputs use ``set_style('paper')`` and SVG/PDF when vector output
  is needed

When To Add A Custom Component
------------------------------

Add a custom component only when the desired plot cannot be represented as a
line, scatter, fill, map, density heatmap, or 3D map over adapted values. For
example, first-search-time grids, sensing footprints, and parameter sweep
summaries may deserve custom components because their geometry is not a simple
per-robot time series.
