from typing import Iterable
from .color import Color
from .node import Node
from .edge import Edge


class Canvas:
    def __init__(self, nodes: Iterable[Node] = (), edges: Iterable[Edge] = ()):
        self._nodes = tuple(nodes)
        self._edges = tuple(edges)

    @property
    def nodes(self) -> tuple[Node]:
        return self._nodes

    @property
    def edges(self) -> tuple[Edge]:
        return self._edges

    def to_json(self) -> dict:
        out = {}
        if self._nodes:
            out["nodes"] = [node.to_json() for node in self._nodes]
        if self._edges:
            out["edges"] = [edge.to_json() for edge in self._edges]
        return out

    @classmethod
    def from_json(cls, json_data: dict) -> "Canvas":
        node_dict = {node_data["id"]: Node.from_json(node_data) for node_data in json_data.get("nodes", [])}
        nodes = list(node_dict.values())
        edges = [Edge.from_json(edge_data, node_dict) for edge_data in json_data.get("edges", [])]
        return cls(nodes, edges)
