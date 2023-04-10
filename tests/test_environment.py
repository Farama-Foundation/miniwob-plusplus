"""Test environment methods."""
import time

import gymnasium
import numpy as np
import pytest

from miniwob.action import ActionTypes
from miniwob.fields import field_lookup


class MiniWoBTester:
    """Base class for testing on a single task."""

    # Subclasses should set this field
    ENV_NAME = ""

    @pytest.fixture
    def env(self):
        """Yield an environment for the task."""
        env = gymnasium.make(self.ENV_NAME)
        yield env
        env.close()

    ################################
    # Helpers

    def create_click_element_action(self, env, element):
        """Create an action that clicks in the specified element."""
        action = env.action_space.sample()
        action["action_type"] = env.action_space_config.action_types.index(
            ActionTypes.CLICK_ELEMENT
        )
        action["ref"] = element["ref"]
        return action

    def create_click_button_action(self, env, obs, button_text):
        """Create an action that clicks on the button with the specified text."""
        for element in obs["dom_elements"]:
            if element["tag"] == "button" and element["text"] == button_text:
                return self.create_click_element_action(env, element)
        assert False, f"{button_text} button not found"


class TestMiniWoBEnvironment(MiniWoBTester):
    """Tests for basic environment functions."""

    ENV_NAME = "miniwob/click-test-v1"

    ################################
    # Tests

    def test_do_nothing(self, env):
        """Test the ability to start an instance for the click-test task."""
        obs, info = env.reset()
        assert obs["utterance"] == "Click the button."
        assert any(element["tag"] == "button" for element in obs["dom_elements"])

    def test_run(self, env):
        """Test reset() and step()."""
        obs, info = env.reset()
        assert obs["utterance"] == "Click the button."
        # Test empty action
        obs, reward, terminated, truncated, info = env.step(None)
        assert obs["utterance"] == "Click the button."
        assert reward == 0
        assert terminated is False
        assert terminated is False
        # Test clicking
        action = self.create_click_button_action(env, obs, "Click Me!")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        assert terminated is True
        assert truncated is False
        # Test reset
        obs, info = env.reset()
        assert obs["utterance"] == "Click the button."
        # Test clicking again
        action = self.create_click_button_action(env, obs, "Click Me!")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        assert terminated is True
        assert truncated is False

    def test_timeout(self, env):
        """Test environment timeout."""
        obs, info = env.reset()
        assert obs["utterance"] == "Click the button."
        # Wait for timeout
        time.sleep(12)
        obs, reward, terminated, truncated, info = env.step(None)
        assert reward < 0
        assert terminated is True
        assert truncated is False
        # Start again
        obs, info = env.reset()
        assert obs["utterance"] == "Click the button."
        obs, reward, terminated, truncated, info = env.step(None)
        assert reward == 0
        assert terminated is False
        assert truncated is False

    def test_speed(self, env):
        """Test the processing speed for step()."""
        obs, info = env.reset()
        start_time = time.time()
        elapsed = []
        N = 50
        for i in range(1, N + 1):
            print("Iteration", i, "/", N)
            obs, reward, terminated, truncated, info = env.step(None)
            assert terminated is False
            elapsed.append(time.time() - start_time)
            start_time = time.time()
        mean = sum(elapsed) / len(elapsed)
        print("Average time:", mean)
        print("SD:", sum((x - mean) ** 2 for x in elapsed) / len(elapsed))

    def test_attention(self, env):
        """Test that visualize_attention() does not crash."""
        env.reset()
        attention = np.random.rand(20, 20) * 0.02
        env.visualize_attention(attention)
        time.sleep(1)
        env.visualize_attention(None)
        time.sleep(1)


################################################


class TestMiniWoBSeed(MiniWoBTester):
    """Tests for seed determinism."""

    ENV_NAME = "miniwob/click-button-v1"

    def test_seed(self, env):
        """Test whether the same seed gives the same result."""
        obs_1, info_1 = env.reset(seed=31416)
        obs_2, info_2 = env.reset(seed=227)
        obs_3, info_3 = env.reset(seed=227)
        obs_4, info_4 = env.reset(seed=31416)
        # Check that everything is the same for the same seed
        assert obs_1["utterance"] == obs_4["utterance"]
        assert obs_2["utterance"] == obs_3["utterance"]
        ref_to_text_1 = {x["ref"]: x["text"] for x in obs_1["dom_elements"]}
        ref_to_text_2 = {x["ref"]: x["text"] for x in obs_2["dom_elements"]}
        ref_to_text_3 = {x["ref"]: x["text"] for x in obs_3["dom_elements"]}
        ref_to_text_4 = {x["ref"]: x["text"] for x in obs_4["dom_elements"]}
        assert ref_to_text_1 == ref_to_text_4
        assert ref_to_text_2 == ref_to_text_3
        assert ref_to_text_1 != ref_to_text_2
        # Compute the correct action from obs 1
        # and apply it on obs 4 (same seed)
        action = self.create_click_button_action(
            env, obs_1, field_lookup(obs_1["fields"], "target")
        )
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        assert terminated is True


class TestMiniWoBMode(MiniWoBTester):
    """Tests for the data mode (available in some tasks)."""

    ENV_NAME = "miniwob/click-test-transfer-v1"

    def test_mode(self, env):
        """Test if setting the mode works.

        - mode = 'train': click on button ONE
        - mode = 'test':  click on button TWO
        """
        # Training time
        obs, info = env.reset()
        assert obs["utterance"] == "Click button ONE."
        action = self.create_click_button_action(env, obs, "ONE")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        obs, info = env.reset()
        assert obs["utterance"] == "Click button ONE."
        action = self.create_click_button_action(env, obs, "TWO")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward < 0
        # Test time
        env.set_data_mode("test")
        obs, info = env.reset()
        assert obs["utterance"] == "Click button TWO."
        action = self.create_click_button_action(env, obs, "ONE")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward < 0
        # Test time again; mode should be persistent
        obs, info = env.reset()
        assert obs["utterance"] == "Click button TWO."
        action = self.create_click_button_action(env, obs, "TWO")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        # Training time again: set mode with reset()
        obs, info = env.reset(options={"data_mode": "train"})
        assert obs["utterance"] == "Click button ONE."
        action = self.create_click_button_action(env, obs, "ONE")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        # Training time again; mode should be persistent
        obs, info = env.reset()
        assert obs["utterance"] == "Click button ONE."
        action = self.create_click_button_action(env, obs, "TWO")
        obs, reward, terminated, truncated, info = env.step(action)
        assert reward < 0


################################################


class TestMiniWoBFields(MiniWoBTester):
    """Tests for field extraction."""

    ENV_NAME = "miniwob/email-inbox-forward-nl-v1"

    def test_fields(self, env):
        """Test field extraction."""
        # Training time
        obs, info = env.reset()
        assert {"by", "to"} <= {x[0] for x in obs["fields"]}
        assert field_lookup(obs["fields"], "by") in obs["utterance"]
        assert field_lookup(obs["fields"], "to") in obs["utterance"]
        # Test time
        obs, info = env.reset(options={"data_mode": "test"})
        assert not obs["fields"]
        assert obs["utterance"]
        # Training time again
        obs, info = env.reset(options={"data_mode": "train"})
        assert {"by", "to"} <= {x[0] for x in obs["fields"]}
        assert field_lookup(obs["fields"], "by") in obs["utterance"]
        assert field_lookup(obs["fields"], "to") in obs["utterance"]
