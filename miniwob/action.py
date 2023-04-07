"""MiniWoB action space."""
import logging
from enum import IntEnum
from typing import Any, Dict

import numpy as np
from gymnasium import spaces
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from miniwob.constants import ASCII_CHARSET, MAX_REF, TYPING_MAX_LENGTH

Action = Dict[str, Any]


class ActionTypes(IntEnum):
    """Valid action types for MiniWoB environments."""

    NONE = 0
    COORD_CLICK = 1
    ELEMENT_CLICK = 2
    TYPE = 3
    FOCUS_AND_TYPE = 4
    COORD_SCROLL = 5


def get_action_space(screen_width: int, screen_height: int) -> spaces.Space:
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
            "scroll_coords": spaces.Box(
                np.array([0.0, 0.0], dtype=np.float32),
                np.array([screen_width, screen_height], dtype=np.float32),
            )
        }
    )
    return space


def create_none_action() -> Action:
    """Return a valid action object that does nothing."""
    return {
        "action_type": ActionTypes.NONE,
        "coords": np.zeros(2, dtype=np.float32),
        "ref": 1,
        "text": " ",
        "scroll_coords": np.zeros(2, dtype=np.float32),
    }


def create_coord_click_action(left: float, top: float) -> Action:
    """Return a valid action object with type COORD_CLICK."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.COORD_CLICK,
            "coords": np.array([left, top], dtype=np.float32),
        }
    )
    return action


def create_element_click_action(ref: int) -> Action:
    """Return a valid action object with type ELEMENT_CLICK."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.ELEMENT_CLICK,
            "ref": ref,
        }
    )
    return action


def create_type_action(text: str) -> Action:
    """Return a valid action object with type TYPE."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.TYPE,
            "text": text,
        }
    )
    return action


def create_focus_and_type_action(ref: int, text: str) -> Action:
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


def create_coord_scroll_action(left: float, top: float, scroll_x: int, scroll_y: int) -> Action:
    """Return a valid action object with type COORD_SCROLL."""
    action = create_none_action()
    action.update(
        {
            "action_type": ActionTypes.COORD_SCROLL,
            "coords": np.array([left, top], dtype=np.float32),
            "scroll_coords": np.array([scroll_x, scroll_y], dtype=np.float32),
        }
    )
    return action


def execute_coord_click(left: float, top: float, driver: ChromeDriver):
    """Click at coordinates (left, top)."""
    body = driver.find_element(By.TAG_NAME, "body")
    # The offset is from the center, not top-left.
    x = -body.size["width"] / 2 + left
    y = -body.size["height"] / 2 + top
    # Added 0 duration to action chain to avoid waiting for the default 0.25s
    chain = ActionChains(driver, duration=0)
    chain.move_to_element_with_offset(body, x, y).click().perform()


def execute_element_click(ref: int, driver: ChromeDriver):
    """Click on the DOM element specified by a ref ID."""
    # TODO: Handle <select> correctly.
    result = driver.execute_script(f"return core.elementClick({ref});")
    if result is not True:
        logging.warning("Clicking %s failed: %s", ref, result)


def execute_type(text: str, driver: ChromeDriver):
    """Send keystrokes to the focused element."""
    chain = ActionChains(driver, duration=0)
    chain.send_keys(text)
    chain.perform()


def execute_focus_and_type(ref: int, text: str, driver: ChromeDriver):
    """Click the specified DOM element and then send keystrokes."""
    execute_element_click(ref, driver)
    execute_type(text, driver)


def execute_coord_scroll(left: float, top: float, scroll_x: int, scroll_y: int, driver: ChromeDriver):
    """Scroll at coordinates (left, top)."""
    x = left
    y = top
    chain = ActionChains(driver, duration=0)
    chain.scroll(int(x), int(y), scroll_x, scroll_y).perform()


def execute_action(action: Action, driver: ChromeDriver):
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
    elif action_type == ActionTypes.COORD_SCROLL:
        left = float(action["coords"][0])
        top = float(action["coords"][1])
        scroll_x = int(action["scroll_coords"][0])
        scroll_y = int(action["scroll_coords"][1])
        execute_coord_scroll(left, top, scroll_x, scroll_y, driver)
    else:
        raise ValueError(f"Unknown action type: {action_type}")
