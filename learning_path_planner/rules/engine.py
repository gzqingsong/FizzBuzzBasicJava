from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Tuple

from learning_path_planner.data.models import StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph


@dataclass
class RulesConfig:
    skip_mastered: bool = True
    high_difficulty_threshold: float = 0.75
    max_consecutive_high_difficulty: int = 2


class RulesEngine:
    """Applies rule-based post-processing to a proposed learning path."""

    def __init__(self, graph: KnowledgeGraph, profile: StudentProfile, cfg: RulesConfig | None = None) -> None:
        self.graph = graph
        self.profile = profile
        self.cfg = cfg or RulesConfig()

    def apply(self, path: List[str]) -> Tuple[List[str], List[str]]:
        warnings: List[str] = []
        adjusted = list(path)

        # Insert missing prerequisites
        adjusted = self._ensure_prerequisites(adjusted, warnings)

        # Drop mastered nodes if configured
        if self.cfg.skip_mastered:
            threshold = 0.7
            adjusted = [n for n in adjusted if self.profile.get_mastery(n) < threshold]

        # Cognitive load balancing check
        adjusted = self._balance_cognitive_load(adjusted, warnings)

        return adjusted, warnings

    def _ensure_prerequisites(self, path: List[str], warnings: List[str]) -> List[str]:
        mastered: Set[str] = set(self.profile.mastered_nodes())
        result: List[str] = []
        seen: Set[str] = set()
        for node_id in path:
            # ensure all prereqs placed before node
            prereqs = self.graph.prerequisites_of(node_id)
            for p in prereqs:
                if p not in mastered and p not in seen and p not in result:
                    result.append(p)
                    seen.add(p)
                    warnings.append(f"Inserted missing prerequisite {p} for {node_id}")
            result.append(node_id)
            seen.add(node_id)
        return result

    def _balance_cognitive_load(self, path: List[str], warnings: List[str]) -> List[str]:
        count_high = 0
        for idx, node_id in enumerate(path):
            if self.graph.get_node(node_id).difficulty >= self.cfg.high_difficulty_threshold:
                count_high += 1
                if count_high > self.cfg.max_consecutive_high_difficulty:
                    warnings.append(
                        "Cognitive load warning: too many high-difficulty topics in a row"
                    )
                    # For simplicity, just warn; advanced implementation could insert a lower-difficulty related node
                    count_high = 0
            else:
                count_high = 0
        return path

