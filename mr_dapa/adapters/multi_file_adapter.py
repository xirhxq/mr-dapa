"""Multi-file adapter for merging data from multiple files."""

import json


class MultiFileAdapter:
    """Adapter for loading and merging multiple JSON files.

    Each file should contain data for one or more robots. Files are
    merged into a single canonical dataset.

    Example::
        adapter = MultiFileAdapter()
        data = adapter.load(['robot1.json', 'robot2.json'])
    """

    def load(self, source) -> list[dict]:
        """Load and merge data from multiple JSON files.

        Args:
            source: List of file paths.

        Returns:
            Merged list of dictionaries in canonical format.
        """
        if isinstance(source, list) and len(source) > 0 and isinstance(source[0], str):
            merged = []
            for path in source:
                with open(path) as f:
                    data = json.load(f)
                if isinstance(data, list):
                    merged.extend(data)
                else:
                    merged.append(data)
            return merged
        raise TypeError(f"MultiFileAdapter expects a list of file paths, got {type(source)}")
