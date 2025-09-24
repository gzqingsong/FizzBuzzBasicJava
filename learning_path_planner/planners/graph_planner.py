from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from learning_path_planner.data.models import Path, PathWithScore, StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph


@dataclass
class PlannerConfig:
    # Scoring weights (higher score is better)
    weight_importance: float = 1.0
    weight_time_cost: float = 1.0
    weight_difficulty_cost: float = 0.5
    weight_mastery_gap_cost: float = 1.0

    # Algorithmic options
    mastered_threshold: float = 0.7
    algorithm: str = "dijkstra"  # dijkstra | astar
    top_k_paths: int = 1


def _heuristic(node_id: str, goal_id: str, graph: KnowledgeGraph) -> float:
    # Simple admissible heuristic: zero (reduces to Dijkstra) to keep correctness.
    # Can be extended to estimate remaining study time.
    return 0.0


def _prerequisites_satisfied_for_candidate(
    candidate_node_id: str,
    mastered: Set[str],
    current_path_nodes: Set[str],
    graph: KnowledgeGraph,
) -> bool:
    prereqs = set(graph.prerequisites_of(candidate_node_id))
    return prereqs.issubset(mastered.union(current_path_nodes))


def _path_score(path: Path, graph: KnowledgeGraph, profile: StudentProfile, cfg: PlannerConfig) -> float:
    score = 0.0
    for node_id in path:
        node = graph.get_node(node_id)
        mastery_gap = 1.0 - profile.get_mastery(node_id)
        benefit = cfg.weight_importance * float(node.importance)
        cost_time = cfg.weight_time_cost * float(node.estimated_time_hours)
        cost_diff = cfg.weight_difficulty_cost * float(node.difficulty)
        cost_gap = cfg.weight_mastery_gap_cost * float(mastery_gap)
        score += benefit - (cost_time + cost_diff + cost_gap)
    return score


class GraphPlanner:
    """Graph-based learning path planner with Dijkstra/A* and path scoring."""

    def __init__(self, graph: KnowledgeGraph, profile: StudentProfile, cfg: Optional[PlannerConfig] = None) -> None:
        self.graph = graph
        self.profile = profile
        self.cfg = cfg or PlannerConfig()

    def plan(self, goal_node_id: str) -> Tuple[PathWithScore, List[PathWithScore]]:
        mastered = set(self.profile.mastered_nodes(self.cfg.mastered_threshold))
        if goal_node_id in mastered:
            path: Path = []
            return (path, 0.0), []

        # Virtual source edges from all mastered nodes
        best_path, candidates = self._shortest_paths_from_mastered(mastered, goal_node_id)

        # Score candidates
        scored: List[PathWithScore] = []
        for p in candidates:
            scored.append((p, _path_score(p, self.graph, self.profile, self.cfg)))
        scored.sort(key=lambda x: x[1], reverse=True)

        best = scored[0] if scored else (best_path, _path_score(best_path, self.graph, self.profile, self.cfg))
        top_k = scored[1 : min(len(scored), self.cfg.top_k_paths)] if len(scored) > 1 else []
        return best, top_k

    def _shortest_paths_from_mastered(self, mastered: Set[str], goal: str) -> Tuple[Path, List[Path]]:
        # Multi-source shortest path using a priority queue
        frontier: List[Tuple[float, str, Optional[str]]] = []  # (priority, node, parent)
        dist: Dict[str, float] = {}
        parent: Dict[str, Optional[str]] = {}

        # Initialize with mastered nodes as zero-cost sources
        for src in mastered:
            dist[src] = 0.0
            parent[src] = None
            heapq.heappush(frontier, (0.0, src, None))

        visited: Set[str] = set()

        while frontier:
            pri, node_id, _ = heapq.heappop(frontier)
            if node_id in visited:
                continue
            visited.add(node_id)

            if node_id == goal:
                break

            current_path_nodes: Set[str] = set()
            # reconstruct partial path nodes for prereq check (approximate)
            cur = node_id
            while cur is not None:
                current_path_nodes.add(cur)
                cur = parent.get(cur)

            for neigh in self.graph.neighbors(node_id):
                if not _prerequisites_satisfied_for_candidate(neigh, mastered, current_path_nodes, self.graph):
                    continue

                node_cost = self._edge_cost(node_id, neigh)
                new_dist = pri + node_cost + (0.0 if self.cfg.algorithm == "dijkstra" else _heuristic(neigh, goal, self.graph))

                if new_dist < dist.get(neigh, float("inf")):
                    dist[neigh] = new_dist
                    parent[neigh] = node_id
                    heapq.heappush(frontier, (new_dist, neigh, node_id))

        path = self._reconstruct_path(parent, goal)
        if not path and self.graph.has_node(goal):
            # If no path found but goal exists, fall back: try linearizing prerequisites greedily
            path = self._greedy_prereq_path(mastered, goal)
        return path, ([path] if path else [])

    def _edge_cost(self, src: str, dst: str) -> float:
        node = self.graph.get_node(dst)
        mastery_gap = 1.0 - self.profile.get_mastery(dst)
        # Cost is a positive accumulation of time, difficulty, and mastery gap
        return (
            self.cfg.weight_time_cost * float(node.estimated_time_hours)
            + self.cfg.weight_difficulty_cost * float(node.difficulty)
            + self.cfg.weight_mastery_gap_cost * float(mastery_gap)
        )

    @staticmethod
    def _reconstruct_path(parent: Dict[str, Optional[str]], goal: str) -> Path:
        if goal not in parent:
            return []
        cur = goal
        rev: List[str] = []
        while cur is not None:
            rev.append(cur)
            cur = parent.get(cur)
        rev.reverse()
        return rev

    def _greedy_prereq_path(self, mastered: Set[str], goal: str) -> Path:
        # DFS from prerequisites to goal ensuring prereqs included
        visited: Set[str] = set()
        order: List[str] = []

        def dfs(node_id: str) -> None:
            if node_id in visited:
                return
            visited.add(node_id)
            for prereq in self.graph.prerequisites_of(node_id):
                if prereq not in mastered:
                    dfs(prereq)
            order.append(node_id)

        dfs(goal)
        # remove already mastered from path
        return [n for n in order if n not in mastered]

