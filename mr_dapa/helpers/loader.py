import os

from ..adapters import JSONAdapter


class DataLoader:
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
