from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from typing import Dict

from learning_path_planner.combiner.hybrid_planner import HybridPlanner, HybridConfig
from learning_path_planner.data.models import KnowledgeEdge, KnowledgeGraphData, KnowledgeNode, StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph
from learning_path_planner.planners.graph_planner import PlannerConfig
from learning_path_planner.rules.engine import RulesConfig


def _load_graph(path: str) -> KnowledgeGraph:
    return KnowledgeGraph.from_json(path)


def _load_student(path: str) -> StudentProfile:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return StudentProfile(**data)


def _load_config(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Learning Path Planner CLI")
    parser.add_argument("--graph", required=True, help="Path to knowledge_graph.json")
    parser.add_argument("--student", required=True, help="Path to student_profile.json")
    parser.add_argument("--config", required=True, help="Path to default.json")
    parser.add_argument("--goal", required=True, help="Goal knowledge node id")
    args = parser.parse_args()

    graph = _load_graph(args.graph)
    student = _load_student(args.student)
    cfg_dict = _load_config(args.config)

    planner_cfg = PlannerConfig(**cfg_dict.get("planner", {}))
    rules_cfg = RulesConfig(**cfg_dict.get("rules", {}))
    hybrid_cfg = HybridConfig(graph=planner_cfg, rules=rules_cfg)

    planner = HybridPlanner(graph, student, hybrid_cfg)
    result = planner.plan(args.goal)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

