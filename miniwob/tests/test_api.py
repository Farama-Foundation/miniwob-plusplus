import gymnasium
from gymnasium import spaces
from gymnasium.utils.env_checker import check_env
from gymnasium.wrappers import FlattenObservation

import miniwob  # noqa: F401


class TestGymAPI:
    def test_click_test_env(self):
        """Check that the click-test environment follows Gym API."""
        env = gymnasium.make("miniwob/click-test-v1")
        check_env(env.unwrapped)
        env.close()

    def test_flattened_observation_space(self):
        """Verify the flattened observation space."""
        env = gymnasium.make("miniwob/login-user-v1")
        check_env(env.unwrapped)
        assert isinstance(env.observation_space, spaces.Dict)
        assert set(env.observation_space) == {"utterance", "dom_elements", "screenshot"}
        # dom_elements is a Sequence space and cannot be flattened.
        # But each element in the Sequence can be flattened.
        env = FlattenObservation(env)
        assert isinstance(env.observation_space, spaces.Dict)
        assert isinstance(env.observation_space["utterance"], spaces.Box)
        assert isinstance(env.observation_space["dom_elements"], spaces.Sequence)
        assert isinstance(env.observation_space["screenshot"], spaces.Box)
        env.close()
