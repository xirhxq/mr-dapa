"""Data adapter protocol for mr-dapa.

This module defines the DataAdapter protocol that all data adapters must implement.
Adapters are responsible for loading data from various sources and converting them
to the canonical mr-dapa format.

Typical usage example::
    from mr_dapa import CSVAdapter

    adapter = CSVAdapter(id_col='robot_id', timestamp_col='time')
    data = adapter.load('data.csv')
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class DataAdapter(Protocol):
    """Protocol for data adapters that load and convert data to canonical format.

    Data adapters take data from various sources (JSON files, CSV files,
    NumPy arrays, etc.) and convert them to the mr-dapa canonical format:
    a list of dictionaries, each representing a robot with id, timestamp,
    and values.

    Implementations must provide a load() method that accepts a source
    and returns a list[dict] in canonical format.
    """

    def load(self, source) -> list[dict]:
        """Load data from source and convert to canonical format.

        Args:
            source: Data source (file path, file object, array, etc.)

        Returns:
            List of dictionaries in canonical mr-dapa format.
        """
        ...
