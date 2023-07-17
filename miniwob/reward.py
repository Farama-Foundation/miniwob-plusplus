"""Reward processors.

Each method takes the metadata with the following keys:
    - env_reward: MiniWoB official reward
    - raw_reward: Raw task reward without time penalty
    - done: Whether the task is done
Then it returns a reward (float).
"""
from typing import Any, Callable, Mapping


Metadata = Mapping[str, Any]
RewardPreprocessor = Callable[[Metadata], float]


def get_original_reward(metadata: Metadata) -> float:
    """Returns the original reward.

    This is the reward as defined in the environment. In all environments,
    any positive reward is scaled by the remaining time. Some environments
    also give partial rewards. See the documentation or docstring of each
    environment for details.

    The returned value is 0.0 if the episode has not terminated yet,
    and a value between -1.0 and 1.0 (inclusive) otherwise.
    """
    return float(metadata["env_reward"])


def get_raw_reward(metadata: Metadata) -> float:
    """Returns the raw reward without time penalty.

    Some environments give partial rewards. See the documentation or docstring
    of each environment for details.

    The returned value is 0.0 if the episode has not terminated yet,
    and a value between -1.0 and 1.0 (inclusive) otherwise.
    """
    return float(metadata["raw_reward"])


def get_binary_reward(metadata: Metadata) -> float:
    """Returns the reward without time penalty or partial reward.

    The returned value is 0.0 if the episode has not terminated yet,
    and either -1.0 or 1.0 otherwise.
    """
    if not metadata["done"]:
        return 0.0
    return 1.0 if metadata["raw_reward"] == 1.0 else -1.0
