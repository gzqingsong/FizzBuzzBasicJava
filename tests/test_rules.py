from learning_path_planner.data.models import KnowledgeEdge, KnowledgeNode, StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph
from learning_path_planner.rules.engine import RulesEngine, RulesConfig


def test_rules_engine_cognitive_load_warning():
    graph = KnowledgeGraph()
    graph.add_node(KnowledgeNode("H1", "Hard 1", difficulty=0.9, importance=0.6, estimated_time_hours=1.0))
    graph.add_node(KnowledgeNode("H2", "Hard 2", difficulty=0.9, importance=0.6, estimated_time_hours=1.0))
    graph.add_node(KnowledgeNode("H3", "Hard 3", difficulty=0.9, importance=0.6, estimated_time_hours=1.0))
    graph.add_edge(KnowledgeEdge("H1", "H2", relation_type="related"))
    graph.add_edge(KnowledgeEdge("H2", "H3", relation_type="related"))

    profile = StudentProfile(mastery={})
    rules = RulesEngine(graph, profile, RulesConfig(skip_mastered=False, high_difficulty_threshold=0.75, max_consecutive_high_difficulty=2))
    path, warnings = rules.apply(["H1", "H2", "H3"])

    assert any("Cognitive load warning" in w for w in warnings)

