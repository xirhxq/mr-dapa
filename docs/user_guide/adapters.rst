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
