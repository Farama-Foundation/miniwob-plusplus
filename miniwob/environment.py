"""MiniWoB environment."""
import logging
from typing import Any, Dict, Mapping, Optional, Tuple, Union

import gymnasium as gym
import numpy as np

from miniwob.action import Action, ActionSpaceConfig, ActionTypes
from miniwob.fields import FieldExtractor
from miniwob.observation import Observation, get_observation_space
from miniwob.reward import RewardProcessor
from miniwob.selenium_instance import SeleniumInstance


class MiniWoBEnvironment(gym.Env):
    """Abstract class for MiniWoB environments."""

    metadata = {"render_modes": ["human"], "render_fps": None}
    reward_range = (-1, 1)

    # MiniWoB task name, which can be specified in the child class.
    subdomain = None

    def __init__(
        self,
        subdomain: Optional[str] = None,
        render_mode: Optional[str] = None,
        base_url: Optional[str] = None,
        action_space_config: Union[str, ActionSpaceConfig] = "all_supported",
        field_extractor: Optional[FieldExtractor] = None,
        reward_processor: Optional[RewardProcessor] = None,
        wait_ms: float = 0.0,
        block_on_reset: bool = True,
        refresh_freq: int = 0,
        data_mode: str = "train",
    ):
        """Creates a new MiniWoBEnvironment.

        Args:
            subdomain: MiniWoB task name (e.g., "click-test") corresponding
                to the HTML filename. This should be left as None for child
                classes of MiniWoBEnvironment.
            render_mode: Render mode. Supported values are:
                - None: Headless Chrome (default)
                - "human": Show the Chrome screen
            base_url: Base URL, which is usually one of the following
                - http://localhost:8000/miniwob/     (served by http-serve)
                - file:///path/to/miniwob-plusplus/html/miniwob/
                If None, infers the file:// path from this module's location.
            action_space_config: ActionSpaceConfig object or a preset name.
            field_extractor: A function that takes the utterance and returns
                a list of fields as key-value tuples (see miniwob.fields).
                If None, uses the default one for the task.
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
        if self.subdomain:
            if subdomain:
                raise ValueError("`subdomain` is already specified.")
        else:
            if not subdomain:
                raise ValueError("`subdomain` is not specified.")
            self.subdomain = subdomain
        if render_mode and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Invalid render mode: {render_mode}")
        self.render_mode = render_mode
        self.instance_kwargs = {
            "subdomain": self.subdomain,
            "headless": (render_mode is None),
            "base_url": base_url,
            "field_extractor": field_extractor,
            "reward_processor": reward_processor,
            "wait_ms": wait_ms,
            "block_on_reset": block_on_reset,
            "refresh_freq": refresh_freq,
            "data_mode": data_mode,
        }
        self._hard_reset_instance()
        if isinstance(action_space_config, str):
            self.action_space_config = ActionSpaceConfig.get_preset(action_space_config)
        else:
            self.action_space_config = action_space_config
        self.action_space_config.screen_width = self.instance.task_width
        self.action_space_config.screen_height = self.instance.task_height
        self.action_space = self.action_space_config.get_action_space()
        self.observation_space = get_observation_space(
            screen_width=self.instance.task_width,
            screen_height=self.instance.task_height,
        )

    def _hard_reset_instance(self):
        """Close the current SeleniumInstance (if exists) and starts a new one."""
        if hasattr(self, "instance") and self.instance:
            self.instance.close()
        logging.info("Starting WebDriver Instance")
        self.instance = SeleniumInstance(index=0, **self.instance_kwargs)
        self.instance.start()
        self.instance.wait()

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Mapping[str, Any]] = None,
    ) -> Tuple[Observation, Dict[str, Any]]:
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
        super().reset(seed=seed)
        # Hard reset the instances if needed
        if not self.instance or self.instance.died:
            logging.warning("Hard-resetting the instance ...")
            self._hard_reset_instance()
        # Process the options
        options = options or {}
        if "data_mode" in options:
            self.set_data_mode(options["data_mode"])
        if "record_screenshots" in options:
            self.set_record_screenshots(options["record_screenshots"])
        # We pass lists for the instance to modify in-place.
        obs = [{}]
        infos = [{}]
        self.instance.call(self.instance.reset, obs, infos, seed)
        self.instance.wait()
        return obs[0], infos[0]

    def step(
        self, action: Action
    ) -> Tuple[Observation, float, bool, bool, Dict[str, Any]]:
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
        obs = [{}]
        rewards = [-1.0]
        dones = [True]
        truncs = [False]
        infos = [{}]
        self.instance.call(
            self.instance.step,
            action,
            self.action_space_config,
            obs,
            rewards,
            dones,
            infos,
        )
        self.instance.wait()
        return obs[0], rewards[0], dones[0], truncs[0], infos[0]

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
        self.instance.mode = mode

    def set_record_screenshots(self, record_screenshots: bool):
        """Adjust whether the record the screenshots.

        Args:
            record_screenshots (bool): Whether to record screenshots.
        """
        self.instance.record_screenshots = record_screenshots

    def visualize_attention(self, attentions: Optional[np.ndarray]):
        """Send the attention weights to be visualized.

        Args:
            attentions: attention weights, which is one of:
                - None: Do not do anything
                - np.array or 2d list of shape (num_grid_rows, num_grid_cols)
                - np.array or 2d list of shape (0, 0): Clear the visualization
        """
        self.instance.call(self.instance.visualize_attention, attentions)
        self.instance.wait()

    def close(self):
        """Close the instance."""
        self.instance.call(self.instance.close)
        self.instance.wait()

    def create_action(
        self,
        action_type: Union[int, np.ndarray, str, ActionTypes],
        **kwargs,
    ) -> Action:
        """Initializes an action with the specified type and random values.

        Args:
            action_type: Action type, which can be an index of the
                action_space_config.action_types array (int or scalar np.ndarray)
                or an action name (str of ActionTypes enum).
            kwargs: Additional key-value pairs to set. An error will be raised
                if the key is not in the action space.

        Returns:
            An action from the action space.
        """
        action = self.action_space.sample()
        if isinstance(action_type, (str, ActionTypes)):
            action["action_type"] = self.action_space_config.action_types.index(
                action_type
            )
        elif isinstance(action_type, int):
            action["action_type"] = action_type
        elif isinstance(action_type, np.ndarray):
            action["action_type"] = action_type.item()
        else:
            raise ValueError(f"Unknown action_type: {repr(action_type)}")
        for key, value in kwargs.items():
            if key not in action:
                raise KeyError(f"Key {key} not in valid action keys {list(action)}.")
            action[key] = value
        return action
