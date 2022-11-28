# MiniWoB actions
import abc
import logging
from enum import IntEnum

from gymnasium import spaces
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class MiniWoBAction(metaclass=abc.ABCMeta):
    """Defines an action in its __call__ method."""

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


class MiniWoBNoOp(MiniWoBAction):
    """Do nothing."""

    def __call__(self, driver):
        pass

    def __str__(self):
        return "MiniWoBNoOp"

    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, MiniWoBNoOp)

    def __hash__(self):
        return hash(self.__class__.__name__)

    def to_dict(self):
        return {"type": "NoOp"}


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
        return {"type": "Terminate"}


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
        body = driver.find_element(By.TAG_NAME, "body")
        # The offset is from the center, not top-left.
        x = -body.size["width"] / 2 + self.left
        y = -body.size["height"] / 2 + self.top
        chain = ActionChains(driver)
        chain.move_to_element_with_offset(body, x, y).click().perform()

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    def __str__(self):
        return f"CoordClick(coords: ({self.left}, {self.top}))"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, MiniWoBCoordClick):
            return False
        return (self.left, self.top) == (other.left, other.top)

    def __hash__(self):
        return hash((self.__class__.__name__, self.left, self.top))

    def to_dict(self):
        return {"type": "CoordClick", "left": self._left, "top": self._top}


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
        if isinstance(element, int):
            self._ref = element
        else:
            self._ref = element._ref
            if self._ref is None:
                raise RuntimeError(f"Cannot click on {element} with _ref = None")
        self._fail_hard = fail_hard

    def __call__(self, driver):
        # TODO: Handle <select> correctly.
        # if self.element.tag == "select":
        #     # SPECIAL CASE: <select>
        #     body = driver.find_element(By.TAG_NAME, "body")
        #     chain = ActionChains(driver)
        #     chain.move_to_element_with_offset(
        #         body, self.element.left + 5, self.element.top + 5
        #     ).click().perform()
        #     return
        result = driver.execute_script(f"return core.elementClick({self._ref});")
        if result is not True:
            if self._fail_hard:
                raise RuntimeError(f"{self} failed: {result}")
            else:
                logging.warning("%s failed: %s", self, result)

    @property
    def ref(self):
        return self._ref

    def __str__(self):
        return f"click({self.ref})"

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
            "type": "ElementClick",
            "element": self.ref,
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
        return f"Type({repr(self._text)})"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, MiniWoBType):
            return False
        return self.text == other.text

    def __hash__(self):
        return hash((self.__class__.__name__, self.text))

    def to_dict(self):
        return {"type": "Type", "text": self.text}


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
    def text(self):
        return self._type.text

    def __str__(self):
        return f"type({self.ref}, {repr(self.text)})"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, MiniWoBFocusAndType):
            return False
        return (self._click, self._type) == (other._click, other._type)

    def __hash__(self):
        return hash((self._click, self._type))

    def to_dict(self):
        return {
            "type": "ElementClick",
            "element": self.ref,
            "text": self.text,
        }


################################################
# Serialized actions for Gymnasium


class ActionTypes(IntEnum):
    NONE = 0
    COORD_CLICK = 1
    ELEMENT_CLICK = 2
    TYPE = 3
    FOCUS_AND_TYPE = 4


ASCII_CHARSET = frozenset(chr(x) for x in range(32, 128))


def get_action_space(
    screen_height, screen_width, typing_max_length=32, typing_charset=ASCII_CHARSET
):
    """Return the space of serialized actions."""
    space = spaces.Dict(
        {
            "action_type": spaces.Discrete(len(ActionTypes)),
            # clicked_top and clicked_left are only used for COORD_CLICK
            "clicked_top": spaces.Box(0.0, screen_height, dtype=float),
            "clicked_left": spaces.Box(0.0, screen_width, dtype=float),
            # clicked_element is only used for ELEMENT_CLICK and FOCUS_AND_TYPE
            "clicked_element": spaces.Box(1, float("inf"), dtype=int),
            # typed_text is only used for TYPE and FOCUS_AND_TYPE
            "typed_text": spaces.Text(typing_max_length, charset=typing_charset),
        }
    )
    return space


def to_action_object(action):
    """Converts the serialized action into a MiniWoBAction object."""
    if isinstance(action, MiniWoBAction):
        # Already a MiniWoBAction
        return action
    action_type = action["action_type"]
    if action_type == ActionTypes.NONE:
        return MiniWoBNoOp()
    elif action_type == ActionTypes.COORD_CLICK:
        top = float(action["clicked_top"])
        left = float(action["clicked_left"])
        return MiniWoBCoordClick(top=top, left=left)
    elif action_type == ActionTypes.ELEMENT_CLICK:
        ref = int(action["clicked_element"])
        return MiniWoBElementClick(ref)
    elif action_type == ActionTypes.TYPE:
        text = action["typed_text"]
        return MiniWoBType(text)
    elif action_type == ActionTypes.FOCUS_AND_TYPE:
        ref = int(action["clicked_element"])
        text = action["typed_text"]
        return MiniWoBFocusAndType(ref, text)
    else:
        raise ValueError(f"Unknown action type: {action_type}")
