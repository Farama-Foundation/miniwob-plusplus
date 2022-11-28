import time

import numpy as np
import pytest

from miniwob.action import MiniWoBCoordClick, MiniWoBElementClick
from miniwob.environment import MiniWoBEnvironment


class MiniWoBTester:
    # Subclasses should set this field
    TASK_NAME = None

    @pytest.fixture
    def env(self):
        env = MiniWoBEnvironment(subdomain=self.TASK_NAME)
        yield env
        env.close()


class TestMiniWoBEnvironment(MiniWoBTester):
    TASK_NAME = "click-test"

    ################################
    # Helpers

    def get_coord_click(self, observation):
        """Get the action that clicks the button."""
        for element in observation.dom_elements:
            if element.tag == "button":
                action = MiniWoBCoordClick(element.left + 5, element.top + 5)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(observation.dom_elements)}")

    def get_element_click(self, observation):
        """Get the action that clicks the button."""
        for element in observation.dom_elements:
            if element.tag == "button":
                action = MiniWoBElementClick(element, fail_hard=True)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(observation.dom_elements)}")

    # get_click = get_coord_click
    get_click = get_element_click

    ################################
    # Tests

    def test_do_nothing(self, env):
        """Test the ability to start an instance for the click-test task."""
        observation, info = env.reset()
        assert observation.utterance == "Click the button."
        assert any(element.tag == "button" for element in observation.dom_elements)

    def test_run(self, env):
        """Test reset() and step()."""
        observation, info = env.reset()
        assert observation.utterance == "Click the button."
        # Test empty action
        observation, reward, terminated, truncated, info = env.step(None)
        assert observation.utterance == "Click the button."
        assert reward == 0
        assert terminated is False
        assert terminated is False
        # Test clicking
        action = self.get_click(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        assert terminated is True
        assert truncated is False
        # Test reset
        observation, info = env.reset()
        assert observation.utterance == "Click the button."
        # Test clicking again
        action = self.get_click(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        assert terminated is True
        assert truncated is False

    def test_timeout(self, env):
        """Test environment timeout."""
        observation, info = env.reset()
        assert observation.utterance == "Click the button."
        # Wait for timeout
        time.sleep(12)
        observation, reward, terminated, truncated, info = env.step(None)
        assert reward < 0
        assert terminated is True
        assert truncated is False
        # Start again
        observation, info = env.reset()
        assert observation.utterance == "Click the button."
        observation, reward, terminated, truncated, info = env.step(None)
        assert reward == 0
        assert terminated is False
        assert truncated is False

    def test_speed(self, env):
        """Test the processing speed for step()."""
        observation, info = env.reset()
        start_time = time.time()
        elapsed = []
        N = 50
        for i in range(1, N + 1):
            print("Iteration", i, "/", N)
            observation, reward, terminated, truncated, info = env.step(None)
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
    TASK_NAME = "click-button"

    def get_button_click(self, observation):
        """Get the action that clicks the button."""
        for element in observation.dom_elements:
            if element.tag == "button" and element.text == observation.fields["target"]:
                action = MiniWoBElementClick(element, fail_hard=True)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(observation.dom_elements)}")

    def test_seed(self, env):
        observation_1, infos = env.reset(seed=31416)
        observation_2, infos = env.reset(seed=227)
        observation_3, infos = env.reset(seed=227)
        observation_4, infos = env.reset(seed=31416)
        # Check that everything is the same for the same seed
        assert observation_1.utterance == observation_4.utterance
        assert observation_2.utterance == observation_3.utterance
        ref_to_text_1 = {x.ref: x.text for x in observation_1.dom_elements}
        ref_to_text_2 = {x.ref: x.text for x in observation_2.dom_elements}
        ref_to_text_3 = {x.ref: x.text for x in observation_3.dom_elements}
        ref_to_text_4 = {x.ref: x.text for x in observation_4.dom_elements}
        assert ref_to_text_1 == ref_to_text_4
        assert ref_to_text_2 == ref_to_text_3
        assert ref_to_text_1 != ref_to_text_2
        # Compute the correct action from observation 1
        # and apply it on observation 4 (same seed)
        action = self.get_button_click(observation_1)
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        assert terminated is True


class TestMiniWoBMode(MiniWoBTester):
    TASK_NAME = "click-test-transfer"

    def get_button_click(self, observation, text):
        """Get the action that clicks the button."""
        for element in observation.dom_elements:
            if element.tag == "button" and element.text == text:
                action = MiniWoBElementClick(element, fail_hard=True)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(observation.dom_elements)}")

    def test_mode(self, env):
        """Test if setting the mode works.
        - mode = 'train': click on button ONE
        - mode = 'test':  click on button TWO
        """
        # Training time
        observation, info = env.reset()
        assert observation.utterance == "Click button ONE."
        action = self.get_button_click(observation, "ONE")
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        observation, info = env.reset()
        assert observation.utterance == "Click button ONE."
        action = self.get_button_click(observation, "TWO")
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward < 0
        # Test time
        env.set_data_mode("test")
        observation, info = env.reset()
        assert observation.utterance == "Click button TWO."
        action = self.get_button_click(observation, "ONE")
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward < 0
        # Test time again; mode should be persistent
        observation, info = env.reset()
        assert observation.utterance == "Click button TWO."
        action = self.get_button_click(observation, "TWO")
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        # Training time again: set mode with reset()
        observation, info = env.reset(options={"data_mode": "train"})
        assert observation.utterance == "Click button ONE."
        action = self.get_button_click(observation, "ONE")
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward > 0
        # Training time again; mode should be persistent
        observation, info = env.reset()
        assert observation.utterance == "Click button ONE."
        action = self.get_button_click(observation, "TWO")
        observation, reward, terminated, truncated, info = env.step(action)
        assert reward < 0


################################################


class TestMiniWoBFields(MiniWoBTester):
    TASK_NAME = "email-inbox-forward-nl"

    def test_fields(self, env):
        print("=" * 40)
        # Training time
        observation, info = env.reset()
        assert "by" in observation.fields.keys
        assert "to" in observation.fields.keys
        assert observation.fields["by"] in observation.utterance
        assert observation.fields["to"] in observation.utterance
        # Test time
        observation, info = env.reset(options={"data_mode": "test"})
        assert observation.fields.keys == ["dummy"]
        assert observation.utterance
        # Training time again
        observation, infos = env.reset(options={"data_mode": "train"})
        assert "by" in observation.fields.keys
        assert "to" in observation.fields.keys
        assert observation.fields["by"] in observation.utterance
        assert observation.fields["to"] in observation.utterance
