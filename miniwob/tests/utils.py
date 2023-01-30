"""Test utilities."""
from typing import Iterable

from gymnasium import registry

import miniwob  # noqa: F401


def get_all_registered_miniwob_envs() -> Iterable[str]:
    """Return the name of all registered MiniWoB environments."""
    envs = []
    for key, value in registry.items():
        # TODO: Enable flightwob tasks.
        if value.namespace == "miniwob" and "flight." not in key:
            envs.append(key)
    return sorted(envs)
