from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from learning_path_planner.data.models import StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph
from learning_path_planner.personalization.adapter import PersonalizationAdapter


@dataclass
class RLEnvConfig:
    mastery_increment: float = 0.2
    time_penalty_weight: float = 0.1
    completion_reward: float = 1.0
    mastered_threshold: float = 0.7


class LearningEnv:
    """Simple RL environment for learning path: select next node to study."""

    def __init__(self, graph: KnowledgeGraph, profile: StudentProfile, goal_node_id: str, cfg: RLEnvConfig | None = None) -> None:
        self.graph = graph
        self.initial_profile = profile
        self.goal = goal_node_id
        self.cfg = cfg or RLEnvConfig()
        self.personalizer = PersonalizationAdapter(graph, profile)
        self._reset_state()

    def _reset_state(self) -> None:
        # Copy mutable parts of the profile
        self.mastery: Dict[str, float] = dict(self.initial_profile.mastery)
        self.trajectory: List[str] = []

    def reset(self) -> Tuple[Dict[str, float], Dict[str, object]]:
        self._reset_state()
        return dict(self.mastery), {"done": self._is_done()}

    def _is_done(self) -> bool:
        return self.mastery.get(self.goal, 0.0) >= self.cfg.mastered_threshold

    def step(self, action_node_id: str) -> Tuple[Dict[str, float], float, bool, Dict[str, object]]:
        # Invalid action: no change and negative reward
        if action_node_id not in self.graph._nodes:
            return dict(self.mastery), -0.5, self._is_done(), {"invalid": True}

        node = self.graph.get_node(action_node_id)
        # Prerequisite check; if not satisfied, small penalty
        prereqs = set(self.graph.prerequisites_of(action_node_id))
        mastered_set = {k for k, v in self.mastery.items() if v >= self.cfg.mastered_threshold}
        if not prereqs.issubset(mastered_set):
            return dict(self.mastery), -0.2, self._is_done(), {"blocked": True}

        # Apply learning increment and compute reward
        before = self.mastery.get(action_node_id, 0.0)
        after = min(1.0, before + self.cfg.mastery_increment)
        self.mastery[action_node_id] = after
        self.trajectory.append(action_node_id)

        mastery_gain = after - before
        time_cost = self.personalizer.adjusted_estimated_time(node)
        reward = mastery_gain * 1.0 - self.cfg.time_penalty_weight * time_cost

        done = self._is_done()
        if done:
            reward += self.cfg.completion_reward

        return dict(self.mastery), reward, done, {}

