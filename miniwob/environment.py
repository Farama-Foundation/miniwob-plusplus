import logging

import gymnasium as gym

from miniwob.action import MiniWoBActionSpace
from miniwob.instance import MiniWoBInstance
from miniwob.state import MiniWoBStateSpace


class MiniWoBEnvironment(gym.Env):
    """MiniWoB environment."""

    # render_mode = None: Headless Chrome (default)
    # render_mode = "human": Show the Chrome screen
    metadata = {"render_modes": ["human"]}
    reward_range = (-1, 1)

    def __init__(
        self,
        subdomain,
        render_mode=None,
        base_url=None,
        cache_state=False,
        threading=True,
        reward_processor=None,
        wait_ms=0.0,
        block_on_reset=True,
        refresh_freq=0,
        data_mode="train",
    ):
        """Creates a new MiniWoBEnvironment.

        Args:
            subdomain (str): MiniWoB task name (e.g., "click-test")
            render_mode (str): Render mode
            base_url (str): Base URL, which is usually one of the following
                - http://localhost:8000/     (served by http-serve)
                - file:///path/to/miniwob-plusplus/html/
                If None, infers the file:// path from this module's location.
            cache_state (bool): Whether to cache and return the initial
                state; only make sense if the task interface never changes
            threading (bool): Whether to run the instances in separate threads
            reward_processor (callable; optional): A function that takes
                the metadata and return a reward (see miniwob.reward)
            wait_ms (float): Pause the instance after each action for this
                amount of time (in milliseconds).
            block_on_reset (bool): On reset, block until the page loads.
            refresh_freq (int): Every this number of episodes,
                refresh the page at the beginning of the next episode.
                Takes time but cleans up any lingering states and memory leaks.
                *** Must specify `seeds` at each reset call.
            data_mode (str): Data mode (e.g., "train", "test"). Used in some
                subdomains.
        """
        if render_mode and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Invalid render mode: {render_mode}")
        self.render_mode = render_mode
        # self.instance will be initialized in reset()
        self.instance = None
        self.instance_kwargs = {
            "subdomain": subdomain,
            "headless": (render_mode is None),
            "base_url": base_url,
            "cache_state": cache_state,
            "threading": threading,
            "reward_processor": reward_processor,
            "wait_ms": wait_ms,
            "block_on_reset": block_on_reset,
            "refresh_freq": refresh_freq,
            "data_mode": data_mode,
        }
        self.action_space = MiniWoBActionSpace()
        self.observation_space = MiniWoBStateSpace()

    def _hard_reset_instance(self):
        """Closes the current MiniWoBInstance (if exists) and starts a new one."""
        if self.instance:
            self.instance.close()
        logging.info("Starting WebDriver Instance")
        self.instance = MiniWoBInstance(index=0, **self.instance_kwargs)
        self.instance.start()
        self.instance.wait()

    def reset(self, seed=None, options=None):
        """Reset the instance.

        Args:
            seed (optional int): Random seed.
            options (optional dict): An option dict with the following allowed keys:
                - data_mode (str): set the data mode to this value.
                - record_screenshots (bool): Whether to record screenshots.
        Returns:
            observation (MiniWoBState)
            info (dict)
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
        states = [None]
        infos = [None]
        self.instance.call(self.instance.reset, states, infos, seed)
        self.instance.wait()
        return states[0], infos[0]

    def step(self, action):
        """Applies an action on the instance and returns the result.

        Args:
            action (MiniWoBAction)

        Returns:
            observation (MiniWoBState)
            reward (float)
            terminated (bool)
            truncated (bool)
            infos (dict): additional debug information.
        """
        # We pass lists for the instance to modify in-place.
        states = [None]
        rewards = [-1.0]
        dones = [True]
        truncs = [False]
        infos = [None]
        self.instance.call(self.instance.step, action, states, rewards, dones, infos)
        self.instance.wait()
        return states[0], rewards[0], dones[0], truncs[0], infos[0]

    def render(self):
        # The currently supported render modes do not require computing the render.
        return None

    def set_data_mode(self, mode):
        """Set the data mode ("train", "test", etc.) of the instance.
        Will have effect starting from the next episode.

        Args:
            mode (str)
        """
        self.instance.mode = mode

    def set_record_screenshots(self, record_screenshots):
        """Adjust whether the record the screenshots of the states.

        Args:
            record_screenshots (bool)
        """
        self.instance.record_screenshots = record_screenshots

    def visualize_attention(self, attentions):
        """Sends the attention weights to be visualized.

        Args:
            attentions: attention weights, which is one of:
                - None: Do not do anything
                - np.array or 2d list of shape (num_grid_rows, num_grid_cols)
                - np.array or 2d list of shape (0, 0): Clear the visualization
        """
        self.instance.call(self.instance.visualize_attention, attentions)
        self.instance.wait()

    def close(self):
        self.instance.call(self.instance.close)
        self.instance.wait()
