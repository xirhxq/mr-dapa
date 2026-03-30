import json


class JSONAdapter:
    def load(self, source) -> list[dict]:
        if isinstance(source, str):
            with open(source) as f:
                return json.load(f)
        if isinstance(source, list):
            return source
        raise TypeError(f"JSONAdapter expects a file path or list, got {type(source)}")
