from typing import Protocol, runtime_checkable


@runtime_checkable
class DataAdapter(Protocol):
    def load(self, source) -> list[dict]:
        ...
