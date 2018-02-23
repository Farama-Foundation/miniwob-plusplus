import os
import pytest
import time

from miniwob.environment import MiniWoBEnvironment
from miniwob.action import (
        MiniWoBCoordClick, MiniWoBElementClick, MiniWoBType, MiniWoBFocusAndType
        )


class RepeatedTester(object):
    # Task name; subclasses should set this field
    TASK_NAME = None
    # Number of times to run the test
    N = 20
    # Maximum number of steps for each episode
    MAX_STEPS = 1
    # Fragile tasks need longer wait time and single instance
    FRAGILE = False

    @pytest.fixture
    def env(self):
        env = MiniWoBEnvironment(self.TASK_NAME)
        base_url = os.environ.get('MINIWOB_BASE_URL')
        print 'BASE URL:', base_url
        if self.FRAGILE is True:
            env.configure(base_url=base_url,
                    num_instances=1, seeds=[1], wait_ms=300)
        elif self.FRAGILE == 'instance':
            env.configure(base_url=base_url,
                    num_instances=1, seeds=[1])
        elif self.FRAGILE == 'delay':
            env.configure(base_url=base_url,
                    num_instances=3, seeds=range(3), wait_ms=1000)
        else:
            env.configure(base_url=base_url,
                    num_instances=3, seeds=range(3))
        yield env
        env.close()

    def test_run(self, env):
        for i in xrange(self.N):
            print 'Iteration {} / {}'.format(i + 1, self.N)
            states = env.reset()
            for j, state in enumerate(states):
                print 'Fields {}: {}'.format(j, state.fields)
            for s in xrange(self.MAX_STEPS):
                print 'Step {} / {}'.format(s + 1, self.MAX_STEPS)
                actions = [self.get_action(x, s) for x in states]
                states, rewards, dones, info = env.step(actions)
                if all(x for x in dones):
                    break
                assert all(x >= 0 for x in rewards)
            else:
                assert False, 'Number of steps exceeded {}'.format(self.MAX_STEPS)
            assert all(x > 0 for x in rewards)

    def get_action(self, state, step):
        """Returns a MiniWoBAction that clicks the right thing."""
        raise NotImplementedError

    def create_element_click_action(self, element):
        action = MiniWoBElementClick(element, fail_hard=True)
        print 'Clicking with {}'.format(action)
        return action

    def click_button(self, state, text):
        """Create an action that clicks on the button with the specified text."""
        for element in state.dom_elements:
            if element.tag == 'button' and element.text == text:
                return self.create_element_click_action(element)
        assert False, 'Submit button not found'

    def create_coord_click_action(self, element):
        action = MiniWoBCoordClick(
                element.left + (element.width / 2),
                element.top + (element.height / 2))
        print 'Clicking with {}'.format(action)
        return action

    def create_type_action(self, text):
        action = MiniWoBType(text)
        print 'Typing with {}'.format(action)
        return action

    def create_focus_and_type_action(self, element, text):
        action = MiniWoBFocusAndType(element, text)
        print 'Focus and Type: {}'.format(action)
        return action


################################################
# Test suites for tasks that involve a single click

class TestClickTest2(RepeatedTester):
    TASK_NAME = 'click-test-2'

    def get_action(self, state, step):
        for element in state.dom_elements:
            if element.tag == 'button' and element.text == 'ONE':
                return self.create_element_click_action(element)
        # No button is found, which is weird
        assert False, 'Button "ONE" not found'


class TestClickButton(RepeatedTester):
    TASK_NAME = 'click-button'

    def get_action(self, state, step):
        target = state.fields['target']
        for element in state.dom_elements:
            if element.tag == 'button' and element.text == target:
                return self.create_coord_click_action(element)
        # No button is found, which is weird
        assert False, 'Button "{}" not found'.format(target)


class TestFocusText(RepeatedTester):
    TASK_NAME = 'focus-text'

    def get_action(self, state, step):
        for element in state.dom_elements:
            if element.tag == 'input_text':
                return self.create_coord_click_action(element)
        # No input is found, which is weird
        assert False, 'Input box not found'


class TestIdentifyShape(RepeatedTester):
    TASK_NAME = 'identify-shape'

    def get_action(self, state, step):
        shape = self._identify_shape(state)
        for element in state.dom_elements:
            if element.tag == 'button' and element.text == shape:
                return self.create_element_click_action(element)
        # No button is found, which is weird
        assert False, 'Button "{}" not found'.format(shape)

    def _identify_shape(self, state):
        for element in state.dom_elements:
            if element.tag == 'svg':
                child = element.children[0]
                print child
                if child.tag == 'circle':
                    return 'Circle'
                elif child.tag == 'text':
                    if child.text.isdigit():
                        return 'Number'
                    else:
                        return 'Letter'
                elif child.tag == 'rect':
                    return 'Rectangle'
                elif child.tag == 'polygon':
                    return 'Triangle'


class TestClickDialog2(RepeatedTester):
    TASK_NAME = 'click-dialog-2'

    def get_action(self, state, step):
        target = state.fields['target']
        if target == 'x':
            target = None
        for element in state.dom_elements:
            if element.tag == 'button' and element.text == target:
                return self.create_element_click_action(element)
        # No button is found, which is weird
        assert False, 'Button "{}" not found'.format(target)


################################################################################
# Test suites for more advanced tasks

class TestEnterText(RepeatedTester):
    TASK_NAME = 'enter-text'
    MAX_STEPS = 3

    def get_action(self, state, step):
        if step == 0:
            # Click on the textbox
            for element in state.dom_elements:
                if element.tag == 'input_text':
                    assert not element.focused
                    return self.create_element_click_action(element)
            assert False, 'Input text not found'
        elif step == 1:
            # Assert that the input is focused
            for element in state.dom_elements:
                if element.tag == 'input_text':
                    assert element.focused
                    break
            assert False, 'Input text not found'
            # Type the text
            target = state.fields['target']
            if len(target) > 2:
                # Hmm... Let's try the LEFT arrow key
                target = target[:-2] + target[-1] + u'\ue012' + target[-2]
            return self.create_type_action(target)
        elif step == 2:
            # Click submit
            return self.click_button(state, 'Submit')


class TestEnterTextFocusAndType(RepeatedTester):
    TASK_NAME = 'enter-text'
    MAX_STEPS = 2

    def get_action(self, state, step):
        if step == 0:
            # Type into the textbox
            target = state.fields['target']
            for element in state.dom_elements:
                if element.tag == 'input_text':
                    return self.create_focus_and_type_action(element, target)
            assert False, 'Input text not found'
        elif step == 1:
            # Click submit
            return self.click_button(state, 'Submit')


class TestClickCheckboxes(RepeatedTester):
    TASK_NAME = 'click-checkboxes'
    MAX_STEPS = 7

    def get_action(self, state, step):
        if not state:
            return
        #print state.dom.visualize()
        things_to_click = [state.fields[key]
                for key in state.fields.keys if key != 'button']
        for element in state.dom_elements:
            if element.tag == 'label':
                checkbox, text = element.children
                if checkbox.value:
                    things_to_click.remove(text.text)
                    continue
                elif text.text in things_to_click:
                    # Click on <input>:
                    #return self.create_element_click_action(checkbox)
                    # Click on <label>:
                    return self.create_element_click_action(element)
        # Click the submit button
        assert not things_to_click
        return self.click_button(state, 'Submit')


class TestChooseDateEasy(RepeatedTester):
    TASK_NAME = 'choose-date-easy'
    MAX_STEPS = 3
    FRAGILE = True

    def get_action(self, state, step):
        if step == 0:
            for element in state.dom_elements:
                if element.tag == 'input_text':
                    return self.create_element_click_action(element)
            assert False, 'Input text not found'
        elif step == 1:
            target = state.fields['day']
            for element in state.dom_elements:
                if element.tag == 'a' and element.text == target:
                    return self.create_element_click_action(element)
            assert False, 'Day {} not found'.format(target)
        elif step == 2:
            return self.click_button(state, 'Submit')


class TestUseAutocomplete(RepeatedTester):
    TASK_NAME = 'use-autocomplete'
    MAX_STEPS = 3
    FRAGILE = True

    def check(self, element, fields):
        t = element.text
        if t is None:
            return False
        if 'end' in fields.keys:
            return t.startswith(fields['start']) and t.endswith(fields['end'])
        else:
            return t.startswith(fields['start'])

    def get_action(self, state, step):
        if step == 0:
            for element in state.dom_elements:
                if element.tag == 'input_text':
                    return self.create_focus_and_type_action(element, state.fields['start'])
            assert False, 'Input text not found'
        elif step == 1:
            #print state.dom.visualize()
            for element in state.dom_elements:
                if element.tag == 'div' and self.check(element, state.fields):
                    return self.create_element_click_action(element)
            assert False, 'Correct entry not found'
        elif step == 2:
            return self.click_button(state, 'Submit')


class TestUseAutocompleteNoDelay(RepeatedTester):
    TASK_NAME = 'use-autocomplete-nodelay'
    MAX_STEPS = 3
    FRAGILE = 'instance'

    def check(self, element, fields):
        t = element.text
        if t is None:
            return False
        if 'end' in fields.keys:
            return t.startswith(fields['start']) and t.endswith(fields['end'])
        else:
            return t.startswith(fields['start'])

    def get_action(self, state, step):
        if step == 0:
            for element in state.dom_elements:
                if element.tag == 'input_text':
                    return self.create_focus_and_type_action(element, state.fields['start'])
            assert False, 'Input text not found'
        elif step == 1:
            #print state.dom.visualize()
            for element in state.dom_elements:
                if element.tag == 'div' and self.check(element, state.fields):
                    return self.create_element_click_action(element)
            assert False, 'Correct entry not found'
        elif step == 2:
            return self.click_button(state, 'Submit')


class TestClickColor(RepeatedTester):
    TASK_NAME = 'click-color'
    COLORS = {
            (0, 0, 0): 'black',
            (255, 0, 0): 'red',
            (0, 255, 0): 'lime',
            (0, 0, 255): 'blue',
            (255, 255, 0): 'yellow',
            (255, 0, 255): 'magenta',
            (0, 255, 255): 'cyan',
            (255, 255, 255): 'white',
            (128, 128, 128): 'grey',
            (128, 128, 0): 'olive',
            (128, 0, 128): 'purple',
            (255, 165, 0): 'orange',
            (255, 192, 203): 'pink',
            }

    def get_action(self, state, step):
        for element in state.dom_elements:
            if 'color' in element.classes:
                r, g, b, a = element.bg_color
                name = self.COLORS[int(r*255), int(g*255), int(b*255)]
                if name == state.fields['target']:
                    return self.create_element_click_action(element)
        assert False, 'Correct entry not found'


class TestEnterTime(RepeatedTester):
    TASK_NAME = 'enter-time'
    MAX_STEPS = 2

    def get_action(self, state, step):
        if step == 0:
            for element in state.dom_elements:
                if element.tag == 'input_time':
                    return self.create_focus_and_type_action(element, state.fields['target'])
            assert False, 'Input text not found'
        elif step == 1:
            return self.click_button(state, 'Submit')


class TestChooseList(RepeatedTester):
    TASK_NAME = 'choose-list'
    MAX_STEPS = 3
    FRAGILE = 'delay'

    def get_action(self, state, step):
        if step == 0:
            for element in state.dom_elements:
                if element.tag == 'select':
                    return self.create_element_click_action(element)
            assert False, 'Select not found'
        elif step == 1:
            print state.dom.visualize()
            for element in state.dom_elements:
                if element.text == state.fields['target']:
                    return self.create_element_click_action(element)
            assert False, 'Correct entry not found'
        elif step == 2:
            return self.click_button(state, 'Submit')


class TestClickPie(RepeatedTester):
    TASK_NAME = 'click-pie-nodelay'
    MAX_STEPS = 2

    def get_action(self, state, step):
        print state.dom.visualize()
        if step == 0:
            path = None
            for element in state.dom_elements:
                if element.tag == 'path':
                    path = element
                elif element.text == '+':
                    return self.create_element_click_action(path)
            assert False, 'Select not found'
        elif step == 1:
            print state.dom.visualize()
            path = None
            for element in state.dom_elements:
                if element.tag == 'path':
                    path = element
                elif element.text == state.fields['target']:
                    return self.create_element_click_action(path)
            assert False, 'Correct entry not found'
