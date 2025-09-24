from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from learning_path_planner.data.models import StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph
from learning_path_planner.personalization.adapter import PersonalizationAdapter
from learning_path_planner.planners.graph_planner import GraphPlanner, PlannerConfig
from learning_path_planner.rules.engine import RulesEngine, RulesConfig


@dataclass
class HybridConfig:
    graph: PlannerConfig = field(default_factory=PlannerConfig)
    rules: RulesConfig = field(default_factory=RulesConfig)
    # For future extensions, include rl weights, etc.


class HybridPlanner:
    """Combines graph planner with rules and personalization adjustments."""

    def __init__(self, graph: KnowledgeGraph, profile: StudentProfile, cfg: HybridConfig | None = None) -> None:
        self.graph = graph
        self.profile = profile
        self.cfg = cfg or HybridConfig()
        self.personalizer = PersonalizationAdapter(graph, profile)
        self.graph_planner = GraphPlanner(graph, profile, self.cfg.graph)
        self.rules_engine = RulesEngine(graph, profile, self.cfg.rules)

    def plan(self, goal_node_id: str) -> Dict[str, object]:
        best, alternatives = self.graph_planner.plan(goal_node_id)
        base_path, base_score = best

        adjusted_path, warnings = self.rules_engine.apply(base_path)

        # Personalization-aware estimate summary
        total_time = 0.0
        avg_difficulty = 0.0
        for node_id in adjusted_path:
            node = self.graph.get_node(node_id)
            total_time += self.personalizer.adjusted_estimated_time(node)
            avg_difficulty += self.personalizer.adjusted_difficulty(node)
        if adjusted_path:
            avg_difficulty /= float(len(adjusted_path))

        return {
            "goal": goal_node_id,
            "path": adjusted_path,
            "base_score": base_score,
            "alternatives": alternatives,
            "personalized_summary": {
                "estimated_total_time_hours": round(total_time, 2),
                "average_adjusted_difficulty": round(avg_difficulty, 3) if adjusted_path else 0.0,
            },
            "warnings": warnings,
        }

