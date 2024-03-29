"""Test utilities."""
from typing import Iterable

import gymnasium


def get_all_registered_miniwob_envs() -> Iterable[str]:
    """Return the name of all registered MiniWoB environments."""
    envs = []
    for env_id, env_spec in gymnasium.registry.items():
        if env_spec.namespace == "miniwob":
            envs.append(env_id)
    return sorted(envs)
