import gymnasium
from gymnasium.utils.env_checker import check_env

import miniwob  # noqa: F401


class TestGymAPI:
    def test_gym_api(self):
        """Check that the environment follows Gym API."""
        env = gymnasium.make("miniwob/click-test-v0")
        check_env(env)
