from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

from learning_path_planner.planners.rl.env import LearningEnv


@dataclass
class QConfig:
    alpha: float = 0.5
    gamma: float = 0.95
    epsilon: float = 0.1
    state_rounding: int = 1  # round mastery values to 1 decimal for hashing
    episodes: int = 100


def _state_key(state: Dict[str, float], rounding: int) -> Tuple[Tuple[str, float], ...]:
    return tuple(sorted((k, round(v, rounding)) for k, v in state.items()))


class QLearningAgent:
    def __init__(self, env: LearningEnv, cfg: QConfig | None = None) -> None:
        self.env = env
        self.cfg = cfg or QConfig()
        self.q: Dict[Tuple, Dict[str, float]] = defaultdict(lambda: defaultdict(float))

    def policy(self, state: Dict[str, float], available_actions: Iterable[str]) -> str:
        import random

        if random.random() < self.cfg.epsilon:
            return random.choice(list(available_actions))
        key = _state_key(state, self.cfg.state_rounding)
        q_values = self.q[key]
        # select max-Q action; default 0 for unseen
        best_action = None
        best_value = float("-inf")
        for a in available_actions:
            val = q_values.get(a, 0.0)
            if val > best_value:
                best_value = val
                best_action = a
        return best_action or list(available_actions)[0]

    def train(self) -> None:
        import random

        for _ in range(self.cfg.episodes):
            state, info = self.env.reset()
            done = info.get("done", False)
            while not done:
                actions = self.env.graph.all_nodes()
                action = self.policy(state, actions)
                next_state, reward, done, _ = self.env.step(action)

                s_key = _state_key(state, self.cfg.state_rounding)
                ns_key = _state_key(next_state, self.cfg.state_rounding)

                best_next = 0.0
                if self.q[ns_key]:
                    best_next = max(self.q[ns_key].values())

                old = self.q[s_key].get(action, 0.0)
                self.q[s_key][action] = old + self.cfg.alpha * (reward + self.cfg.gamma * best_next - old)

                state = next_state

