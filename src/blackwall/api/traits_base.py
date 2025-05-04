from abc import ABC
from dataclasses import dataclass, fields
from typing import Any, Self


@dataclass
class TraitsBase(ABC):
    def to_traits(self, prefix: str) -> dict[str, Any]:
        traits = {}

        for field in fields(type(self)):
            value = getattr(self, field.name)
            field.metadata.get("masked", False)
            if value is not None:
                traits[f"{prefix}:{field.name}"] = value

        return traits

    @classmethod
    def from_dict(cls, prefix: str | None, source: dict[str, Any]) -> Self:
        kwargs = {}
        for field in fields(cls):
            key = field.name if prefix is None else f"{prefix}:{field.name}"
            value = source.get(key)
            if value is not None:
                kwargs[field.name] = value
        return cls(**kwargs)
    