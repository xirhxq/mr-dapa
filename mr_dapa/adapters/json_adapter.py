"""JSON adapter for loading data in mr-dapa canonical format."""

import json


class JSONAdapter:
    """Adapter for loading JSON data files or lists.

    Accepts either a file path (str) pointing to a JSON file, or a
    pre-loaded list in canonical format. This is the default adapter
    if no adapter is specified.

    Example::
        adapter = JSONAdapter()
        data = adapter.load('data.json')
    """

    def load(self, source) -> list[dict]:
        """Load data from JSON file or list.

        Args:
            source: File path (str) or list in canonical format.

        Returns:
            List of dictionaries in canonical mr-dapa format.

        Raises:
            TypeError: If source is not a str or list.
        """
        if isinstance(source, str):
            with open(source) as f:
                return json.load(f)
        if isinstance(source, list):
            return source
        raise TypeError(f"JSONAdapter expects a file path or list, got {type(source)}")
