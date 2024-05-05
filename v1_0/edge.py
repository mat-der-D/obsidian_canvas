from enum import Enum, auto
from typing import NamedTuple

from .color import Color
from .node import Node


class Side(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()


class EndType(Enum):
    NONE = auto()
    ARROW = auto()


class EndInfo(NamedTuple):
    node: Node
    side: Side
    end: EndType | None = None


class Edge(NamedTuple):
    id: str
    from_info: EndInfo
    to_info: EndInfo
    color: Color | None = None
    label: str | None = None

    def to_json(self) -> dict:
        out = {
            "id": self.id,
            "fromNode": self.from_info.node.id,
            "toNode": self.to_info.node.id,
        }
        for end_info, prefix in [(self.from_info, "from"), (self.to_info, "to")]:
            if end_info.side is not None:
                out[f"{prefix}Side"] = end_info.side.name.lower()
            if end_info.end is not None:
                out[f"{prefix}End"] = end_info.end.name.lower()

        if self.color is not None:
            out["color"] = self.color.key_phrase
        if self.label is not None:
            out["label"] = self.label
        return out

    @classmethod
    def from_json(cls, json_data: dict, node_dict: dict[str, Node]) -> "Edge":
        from_info = EndInfo(
            node=node_dict[json_data["fromNode"]],
            side=Side[json_data["fromSide"].upper()] if "fromSide" in json_data else None,
            end=EndType[json_data["fromEnd"].upper()] if "fromEnd" in json_data else None,
        )
        to_info = EndInfo(
            node=node_dict[json_data["toNode"]],
            side=Side[json_data["toSide"].upper()] if "toSide" in json_data else None,
            end=EndType[json_data["toEnd"].upper()] if "toEnd" in json_data else None,
        )
        color = Color(json_data["color"]) if "color" in json_data else None
        label = json_data.get("label")
        return cls(json_data["id"], from_info, to_info, color, label)
