Learning Path Planning Agent (Python)

This project implements a modular, extensible learning path planning system. It generates personalized, efficient, and adaptive learning paths on top of a knowledge graph, combining classic graph search, a lightweight rules engine, optional reinforcement learning, and personalization adapters.

Key capabilities:
- Graph-based planning with Dijkstra/A* and multi-factor path scoring
- Rules to enforce pedagogical constraints and balance cognitive load
- Optional RL agent (tabular Q-learning) and environment stub for experimentation
- Personalization adjustments based on student learning style and mastery
- Hybrid combiner to produce a final plan
- CLI with sample data to try it out quickly


Project structure

```
learning_path_planner/
  __init__.py
  data/
    models.py
  graph/
    knowledge_graph.py
  planners/
    graph_planner.py
    rl/
      env.py
      q_learning.py
  rules/
    engine.py
  personalization/
    adapter.py
  combiner/
    hybrid_planner.py
  cli/
    main.py

configs/
  default.json

data/
  sample/
    knowledge_graph.json
    student_profile.json

tests/
  test_graph_planner.py
  test_rules.py

requirements.txt
README.md
```


Quick start

1) Use the sample data to generate a learning path:

```
python -m learning_path_planner.cli.main \
  --graph ./data/sample/knowledge_graph.json \
  --student ./data/sample/student_profile.json \
  --config ./configs/default.json \
  --goal "calculus.integration"
```

2) Run tests:

```
python -m pytest -q
```


Notes
- This code is dependency-light and uses only the Python standard library by default. No external packages are required to run the sample.
- If you want to experiment with more advanced features (e.g., deep RL, NetworkX), add them to requirements.txt as optional extras.

# FizzBuzzBasicJava
FizzBuzz implemented with basic java 

Notice:
1. Application main class: com.walter.fizzbuzz.Main
2. UT test suite class: com.walter.fizzbuzz.testsuite.FizzBuzzSuiteTest
3. The tag named 'stage1' is for stage1 requirement, while that name 'stage2' is for stage2 requirement.