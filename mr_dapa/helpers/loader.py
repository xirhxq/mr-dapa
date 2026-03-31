"""Data loader for loading files with optional adapter."""

import os
from ..adapters import JSONAdapter


class DataLoader:
    """Loads data files using the specified or default adapter.

    Args:
        files: Single file path (str) or list of file paths.
        adapter: Optional DataAdapter instance. Defaults to JSONAdapter.

    Attributes:
        data: Loaded data in canonical format.
        file: First file path (for single file) or first file in list.
        folder: Directory containing the data files.
        datas: List of loaded data objects (for multi-file mode).
    """

    def __init__(self, files, adapter=None):
        self.files = files if isinstance(files, list) else [files]
        self.folders = [os.path.dirname(f) for f in self.files]
        self.file = self.files[0]
        self.folder = self.folders[0]
        self.adapter = adapter or JSONAdapter()

        if isinstance(self.adapter, JSONAdapter) and len(self.files) == 1:
            self.datas = [self.adapter.load(self.files[0])]
        elif isinstance(self.adapter, JSONAdapter):
            self.datas = [self.adapter.load(f) for f in self.files]
        else:
            self.datas = [self.adapter.load(self.files)]

        self.data = self.datas[0]
