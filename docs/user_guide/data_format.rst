Data Format
============

Canonical Format
----------------

mr-dapa expects data in a specific JSON format. Each robot has its own
timestamp array, supporting async data (different robots, different sample rates).

.. code-block:: json

   [
     {
       "id": 1,
       "timestamp": [0.0, 0.02, 0.04],
       "values": [
         {
           "name": "X Position",
           "alias": "x",
           "unit": "m",
           "value": [1.0, 1.1, 1.2]
         },
         {
           "name": "Y Position",
           "alias": "y",
           "unit": "m",
           "value": [2.0, 2.1, 2.2]
         }
       ]
     }
   ]

Format Details
---------------

* ``id``: Unique robot identifier (integer)
* ``timestamp``: Array of timestamp values for this robot
* ``values``: List of value series
  * ``name``: Full name of the value
  * ``alias``: Short identifier used in components
  * ``unit``: Unit string (for axis labels)
  * ``value``: Array of values (same length as timestamp)

Using Adapters
---------------

If your data is in a different format, use one of the built-in adapters:

* :class:`~mr_dapa.JSONAdapter` - Load from JSON files (default)
* :class:`~mr_dapa.CSVAdapter` - Load from CSV files
* :class:`~mr_dapa.MultiFileAdapter` - Merge multiple JSON files
* :class:`~mr_dapa.NumPyAdapter` - Load from NumPy arrays

See :doc:`adapters` for more details.
