"""Test utilities."""
from typing import Iterable

import gymnasium as gym


def get_all_registered_miniwob_envs() -> Iterable[str]:
    """Return the name of all registered MiniWoB environments."""
    envs = []
    for env_id, env_spec in gym.registry.items():
        # TODO: Enable flightwob tasks.
        if env_spec.namespace == "miniwob" and "flight." not in env_id:
            envs.append(env_id)
    return sorted(envs)
