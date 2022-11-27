import time

import numpy as np
import pytest

from miniwob.action import MiniWoBCoordClick, MiniWoBElementClick, MiniWoBTerminate
from miniwob.environment import MiniWoBEnvironment


class MiniWoBTester:
    # Subclasses should set this field
    TASK_NAME = None

    @pytest.fixture
    def env(self):
        env = MiniWoBEnvironment(
            subdomain=self.TASK_NAME,
            num_instances=3,
        )
        yield env
        env.close()


class TestMiniWoBEnvironment(MiniWoBTester):
    TASK_NAME = "click-test"

    ################################
    # Helpers

    def get_coord_click(self, state):
        """Get the action that clicks the button."""
        for element in state.dom_elements:
            if element.tag == "button":
                action = MiniWoBCoordClick(element.left + 5, element.top + 5)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(state.dom_elements)}")

    def get_element_click(self, state):
        """Get the action that clicks the button."""
        for element in state.dom_elements:
            if element.tag == "button":
                action = MiniWoBElementClick(element, fail_hard=True)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(state.dom_elements)}")

    # get_click = get_coord_click
    get_click = get_element_click

    ################################
    # Tests

    def test_do_nothing(self, env):
        """Test the ability to start up multiple instances."""
        env.reset()
        assert len(env.instances) == 3

    def test_run(self, env):
        """Test reset and step."""
        print("=" * 40)
        states, infos = env.reset()
        print([x.utterance for x in states])
        assert all(x.utterance == "Click the button." for x in states)
        print([x.fields for x in states])
        assert all(x.fields.keys == ["dummy"] for x in states)
        print([x.dom for x in states])
        print(states[0].dom_elements)
        print(states[0].dom.visualize())
        ################################
        print("=" * 40)
        states, rewards, dones, truncs, infos = env.step([None, None, None])
        print([x.utterance for x in states])
        print([x.dom for x in states])
        print(rewards)
        assert rewards == [0, 0, 0]
        print(dones)
        assert dones == [False, False, False]
        print(infos)
        ################################
        # Test clicking
        print("=" * 40)
        action = self.get_click(states[1])
        states, rewards, dones, truncs, infos = env.step([None, action, None])
        assert states[1] is None
        states = [states[0], states[2]]
        print([x.utterance for x in states])
        print([x.dom for x in states])
        print(rewards)
        assert rewards[0] == 0 and rewards[1] > 0 and rewards[2] == 0
        print(dones)
        assert dones == [False, True, False]
        print(infos)
        ################################
        # Wait for timeout
        print("=" * 40)
        for i in range(1, 13):
            print(f"Sleeping ... ({i})")
            time.sleep(1)
        states, rewards, dones, truncs, infos = env.step([None, None, None])
        assert states == [None, None, None]
        print(rewards)
        assert rewards[0] < 0 and rewards[1] > 0 and rewards[2] < 0
        print(dones)
        assert dones == [True, True, True]
        print(infos)
        ################################
        # Start again
        print("=" * 40)
        states, infos = env.reset()
        print([x.utterance for x in states])
        print([x.dom for x in states])
        ################################
        print("=" * 40)
        states, rewards, dones, truncs, infos = env.step([None, None, None])
        print([x.utterance for x in states])
        print([x.dom for x in states])
        print(rewards)
        assert rewards == [0, 0, 0]
        print(dones)
        assert dones == [False, False, False]
        print(infos)

    def test_speed(self, env):
        states, infos = env.reset()
        start_time = time.time()
        elapsed = []
        N = 50
        for i in range(1, N + 1):
            print("Iteration", i, "/", N)
            actions = [None] * len(states)
            states, rewards, dones, truncs, infos = env.step(actions)
            elapsed.append(time.time() - start_time)
            start_time = time.time()
        mean = sum(elapsed) / len(elapsed)
        print("Average time:", mean)
        print("SD:", sum((x - mean) ** 2 for x in elapsed) / len(elapsed))

    def test_reset(self, env):
        print("=" * 40)
        states, infos = env.reset()
        # Test clicking
        action = self.get_click(states[1])
        states, rewards, dones, truncs, infos = env.step([None, action, None])
        assert dones == [False, True, False]
        print(infos)
        # Should issue a warning on the second instance
        states, rewards, dones, truncs, infos = env.step([None, action, None])
        assert dones == [False, True, False]
        print(infos)
        # Hard reset
        states, infos = env.reset()
        states, rewards, dones, truncs, infos = env.step([None, None, None])
        assert dones == [False, False, False]
        print(infos)
        # Now click the first and second
        action_0 = self.get_click(states[0])
        action_1 = self.get_click(states[1])
        states, rewards, dones, truncs, infos = env.step([action_0, action_1, None])
        assert dones == [True, True, False]
        print(infos)

    def test_attention(self, env):
        print("=" * 40)
        env.reset()
        attention = np.random.rand(20, 20) * 0.02
        env.visualize_attention([attention, None, None])
        time.sleep(2)
        env.visualize_attention([[[]], None, None])
        time.sleep(2)

    def test_suicide(self, env):
        print("=" * 40)
        states, infos = env.reset()
        action = MiniWoBTerminate()
        states, rewards, dones, truncs, infos = env.step([None, action, None])
        assert dones == [False, True, False]
        assert rewards[1] == -1


################################################


class TestMiniWoBSeed(MiniWoBTester):
    TASK_NAME = "click-button"

    def get_button_click(self, state):
        """Get the action that clicks the button."""
        for element in state.dom_elements:
            if element.tag == "button" and element.text == state.fields["target"]:
                action = MiniWoBElementClick(element, fail_hard=True)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(state.dom_elements)}")

    def test_seed(self, env):
        print("=" * 40)
        states, infos = env.reset(seed=0, options={"custom_seeds": [0, 1, 0]})
        print(states[0].dom.visualize())
        # Check that everything is the same for instances 0 and 2
        utt_0 = states[0].utterance
        utt_1 = states[1].utterance
        assert utt_0 == states[2].utterance != utt_1
        ref_to_text_0 = {x.ref: x.text for x in states[0].dom_elements}
        ref_to_text_1 = {x.ref: x.text for x in states[1].dom_elements}
        assert ref_to_text_0 == {x.ref: x.text for x in states[2].dom_elements}
        # Test clicking the correct buttons
        actions_button = [self.get_button_click(state) for state in states]
        states, rewards, dones, truncs, infos = env.step(actions_button)
        assert dones == [True, True, True]
        # Now run everything again but with shuffled seeds
        states, infos = env.reset(seed=0, options={"custom_seeds": [0, 0, 1]})
        assert states[0].utterance == states[1].utterance == utt_0
        assert states[2].utterance == utt_1
        assert ref_to_text_0 == {x.ref: x.text for x in states[0].dom_elements}
        assert ref_to_text_0 == {x.ref: x.text for x in states[1].dom_elements}
        assert ref_to_text_1 == {x.ref: x.text for x in states[2].dom_elements}
        # Test clicking with the old action objects
        actions_button = [actions_button[2], actions_button[0], actions_button[1]]
        states, rewards, dones, truncs, infos = env.step(actions_button)
        assert dones == [True, True, True]


class TestMiniWoBMode(MiniWoBTester):
    TASK_NAME = "click-test-transfer"

    def get_button_click(self, state, text):
        """Get the action that clicks the button."""
        for element in state.dom_elements:
            if element.tag == "button" and element.text == text:
                action = MiniWoBElementClick(element, fail_hard=True)
                print(f"Clicking with {action}")
                return action
        raise ValueError(f"Cannot find button: {str(state.dom_elements)}")

    def test_mode(self, env):
        """Test if setting the mode works.
        - mode = 'train': click on button ONE
        - mode = 'test':  click on button TWO
        """
        print("=" * 40)
        # Training time
        states, infos = env.reset()
        targets = ["ONE", "TWO", "ONE"]
        actions = []
        for state, target in zip(states, targets):
            assert state.utterance == "Click button ONE."
            actions.append(self.get_button_click(state, target))
        states, rewards, dones, truncs, infos = env.step(actions)
        assert dones == [True, True, True]
        assert rewards[0] > 0 and rewards[1] < 0 and rewards[2] > 0
        # Test time
        env.set_data_mode("test")
        states, infos = env.reset()
        actions = []
        for state, target in zip(states, targets):
            assert state.utterance == "Click button TWO."
            actions.append(self.get_button_click(state, target))
        states, rewards, dones, truncs, infos = env.step(actions)
        assert dones == [True, True, True]
        assert rewards[0] < 0 and rewards[1] > 0 and rewards[2] < 0
        # Test time again; mode should be persistent
        states, infos = env.reset()
        actions = []
        for state, target in zip(states, targets):
            assert state.utterance == "Click button TWO."
            actions.append(self.get_button_click(state, target))
        states, rewards, dones, truncs, infos = env.step(actions)
        assert dones == [True, True, True]
        assert rewards[0] < 0 and rewards[1] > 0 and rewards[2] < 0
        # Training time again: set mode with reset()
        states, infos = env.reset(options={"data_mode": "train"})
        actions = []
        for state, target in zip(states, targets):
            assert state.utterance == "Click button ONE."
            actions.append(self.get_button_click(state, target))
        states, rewards, dones, truncs, infos = env.step(actions)
        assert dones == [True, True, True]
        assert rewards[0] > 0 and rewards[1] < 0 and rewards[2] > 0


################################################


class TestMiniWoBFields(MiniWoBTester):
    TASK_NAME = "email-inbox-forward-nl"

    def test_fields(self, env):
        print("=" * 40)
        # Training time
        states, infos = env.reset()
        for state in states:
            print(state.utterance)
            print(state.fields)
            assert "by" in state.fields.keys
            assert "to" in state.fields.keys
            assert state.fields["by"] in state.utterance
            assert state.fields["to"] in state.utterance
        # Test time
        states, infos = env.reset(options={"data_mode": "test"})
        for state in states:
            print(state.utterance)
            print(state.fields)
            assert state.fields.keys == ["dummy"]
            assert state.utterance
        # Training time
        states, infos = env.reset(options={"data_mode": "train"})
        for state in states:
            print(state.utterance)
            print(state.fields)
            assert "by" in state.fields.keys
            assert "to" in state.fields.keys
            assert state.fields["by"] in state.utterance
            assert state.fields["to"] in state.utterance
