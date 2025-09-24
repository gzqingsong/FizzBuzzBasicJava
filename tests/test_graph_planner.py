from learning_path_planner.data.models import KnowledgeEdge, KnowledgeNode, StudentProfile
from learning_path_planner.graph.knowledge_graph import KnowledgeGraph
from learning_path_planner.combiner.hybrid_planner import HybridPlanner


def test_hybrid_planner_generates_prereq_path():
    graph = KnowledgeGraph()
    # Nodes
    graph.add_node(KnowledgeNode("A", "A", difficulty=0.3, importance=0.5, estimated_time_hours=1.0))
    graph.add_node(KnowledgeNode("B", "B", difficulty=0.5, importance=0.6, estimated_time_hours=1.5))
    graph.add_node(KnowledgeNode("C", "C", difficulty=0.7, importance=0.9, estimated_time_hours=2.0))
    # Edges A->B->C (prerequisites)
    graph.add_edge(KnowledgeEdge("A", "B", relation_type="prerequisite"))
    graph.add_edge(KnowledgeEdge("B", "C", relation_type="prerequisite"))

    profile = StudentProfile(mastery={"A": 0.8, "B": 0.2, "C": 0.0}, learning_style="visual", cognitive_level="intermediate")

    planner = HybridPlanner(graph, profile)
    result = planner.plan("C")
    path = result["path"]

    assert path[-1] == "C"
    assert "A" not in path  # already mastered, should be skipped by rules
    assert path == ["B", "C"]

