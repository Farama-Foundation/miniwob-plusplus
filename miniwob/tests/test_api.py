import gymnasium
from gymnasium.utils.env_checker import check_env

import miniwob  # noqa: F401


class TestGymAPI:
    def test_click_test_env(self):
        """Check that the click-test environment follows Gym API."""
        env = gymnasium.make("miniwob/click-test-v0.0")
        check_env(env.unwrapped)
        env.close()
