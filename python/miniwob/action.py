# MiniWoB actions
import abc
import logging

from selenium.webdriver.common.action_chains import ActionChains


class MiniWoBAction(object):
    """Defines an action in its __call__ method."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __call__(self, driver):
        """Performs the action defined by this class on the driver.

        Args:
            driver (Selenium WebDriver)
        """
        raise NotImplementedError()

    def to_dict(self):
        """Dict representation for JSON serialization."""
        raise NotImplementedError()


class MiniWoBTerminate(MiniWoBAction):
    """Immediately fails the task.

    This is done via a JavaScript call.
    """
    def __call__(self, driver):
        driver.execute_script('return core.endEpisode(-1,false,"terminate");')

    def __str__(self):
        return "MiniWoBTerminate"
    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, MiniWoBTerminate)

    def __hash__(self):
        return hash(self.__class__.__name__)

    def to_dict(self):
        return {'type': 'Terminate'}


class MiniWoBCoordClick(MiniWoBAction):
    """Defines a click action left pixels from the left of the screen and top
    pixels from the top of the screen.

    This is done via Selenium.

    Args:
        left (int): number of pixels from the left of the screen
        top (int): number of pixels from the top of the screen
    """
    def __init__(self, left, top):
        self._left = left
        self._top = top

    def __call__(self, driver):
        """Clicks at coordinates (left, top)"""
        body = driver.find_element_by_tag_name('body')
        chain = ActionChains(driver)
        chain.move_to_element_with_offset(
                body, self.left, self.top).click().perform()

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    def __str__(self):
        return "CoordClick(coords: ({}, {}))".format(self.left, self.top)
    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, MiniWoBCoordClick):
            return False
        return (self.left, self.top) == (other.left, other.top)

    def __hash__(self):
        return hash((self.__class__.__name__, self.left, self.top))

    def to_dict(self):
        return {'type': 'CoordClick', 'left': self._left, 'top': self._top}


class MiniWoBElementClick(MiniWoBAction):
    """An action that clicks on a DOM element regardless of its position
    or visibility.

    This is done via a JavaScript call.

    Args:
        element: One of the following:
            - the DOMElement object to click
            - ref (int) of the DOMElement object to click
        fail_hard (bool): If True, throw an error when the click cannot
            be successfully performed
    """
    def __init__(self, element, fail_hard=False):
        self._element = element
        self._ref = element.ref
        if self._ref is None:
            raise RuntimeError(
                    'Cannot click on {} with _ref = None'.format(element))
        self._fail_hard = fail_hard

    def __call__(self, driver):
        if self.element.tag == 'select':
            # SPECIAL CASE: <select>
            body = driver.find_element_by_tag_name('body')
            chain = ActionChains(driver)
            chain.move_to_element_with_offset(
                    body, self.element.left + 5,
                    self.element.top + 5).click().perform()
            return
        result = driver.execute_script(
                'return core.elementClick({});'.format(self._ref))
        if result is not True:
            if self._fail_hard:
                raise RuntimeError('{} failed: {}'.format(self, result))
            else:
                logging.warn('%s failed: %s', self, result)

    @property
    def ref(self):
        return self._ref

    @property
    def element(self):
        return self._element

    def __str__(self):
        return "click({})".format(self.element)
    __repr__ = __str__

    def __eq__(self, other):
        """Compare based on element refs."""
        if not isinstance(other, MiniWoBElementClick):
            return False
        return (self.ref, self._fail_hard) == (other.ref, other._fail_hard)

    def __hash__(self):
        return hash((self.__class__.__name__, self.ref, self._fail_hard))

    def to_dict(self):
        return {
            'type': 'ElementClick',
            'element': self.element.to_dict(),
            }


class MiniWoBType(MiniWoBAction):
    """An action that sends keystrokes to the focused element.

    This is done via Selenium.

    Args:
        text (str or list[str]): Things to type.
            Non-printable characters defined in
            selenium.webdriver.common.keys.Keys can also be used to send
            special keys (arrows, backspace, etc.)
    """
    def __init__(self, text):
        self._text = text

    def __call__(self, driver):
        chain = ActionChains(driver)
        chain.send_keys(self._text)
        chain.perform()

    @property
    def text(self):
        return self._text

    def __str__(self):
        return "Type({})".format(repr(self._text))
    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, MiniWoBType):
            return False
        return self.text == other.text

    def __hash__(self):
        return hash((self.__class__.__name__, self.text))

    def to_dict(self):
        return {'type': 'Type', 'text': self.text}


class MiniWoBFocusAndType(MiniWoBAction):
    """An action that first performs an element click to focus an element,
    followed by sending keystrokes.

    Implemented by executing a MiniWoBElementClick followed by MiniWoBType.

    Args:
        element: One of the following:
            - the DOMElement object to click
            - ref (int) of the DOMElement object to click
        text (str or list[str]): Things to type.
    """
    def __init__(self, element, text):
        self._click = MiniWoBElementClick(element)
        self._type = MiniWoBType(text)

    def __call__(self, driver):
        self._click(driver)
        self._type(driver)

    @property
    def ref(self):
        return self._click.ref

    @property
    def element(self):
        return self._click.element

    @property
    def text(self):
        return self._type.text

    def __str__(self):
        return "type({}, {})".format(self._click.element, repr(self._type.text))
    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, MiniWoBFocusAndType):
            return False
        return (self._click, self._type) == (other._click, other._type)

    def __hash__(self):
        return hash((self._click, self._type))

    def to_dict(self):
        return {
            'type': 'ElementClick',
            'element': self.element.to_dict(),
            'text': self.text,
            }
