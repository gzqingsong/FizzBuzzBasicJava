from __future__ import annotations

import json
from dataclasses import asdict
from typing import Dict, Iterable, List, Optional, Set, Tuple

from learning_path_planner.data.models import (
    KnowledgeEdge,
    KnowledgeGraphData,
    KnowledgeNode,
)


class KnowledgeGraph:
    """In-memory knowledge graph representation with convenience methods."""

    def __init__(self) -> None:
        self._nodes: Dict[str, KnowledgeNode] = {}
        self._out_edges: Dict[str, List[KnowledgeEdge]] = {}
        self._in_edges: Dict[str, List[KnowledgeEdge]] = {}

    # --- Node/edge management ---
    def add_node(self, node: KnowledgeNode) -> None:
        self._nodes[node.node_id] = node
        self._out_edges.setdefault(node.node_id, [])
        self._in_edges.setdefault(node.node_id, [])

    def add_edge(self, edge: KnowledgeEdge) -> None:
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise ValueError("Both source and target must exist before adding an edge")
        self._out_edges.setdefault(edge.source_id, []).append(edge)
        self._in_edges.setdefault(edge.target_id, []).append(edge)

    def get_node(self, node_id: str) -> KnowledgeNode:
        return self._nodes[node_id]

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def neighbors(self, node_id: str) -> List[str]:
        return [edge.target_id for edge in self._out_edges.get(node_id, [])]

    def predecessors(self, node_id: str) -> List[str]:
        return [edge.source_id for edge in self._in_edges.get(node_id, [])]

    def prerequisites_of(self, node_id: str) -> List[str]:
        return [e.source_id for e in self._in_edges.get(node_id, []) if e.relation_type == "prerequisite"]

    # --- Validation ---
    def prerequisites_satisfied(self, node_id: str, mastered: Set[str]) -> bool:
        required = set(self.prerequisites_of(node_id))
        return required.issubset(mastered)

    # --- Serialization ---
    def to_data(self) -> KnowledgeGraphData:
        nodes = list(self._nodes.values())
        edges: List[KnowledgeEdge] = []
        for source_id, out_edges in self._out_edges.items():
            edges.extend(out_edges)
        return KnowledgeGraphData(nodes=nodes, edges=edges)

    def to_json(self, path: str) -> None:
        data = self.to_data()
        json_obj = {
            "nodes": [asdict(n) for n in data.nodes],
            "edges": [asdict(e) for e in data.edges],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(path: str) -> "KnowledgeGraph":
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        graph = KnowledgeGraph()
        for n in payload.get("nodes", []):
            graph.add_node(KnowledgeNode(**n))
        for e in payload.get("edges", []):
            graph.add_edge(KnowledgeEdge(**e))
        return graph

    # --- Utility ---
    def all_nodes(self) -> List[str]:
        return list(self._nodes.keys())

    def __len__(self) -> int:
        return len(self._nodes)

