import json
import os


class DataLoader:
    def __init__(self, files):
        self.files = files
        self.folders = [os.path.dirname(f) for f in files]
        self.file = files[0]
        self.folder = self.folders[0]
        self.datas = [self._load(f) for f in files]
        self.data = self.datas[0]

    @staticmethod
    def _load(path):
        with open(path) as f:
            return json.load(f)
