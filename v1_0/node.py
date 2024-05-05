from enum import Enum, auto
from typing import NamedTuple

from .color import Color


class Text(NamedTuple):
    text: str

    def to_json(self) -> dict:
        return {
            "type": "text",
            "text": self.text,
        }


class File(NamedTuple):
    file: str
    subpath: str | None = None  # must start with "#"

    def to_json(self) -> dict:
        out = {
            "type": "file",
            "file": self.file,
        }
        if self.subpath is not None:
            out["subpath"] = self.subpath
        return out


class Link(NamedTuple):
    link: str

    def to_json(self) -> dict:
        return {
            "type": "link",
            "link": self.link,
        }


class BackgroundStyle(Enum):
    COVER = auto()  # fills the entire width and height of the node
    RATIO = auto()  # maintains the aspect ratio of the background image
    REPEAT = auto()  # repeats the image as a pattern in both x/y directions


class Group(NamedTuple):
    label: str | None = None
    background: str | None = None
    background_style: BackgroundStyle | None = None

    def to_json(self) -> dict:
        out = {
            "type": "group",
        }
        if self.label is not None:
            out["label"] = self.label
        if self.background is not None:
            out["background"] = self.background
        if self.background_style is not None:
            out["backgroundStyle"] = self.background_style.name.lower()
        return out


NodeContent = Text | File | Link | Group


class Node(NamedTuple):
    id: str
    x: int
    y: int
    width: int
    height: int
    content: NodeContent
    color: Color | None = None

    @classmethod
    def from_corners(
            cls,
            id: str,
            corner1: tuple[int, int],
            corner2: tuple[int, int],
            content: NodeContent,
            color: Color | None = None,
    ) -> "Node":
        return cls(
            id,
            corner1[0],
            corner1[1],
            corner2[0] - corner1[0],
            corner2[1] - corner1[1],
            content,
            color,
        )

    def to_json(self) -> dict:
        out = {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            **self.content.to_json(),
        }
        if self.color is not None:
            out["color"] = self.color.key_phrase

        return out

    @classmethod
    def from_json(cls, node_json: dict) -> "Node":
        content_type = node_json["type"]
        if content_type == "text":
            content = Text(node_json["text"])
        elif content_type == "file":
            content = File(node_json["file"], node_json.get("subpath"))
        elif content_type == "link":
            content = Link(node_json["link"])
        elif content_type == "group":
            content = Group(
                node_json.get("label"),
                node_json.get("background"),
                BackgroundStyle[node_json.get("backgroundStyle").upper()],
            )
        else:
            raise ValueError(f"Unknown content type: {content_type}")

        return cls(
            node_json["id"],
            node_json["x"],
            node_json["y"],
            node_json["width"],
            node_json["height"],
            content,
            None if "color" not in node_json else Color(node_json["color"]),
        )
