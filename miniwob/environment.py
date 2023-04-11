"""MiniWoB environment."""
import logging
from abc import ABC
from typing import Any, Dict, Mapping, Optional, Tuple, List

import gymnasium as gym
import numpy as np

from miniwob.action import Action, get_action_space
from miniwob.instance import MiniWoBInstance
from miniwob.observation import Observation, get_observation_space
from miniwob.reward import RewardPreprocessor

INSTANCES = [] # List[MiniWoBInstance]

class MiniWoBEnvironment(gym.Env, ABC):
    """Abstract class for MiniWoB environments."""

    metadata = {"render_modes": ["human"], "render_fps": None}
    reward_range = (-1, 1)

    # MiniWoB task name, which should be specified by the child class.
    subdomain = None

    def __init__(
        self,
        render_mode: Optional[str] = None,
        base_url: Optional[str] = None,
        reward_processor: Optional[RewardPreprocessor] = None,
        wait_ms: float = 0.0,
        block_on_reset: bool = True,
        refresh_freq: int = 0,
        data_mode: str = "train",
        num_instances: int = 4
    ):
        """Creates a new MiniWoBEnvironment.

        Args:
            subdomain: MiniWoB task name (e.g., "click-test")
            render_mode: Render mode. Supported values are:
                - None: Headless Chrome (default)
                - "human": Show the Chrome screen
            base_url: Base URL, which is usually one of the following
                - http://localhost:8000/     (served by http-serve)
                - file:///path/to/miniwob-plusplus/html/
                If None, infers the file:// path from this module's location.
            reward_processor: A function that takes the metadata and returns
                a reward (see miniwob.reward)
            wait_ms: Pause the instance after each action for this amount of
                time (in milliseconds).
            block_on_reset: On reset, block until the page loads.
            refresh_freq: Every this number of episodes, refresh the page at
                the beginning of the next episode. Takes time but cleans up
                any lingering states and memory leaks.
                *** Must specify `seeds` at each reset call.
            data_mode: Data mode (e.g., "train", "test"). Used in some tasks.
        """
        assert self.subdomain, "`self.subdomain` cannot be empty."
        if render_mode and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Invalid render mode: {render_mode}")
        self.render_mode = render_mode
        self.instance_kwargs = {
            "subdomain": self.subdomain,
            "headless": (render_mode is None),
            "base_url": base_url,
            "threading": True,
            "reward_processor": reward_processor,
            "wait_ms": wait_ms,
            "block_on_reset": block_on_reset,
            "refresh_freq": refresh_freq,
            "data_mode": data_mode,
        }

        self.num_instances = num_instances
        self._hard_reset_instance()
        self.action_space = get_action_space(
            screen_width=self.instances[0].task_width,
            screen_height=self.instances[0].task_height,
        )
        self.observation_space = get_observation_space(
            screen_width=self.instances[0].task_width,
            screen_height=self.instances[0].task_height,
        )
        self.dones = [False] * self.num_instances

    def _hard_reset_instance(self):
        """Close the current MiniWoBInstance (if exists) and starts a new one."""

        # MODIFIED: Never close the instance
        #if hasattr(self, "instance") and self.instance:
        #    self.instance.close()
        global INSTANCES
        logging.info("Starting WebDriver Instance")

        # Replace the instances that died
        if len(INSTANCES) != 0:
            for i in range(len(INSTANCES)):
                if INSTANCES[i].died:
                    INSTANCES[i] = MiniWoBInstance(index=i, **self.instance_kwargs)
                    INSTANCES[i].start()
                    INSTANCES[i].wait()
            self.instances = INSTANCES
            return
        self.instances = [MiniWoBInstance(index=i, **self.instance_kwargs) for i in range(self.num_instances)]
        INSTANCES = self.instances
        for instance in self.instances:
            instance.start()
        for instance in self.instances:
            instance.wait()

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Mapping[str, Any]] = None,
    ) -> Tuple[List[Observation], List[Dict[str, Any]]]:
        """Reset the instance.

        Args:
            seed: Random seed.
            options: An option dict with the following allowed keys:
                - data_mode (str): set the data mode to this value.
                - record_screenshots (bool): Whether to record screenshots.

        Returns:
            a tuple (observation, info):
                - observation: Initial observation from the observation space.
                - info: Auxiliary information.
        """
        # The seed in Env is actually not used
        if seed is None:
            seed = np.random.randint(0, 2 ** 31)
        super().reset(seed=seed)
        # Hard reset the instances if needed
        self._hard_reset_instance()
        # Process the options
        options = options or {}
        if "data_mode" in options:
            self.set_data_mode(options["data_mode"])
        if "record_screenshots" in options:
            self.set_record_screenshots(options["record_screenshots"])
        # We pass lists for the instance to modify in-place.
        obs = [{} for _ in range(self.num_instances)]
        infos = [{} for _ in range(self.num_instances)]
        for instance in self.instances:
            # Unsuring seeds are unique
            instance.call(instance.reset, obs, infos, seed * self.num_instances + instance.index)
        for instance in self.instances:
            instance.wait()
        self.dones = [False] * self.num_instances
        return obs, infos

    def step(
        self, actions: List[Action]
    ) -> Tuple[List[Observation], List[float], List[bool], List[bool], List[Dict[str, Any]]]:
        """Apply an action on the instance and returns the result.

        Args:
            action: An action from the action space.

        Returns:
            a tuple (observation, reward, terminated, truncated, info):
                - observation: Observation from the observation space.
                - reward: The reward.
                - terminated: Whether the episode has terminated.
                - truncated: Whether the episode has been truncated (always False).
                - info: Auxiliary information.
        """
        # We pass lists for the instance to modify in-place.
        obs = [{} for _ in range(len(actions))]
        rewards = [-1.0 for _ in range(len(actions))]
        dones = [True for _ in range(len(actions))]
        truncs = [False for _ in range(len(actions))]
        infos = [{} for _ in range(len(actions))]
        for i in range(len(actions)):
            instance = self.instances[i]
            instance.call(instance.step, actions[instance.index], obs, rewards, dones, infos) if not self.dones[instance.index] else None
        for i in range(len(actions)):
            instance = self.instances[i]
            instance.wait() if not self.dones[instance.index] else None
        self.dones = dones
        return obs, rewards, dones, truncs, infos

    def render(self) -> None:
        """Render the environment based on the render mode."""
        # The currently supported render modes do not require computing the render.
        return None

    def set_data_mode(self, mode: str):
        """Set the data mode ("train", "test", etc.) of the instance.

        The data mode will have effect starting from the next episode.

        Args:
            mode (str): The mode to set to.
        """
        for instance in self.instances:
            instance.mode = mode

    def set_record_screenshots(self, record_screenshots: bool):
        """Adjust whether the record the screenshots.

        Args:
            record_screenshots (bool): Whether to record screenshots.
        """
        for instance in self.instances:
            instance.record_screenshots = record_screenshots

    def visualize_attention(self, attentions: Optional[np.ndarray]):
        """Send the attention weights to be visualized.

        Args:
            attentions: attention weights, which is one of:
                - None: Do not do anything
                - np.array or 2d list of shape (num_grid_rows, num_grid_cols)
                - np.array or 2d list of shape (0, 0): Clear the visualization
        """
        for instance in self.instances:
            instance.call(instance.visualize_attention, attentions)
        for instance in self.instances:
            instance.wait()

    def close(self):
        """Close the instance."""
        for instance in self.instances:
            instance.call(instance.close)
        for instance in self.instances:
            instance.wait()
