import logging
import os
import sys

import gymnasium as gym

from miniwob.action import MiniWoBActionSpace
from miniwob.instance import MiniWoBInstance
from miniwob.state import MiniWoBStateSpace


class MiniWoBEnvironment(gym.Env):
    """MiniWoB environment."""

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
        num_instances=None,
    ):
        """Creates a new MiniWoBEnvironment with no instances.
        Must call configure() to set up instances.

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
            num_instances (optional int): If specified, launch multiple
                instances; the actions, observations, termination flags, etc.
                will become lists of values. (This violates the current gym API
                and is included for backward compatibility.)
        """
        if render_mode and render_mode not in self.metadata["render_modes"]:
            raise ValueError(f"Invalid render mode: {render_mode}")
        self.render_mode = render_mode
        if num_instances is not None and not (
            isinstance(num_instances, int) and num_instances > 0
        ):
            raise ValueError(
                f"num_instances must be None or positive int; got {num_instances}"
            )
        self.num_instances = num_instances
        # self.instances will be initialized in reset()
        self.instances = []
        self.died = False
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

    def _hard_reset_instances(self):
        """Creates the required number of MiniWoBInstance after closing existing ones."""
        for instance in self.instances:
            instance.close()
        self.instances = []
        for index in range(self.num_instances or 1):
            logging.info("Starting WebDriver Instance %d", index)
            instance = MiniWoBInstance(index, **self.instance_kwargs)
            instance.start()
            self.instances.append(instance)
        for instance in self.instances:
            instance.wait()

    def reset(self, seed=None, options=None):
        """Forces stop and start all instances.

        Args:
            seed (optional int): Random seed. The same seed is used for all instances.
            options (optional dict): An option dict with the following allowed keys:
                - data_mode (str): set the data mode to this value.
                - custom_seeds (list of ints): set the seed of each instance individually.
                - record_screenshots (bool): Whether to record screenshots of the states.
        Returns:
            observation (MiniWoBState or list[MiniWoBState])
            info (dict or list[dict]): additional debug information.
        """
        # The seed in Env is actually not used
        super().reset(seed=seed)
        # Hard reset the instances if needed
        if not self.instances or any(instance.died for instance in self.instances):
            logging.warning("Hard-resetting instances ...")
            self._hard_reset_instances()
        # Process the options
        options = options or {}
        seeds = [seed] * len(self.instances)
        if "custom_seeds" in options:
            seeds = options["custom_seeds"]
            assert len(seeds) == len(self.instances)
        if "data_mode" in options:
            self.set_data_mode(options["data_mode"])
        if "record_screenshots" in options:
            self.set_record_screenshots(options["record_screenshots"])
        # The ith entry in `states` will be set by the ith instance
        states = [None] * len(self.instances)
        infos = [None] * len(self.instances)
        for i, instance in enumerate(self.instances):
            instance.call(instance.reset, states, infos, seeds[i])
        for instance in self.instances:
            instance.wait()
        self.died = any(instance.died for instance in self.instances)
        if self.num_instances is None:
            return states[0], infos[0]
        else:
            return states, infos

    def step(self, actions):
        """Applies an action on each instance and returns the results.

        Args:
            actions (list[MiniWoBAction or None])

        Returns:
            observation (MiniWoBState or list[MiniWoBState])
            reward (float or list[float])
            terminated (bool or list[bool])
            truncated (bool or list[bool])
            infos (dict or list[dict]): additional debug information.
        """
        if self.num_instances is None:
            actions = [actions]
        if len(actions) != len(self.instances):
            raise ValueError(
                "len(action) is {} but there are {} instances".format(
                    len(actions), len(self.instances)
                )
            )
        # Initialize with reasonable values
        states = [None] * len(self.instances)
        rewards = [-1.0] * len(self.instances)
        dones = [True] * len(self.instances)
        truncated = [False] * len(self.instances)
        infos = [None] * len(self.instances)
        # Have the instances replace the values
        for i, instance in enumerate(self.instances):
            instance.call(instance.step, actions[i], states, rewards, dones, infos)
        for instance in self.instances:
            instance.wait()
        self.died = any(instance.died for instance in self.instances)
        if self.num_instances is None:
            return states[0], rewards[0], dones[0], truncated[0], infos[0]
        else:
            return states, rewards, dones, truncated, infos

    def render(self):
        # The currently supported render modes do not require computing the render.
        return None

    def set_data_mode(self, mode):
        """Set the data mode ("train", "test", etc.) of all instances.
        Will have effect starting from the next episode.

        Args:
            mode (str)
        """
        for instance in self.instances:
            instance.mode = mode

    def set_record_screenshots(self, record_screenshots):
        """Adjust whether the record the screenshots of the states.

        Args:
            record_screenshots (bool)
        """
        for instance in self.instances:
            instance.record_screenshots = record_screenshots

    def visualize_attention(self, attentions):
        """Sends the attention weights to be visualized.

        Args:
            attentions (list[*]): attention weight for each instance.
                Each list element is one of:
                - None: Do not do anything
                - np.array or 2d list of shape (num_grid_rows, num_grid_cols)
                - np.array or 2d list of shape (0, 0): Clear the visualization
        """
        for i, instance in enumerate(self.instances):
            instance.call(instance.visualize_attention, attentions[i])
        for instance in self.instances:
            instance.wait()

    def close(self):
        for instance in self.instances:
            instance.call(instance.close)
        for instance in self.instances:
            instance.wait()


def test_environment():
    try:
        task_name = sys.argv[1]
    except IndexError:
        print(f"Usage: python {sys.argv[0]} TASK_NAME")
        exit(1)
    env = MiniWoBEnvironment(task_name)
    base_url = os.environ.get("MINIWOB_BASE_URL")
    env.configure(num_instances=1, seeds=[0], base_url=base_url)
    states = env.reset()
    print(states[0].dom.visualize())
    env.close()


if __name__ == "__main__":
    test_environment()
