from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class KnowledgeNode:
    """Represents a knowledge point in the graph."""

    node_id: str
    name: str
    difficulty: float = 0.5  # 0.0 (easy) -> 1.0 (hard)
    importance: float = 0.5  # 0.0 (low) -> 1.0 (high)
    estimated_time_hours: float = 1.0
    # Optional metadata hook for content/resource selection
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class KnowledgeEdge:
    """Represents a directed relation between knowledge nodes."""

    source_id: str
    target_id: str
    relation_type: str = "prerequisite"  # prerequisite | part_of | related
    weight: float = 1.0  # Baseline traversal/learning cost


@dataclass
class StudentProfile:
    """Represents a student's profile and mastery state."""

    mastery: Dict[str, float]  # node_id -> mastery in [0,1]
    learning_style: str = "neutral"  # visual | auditory | kinesthetic | neutral
    cognitive_level: str = "intermediate"  # novice | intermediate | advanced
    history: List[str] = field(default_factory=list)  # node_ids learned in order

    def mastered_nodes(self, threshold: float = 0.7) -> List[str]:
        return [node_id for node_id, level in self.mastery.items() if level >= threshold]

    def get_mastery(self, node_id: str) -> float:
        return float(self.mastery.get(node_id, 0.0))

    def update_mastery(self, node_id: str, delta: float) -> None:
        current = self.get_mastery(node_id)
        self.mastery[node_id] = max(0.0, min(1.0, current + delta))
        self.history.append(node_id)


@dataclass
class KnowledgeGraphData:
    """Serializable DTO for storing the knowledge graph."""

    nodes: List[KnowledgeNode]
    edges: List[KnowledgeEdge]


Path = List[str]
PathWithScore = Tuple[Path, float]

