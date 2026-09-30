"""Data model for a single todo item."""

from dataclasses import asdict, dataclass


@dataclass
class Todo:
    """A todo item with a unique id, text, and completion flag."""

    id: int
    text: str
    done: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        return cls(
            id=int(data["id"]),
            text=str(data["text"]),
            done=bool(data.get("done", False)),
        )
