from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from learning_path_planner.graph.knowledge_graph import KnowledgeGraph
from learning_path_planner.data.models import KnowledgeNode, StudentProfile


@dataclass
class PersonalizationConfig:
    style_time_multipliers: Dict[str, float] = None  # e.g., {"visual": 0.95}
    cognitive_difficulty_multipliers: Dict[str, float] = None  # e.g., {"novice": 0.9}

    def __post_init__(self) -> None:
        if self.style_time_multipliers is None:
            self.style_time_multipliers = {
                "visual": 0.95,
                "auditory": 1.0,
                "kinesthetic": 1.05,
                "neutral": 1.0,
            }
        if self.cognitive_difficulty_multipliers is None:
            self.cognitive_difficulty_multipliers = {
                "novice": 0.9,
                "intermediate": 1.0,
                "advanced": 1.1,
            }


class PersonalizationAdapter:
    def __init__(self, graph: KnowledgeGraph, profile: StudentProfile, cfg: PersonalizationConfig | None = None) -> None:
        self.graph = graph
        self.profile = profile
        self.cfg = cfg or PersonalizationConfig()

    def adjusted_estimated_time(self, node: KnowledgeNode) -> float:
        base = float(node.estimated_time_hours)
        style_mult = float(self.cfg.style_time_multipliers.get(self.profile.learning_style, 1.0))
        return base * style_mult

    def adjusted_difficulty(self, node: KnowledgeNode) -> float:
        base = float(node.difficulty)
        cog_mult = float(self.cfg.cognitive_difficulty_multipliers.get(self.profile.cognitive_level, 1.0))
        return max(0.0, min(1.0, base * cog_mult))

