"""Test action execution."""
from typing import Mapping, Tuple

import pytest

from miniwob.action import (
    create_coord_click_action,
    create_element_click_action,
    create_focus_and_type_action,
    create_type_action,
)
from miniwob.environment import MiniWoBEnvironment


class RepeatedTester:
    """Base class for repeated testing on a single task."""

    # Task name; subclasses should set this field
    TASK_NAME = ""
    # Number of times to run the test
    N = 10
    # Maximum number of steps for each episode
    MAX_STEPS = 1
    # Fragile tasks need longer wait time and single instance
    FRAGILE = False

    @pytest.fixture
    def env(self):
        """Yield an environment for the task."""
        if self.FRAGILE:
            env = MiniWoBEnvironment(subdomain=self.TASK_NAME, wait_ms=300)
        else:
            env = MiniWoBEnvironment(subdomain=self.TASK_NAME)
        yield env
        env.close()

    def test_run(self, env):
        """Run the test N times on the environment."""
        for i in range(self.N):
            print(f"Iteration {i + 1} / {self.N}")
            obs, info = env.reset()
            reward = -1
            for step in range(self.MAX_STEPS):
                action = self._get_action(obs, info, step)
                obs, reward, terminated, _, _ = env.step(action)
                assert reward >= 0
                if terminated:
                    break
            else:
                assert False, f"Number of steps exceeded {self.MAX_STEPS}"
            assert reward >= 0

    def _get_action(self, obs, info, step):
        """Return a MiniWoBAction that clicks the right thing."""
        raise NotImplementedError

    def click_button(self, obs, text):
        """Create an action that clicks on the button with the specified text."""
        for element in obs["dom_elements"]:
            if element["tag"] == "button" and element["text"] == text:
                return create_element_click_action(element["ref"])
        assert False, "Submit button not found"

    def create_coord_click_action(self, element):
        """Create an action that clicks on the element using CoordClick."""
        left, top = element["pos"].tolist()
        width, height = element["size"].tolist()
        action = create_coord_click_action(left + (width / 2), top + (height / 2))
        return action


################################################
# Test suites for tasks that involve a single click


class TestClickTest2(RepeatedTester):
    """Tests for task click-test-2."""

    TASK_NAME = "click-test-2"

    def _get_action(self, obs, info, step):
        for element in obs["dom_elements"]:
            if element["tag"] == "button" and element["text"] == "ONE":
                return create_element_click_action(element["ref"])
        # No button is found, which is weird
        assert False, 'Button "ONE" not found'


class TestClickButton(RepeatedTester):
    """Tests for task click-button."""

    TASK_NAME = "click-button"

    def _get_action(self, obs, info, step):
        target = info["fields"]["target"]
        for element in obs["dom_elements"]:
            if element["tag"] == "button" and element["text"] == target:
                return self.create_coord_click_action(element)
        # No button is found, which is weird
        assert False, f'Button "{target}" not found'


class TestFocusText(RepeatedTester):
    """Tests for task focus-text."""

    TASK_NAME = "focus-text"

    def _get_action(self, obs, info, step):
        for element in obs["dom_elements"]:
            if element["tag"] == "input_text":
                return self.create_coord_click_action(element)
        # No input is found, which is weird
        assert False, "Input box not found"


class TestIdentifyShape(RepeatedTester):
    """Tests for task identify-shape."""

    TASK_NAME = "identify-shape"

    def _get_action(self, obs, info, step):
        shape = self._identify_shape(obs)
        for element in obs["dom_elements"]:
            if element["tag"] == "button" and element["text"] == shape:
                return create_element_click_action(element["ref"])
        # No button is found, which is weird
        assert False, f'Button "{shape}" not found'

    def _identify_shape(self, obs):
        for element in obs["dom_elements"]:
            if element["tag"] == "svg":
                child = [
                    x for x in obs["dom_elements"] if x["parent"] == element["ref"]
                ][0]
                if child["tag"] == "circle":
                    return "Circle"
                elif child["tag"] == "text":
                    if child["text"].isdigit():
                        return "Number"
                    else:
                        return "Letter"
                elif child["tag"] == "rect":
                    return "Rectangle"
                elif child["tag"] == "polygon":
                    return "Triangle"


class TestClickDialog2(RepeatedTester):
    """Tests for task click-dialog-2."""

    TASK_NAME = "click-dialog-2"

    def _get_action(self, obs, info, step):
        target = info["fields"]["target"]
        if target == "x":
            target = ""
        for element in obs["dom_elements"]:
            if element["tag"] == "button" and element["text"] == target:
                return create_element_click_action(element["ref"])
        # No button is found, which is weird
        assert False, f'Button "{target}" not found'


################################################################################
# Test suites for more advanced tasks


class TestEnterText(RepeatedTester):
    """Tests for task enter-text."""

    TASK_NAME = "enter-text"
    MAX_STEPS = 3

    def _get_action(self, obs, info, step):
        if step == 0:
            # Click on the textbox
            for element in obs["dom_elements"]:
                if element["tag"] == "input_text":
                    assert not element["flags"][0].item()
                    return create_element_click_action(element["ref"])
            assert False, "Input text not found"
        elif step == 1:
            # Assert that the input is focused
            for element in obs["dom_elements"]:
                if element["tag"] == "input_text":
                    assert element["flags"][0].item()
                    break
            else:
                assert False, "Input text not found"
            # Type the text
            target = info["fields"]["target"]
            if len(target) > 2:
                # Hmm... Let's try the LEFT arrow key
                target = target[:-2] + target[-1] + "\ue012" + target[-2]
            return create_type_action(target)
        elif step == 2:
            # Click submit
            return self.click_button(obs, "Submit")


class TestEnterTextFocusAndType(RepeatedTester):
    """Tests for task enter-text, using FocusAndType actions."""

    TASK_NAME = "enter-text"
    MAX_STEPS = 2

    def _get_action(self, obs, info, step):
        if step == 0:
            # Type into the textbox
            target = info["fields"]["target"]
            for element in obs["dom_elements"]:
                if element["tag"] == "input_text":
                    return create_focus_and_type_action(element["ref"], target)
            assert False, "Input text not found"
        elif step == 1:
            # Click submit
            return self.click_button(obs, "Submit")


class TestClickCheckboxes(RepeatedTester):
    """Tests for task click-checkboxes."""

    TASK_NAME = "click-checkboxes"
    MAX_STEPS = 7

    def _get_action(self, obs, info, step):
        if not obs:
            return
        # print obs.dom.visualize()
        things_to_click = [
            info["fields"][key] for key in info["fields"].keys if key != "button"
        ]
        for element in obs["dom_elements"]:
            if element["tag"] == "label":
                checkbox, text = (
                    x for x in obs["dom_elements"] if x["parent"] == element["ref"]
                )
                if checkbox["value"]:
                    things_to_click.remove(text["text"])
                    continue
                elif text["text"] in things_to_click:
                    # Click on <label>:
                    return create_element_click_action(element["ref"])
        # Click the submit button
        assert not things_to_click
        return self.click_button(obs, "Submit")


class TestChooseDateEasy(RepeatedTester):
    """Tests for task choose-date-easy."""

    TASK_NAME = "choose-date-easy"
    MAX_STEPS = 3
    FRAGILE = True

    def _get_action(self, obs, info, step):
        if step == 0:
            for element in obs["dom_elements"]:
                if element["tag"] == "input_text":
                    return create_element_click_action(element["ref"])
            assert False, "Input text not found"
        elif step == 1:
            target = info["fields"]["day"]
            for element in obs["dom_elements"]:
                if element["tag"] == "a" and element["text"] == target:
                    return create_element_click_action(element["ref"])
            assert False, f"Day {target} not found"
        elif step == 2:
            return self.click_button(obs, "Submit")


class TestUseAutocomplete(RepeatedTester):
    """Tests for task use-autocomplete."""

    TASK_NAME = "use-autocomplete"
    MAX_STEPS = 3
    FRAGILE = True

    def _check(self, element, fields):
        t = element["text"]
        if t is None:
            return False
        if "end" in fields.keys:
            return t.startswith(fields["start"]) and t.endswith(fields["end"])
        else:
            return t.startswith(fields["start"])

    def _get_action(self, obs, info, step):
        if step == 0:
            for element in obs["dom_elements"]:
                if element["tag"] == "input_text":
                    return create_focus_and_type_action(
                        element["ref"], info["fields"]["start"]
                    )
            assert False, "Input text not found"
        elif step == 1:
            # print obs.dom.visualize()
            for element in obs["dom_elements"]:
                if element["tag"] == "div" and self._check(element, info["fields"]):
                    return create_element_click_action(element["ref"])
            assert False, "Correct entry not found"
        elif step == 2:
            return self.click_button(obs, "Submit")


class TestUseAutocompleteNoDelay(RepeatedTester):
    """Tests for task use-autocomplete-nodelay."""

    TASK_NAME = "use-autocomplete-nodelay"
    MAX_STEPS = 3
    FRAGILE = "instance"

    def _check(self, element, fields):
        t = element["text"]
        if t is None:
            return False
        if "end" in fields.keys:
            return t.startswith(fields["start"]) and t.endswith(fields["end"])
        else:
            return t.startswith(fields["start"])

    def _get_action(self, obs, info, step):
        if step == 0:
            for element in obs["dom_elements"]:
                if element["tag"] == "input_text":
                    return create_focus_and_type_action(
                        element["ref"], info["fields"]["start"]
                    )
            assert False, "Input text not found"
        elif step == 1:
            # print obs.dom.visualize()
            for element in obs["dom_elements"]:
                if element["tag"] == "div" and self._check(element, info["fields"]):
                    return create_element_click_action(element["ref"])
            assert False, "Correct entry not found"
        elif step == 2:
            return self.click_button(obs, "Submit")


class TestClickColor(RepeatedTester):
    """Tests for task click-color."""

    TASK_NAME = "click-color"
    COLORS: Mapping[Tuple[int, int, int], str] = {
        (0, 0, 0): "black",
        (255, 0, 0): "red",
        (0, 255, 0): "lime",
        (0, 0, 255): "blue",
        (255, 255, 0): "yellow",
        (255, 0, 255): "magenta",
        (0, 255, 255): "cyan",
        (255, 255, 255): "white",
        (128, 128, 128): "grey",
        (128, 128, 0): "olive",
        (128, 0, 128): "purple",
        (255, 165, 0): "orange",
        (255, 192, 203): "pink",
    }

    def _get_action(self, obs, info, step):
        for element in obs["dom_elements"]:
            if "color" in element["classes"]:
                r, g, b, a = element["bg_color"].tolist()
                name = self.COLORS[int(r * 255), int(g * 255), int(b * 255)]
                if name == info["fields"]["target"]:
                    return create_element_click_action(element["ref"])
        assert False, "Correct entry not found"


class TestEnterTime(RepeatedTester):
    """Tests for task enter-time."""

    TASK_NAME = "enter-time"
    MAX_STEPS = 2

    def _get_action(self, obs, info, step):
        if step == 0:
            target = info["fields"]["target"]
            if target.startswith("1:"):
                target = "0" + target  # Typing '14' will change the number to 2
            for element in obs["dom_elements"]:
                if element["tag"] == "input_time":
                    return create_focus_and_type_action(element["ref"], target)
            assert False, "Input text not found"
        elif step == 1:
            return self.click_button(obs, "Submit")


class TestClickPie(RepeatedTester):
    """Tests for task click-pie-nodelay."""

    TASK_NAME = "click-pie-nodelay"
    MAX_STEPS = 2

    def _get_action(self, obs, info, step):
        if step == 0:
            path = None
            for element in obs["dom_elements"]:
                if element["tag"] == "path":
                    path = element
                elif element["text"] == "+":
                    assert path is not None
                    return create_element_click_action(path["ref"])
            assert False, "Select not found"
        elif step == 1:
            path = None
            for element in obs["dom_elements"]:
                if element["tag"] == "path":
                    path = element
                elif element["text"] == info["fields"]["target"]:
                    assert path is not None
                    return create_element_click_action(path["ref"])
            assert False, "Correct entry not found"
