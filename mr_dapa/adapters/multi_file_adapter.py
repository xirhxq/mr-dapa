import json


class MultiFileAdapter:
    def load(self, source) -> list[dict]:
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
