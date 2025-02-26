from abc import ABC
from dataclasses import dataclass, fields
from typing import Any

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