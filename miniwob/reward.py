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
    """Return the original reward with time penalty.

    This is the reward as defined in the environment.
    """
    return float(metadata["env_reward"])


def get_raw_reward(metadata: Metadata) -> float:
    """Return the raw reward without time penalty.

    This is usually 1 for success and -1 for failure, but not always.
    """
    return float(metadata["raw_reward"])


def get_click_checkboxes_hard(metadata: Metadata) -> float:
    """Return the reward without partial credits.

    This can be applied when the original environment gives partial credits
    in addition to the time penalty (e.g., click-checkboxes).
    Give 1 if the raw reward is 1. Otherwise, give -1.
    """
    if not metadata["done"]:
        return 0.0
    return 1.0 if metadata["raw_reward"] == 1.0 else -1.0


def raw_reward_threshold(threshold: float) -> RewardPreprocessor:
    """Return a reward processor that cut off at a threshold."""

    def fn(metadata: Metadata) -> float:
        if metadata["raw_reward"] > threshold:
            return 1.0
        elif metadata["raw_reward"] > 0:
            return -1
        return metadata["raw_reward"]

    return fn
