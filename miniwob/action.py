"""MiniWoB action space."""
import logging
from enum import IntEnum

import numpy as np
from gymnasium import spaces
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class ActionTypes(IntEnum):
    NONE = 0
    COORD_CLICK = 1
    ELEMENT_CLICK = 2
    TYPE = 3
    FOCUS_AND_TYPE = 4


TYPING_MAX_LENGTH = 32
ASCII_CHARSET = frozenset(chr(x) for x in range(32, 128))
MAX_REF = 1000000


def get_action_space(screen_width, screen_height):
    """Return the space of serialized actions."""
    space = spaces.Dict(
        {
            "action_type": spaces.Discrete(len(ActionTypes)),
            # coords (left, top) is used for COORD_CLICK
            "coords": spaces.Box(
                np.array([0.0, 0.0], dtype=np.float32),
                np.array([screen_width, screen_height], dtype=np.float32),
            ),
            # ref (element ref ID) is used for ELEMENT_CLICK and FOCUS_AND_TYPE
            "ref": spaces.Discrete(MAX_REF, start=1),
            # text is only used for TYPE and FOCUS_AND_TYPE
            "text": spaces.Text(TYPING_MAX_LENGTH, charset=ASCII_CHARSET),
        }
    )
    return space


def create_none_action():
    """Return a valid action object that does nothing."""
    return {
        "action_type": ActionTypes.NONE,
        "coords": np.zeros(2, dtype=np.float32),
        "ref": 1,
        "text": " ",
    }


def create_coord_click_action(left, top):
    """Return a valid action object with type COORD_CLICK."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.COORD_CLICK,
            "coords": np.array([left, top], dtype=np.float32),
        }
    )
    return action


def create_element_click_action(ref):
    """Return a valid action object with type ELEMENT_CLICK."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.ELEMENT_CLICK,
            "ref": ref,
        }
    )
    return action


def create_type_action(text):
    """Return a valid action object with type TYPE."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.TYPE,
            "text": text,
        }
    )
    return action


def create_focus_and_type_action(ref, text):
    """Return a valid action object with type FOCUS_AND_TYPE."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.FOCUS_AND_TYPE,
            "ref": ref,
            "text": text,
        }
    )
    return action


def execute_coord_click(left, top, driver):
    """Click at coordinates (left, top)."""
    body = driver.find_element(By.TAG_NAME, "body")
    # The offset is from the center, not top-left.
    x = -body.size["width"] / 2 + left
    y = -body.size["height"] / 2 + top
    chain = ActionChains(driver)
    chain.move_to_element_with_offset(body, x, y).click().perform()


def execute_element_click(ref, driver):
    """Click on the DOM element specified by a ref ID."""
    # TODO: Handle <select> correctly.
    result = driver.execute_script(f"return core.elementClick({ref});")
    if result is not True:
        logging.warning("Clicking %s failed: %s", ref, result)


def execute_type(text, driver):
    """Send keystrokes to the focused element."""
    chain = ActionChains(driver)
    chain.send_keys(text)
    chain.perform()


def execute_focus_and_type(ref, text, driver):
    """Click the specified DOM element and then send keystrokes."""
    execute_element_click(ref, driver)
    execute_type(text, driver)


def execute_action(action, driver):
    """Execute the action on the ChromeDriver."""
    action_type = action["action_type"]
    if action_type == ActionTypes.NONE:
        pass
    elif action_type == ActionTypes.COORD_CLICK:
        left = float(action["coords"][0])
        top = float(action["coords"][1])
        execute_coord_click(left, top, driver)
    elif action_type == ActionTypes.ELEMENT_CLICK:
        ref = int(action["ref"])
        execute_element_click(ref, driver)
    elif action_type == ActionTypes.TYPE:
        text = action["text"]
        execute_type(text, driver)
    elif action_type == ActionTypes.FOCUS_AND_TYPE:
        ref = int(action["ref"])
        text = action["text"]
        execute_focus_and_type(ref, text, driver)
    else:
        raise ValueError(f"Unknown action type: {action_type}")
