"""Methods that execute actions in Selenium."""
import logging
from typing import Sequence, Tuple

from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.common.action_chains import ActionChains

from miniwob.action import (
    COORDS_ACTIONS,
    ELEMENT_ACTIONS,
    FIELD_ACTIONS,
    SCROLL_ACTIONS,
    TEXT_ACTIONS,
    Action,
    ActionSpaceConfig,
    ActionTypes,
)
from miniwob.constants import WEBDRIVER_MODIFIER_KEYS, WEBDRIVER_SPECIAL_KEYS


def _get_move_coords_action_chains(left: float, top: float, driver: ChromeDriver):
    """Returns an ActionChains object that queues up a coordinate move action."""
    chain = ActionChains(driver, duration=0)
    chain.w3c_actions.pointer_action.move_to_location(left, top)
    return chain


def execute_move_coords(left: float, top: float, driver: ChromeDriver):
    """Move to coordinates (left, top)."""
    chain = _get_move_coords_action_chains(left, top, driver)
    chain.w3c_actions.perform()


def execute_click_coords(left: float, top: float, driver: ChromeDriver):
    """Click at coordinates (left, top)."""
    chain = _get_move_coords_action_chains(left, top, driver)
    chain.w3c_actions.pointer_action.click()
    chain.w3c_actions.perform()


def execute_dblclick_coords(left: float, top: float, driver: ChromeDriver):
    """Double-click at coordinates (left, top)."""
    chain = _get_move_coords_action_chains(left, top, driver)
    chain.w3c_actions.pointer_action.double_click()
    chain.w3c_actions.perform()


def execute_mousedown_coords(left: float, top: float, driver: ChromeDriver):
    """Move to coordinates (left, top) then start dragging."""
    chain = _get_move_coords_action_chains(left, top, driver)
    chain.w3c_actions.pointer_action.click_and_hold()
    chain.w3c_actions.perform()


def execute_mouseup_coords(left: float, top: float, driver: ChromeDriver):
    """Move to coordinates (left, top) then stop dragging."""
    chain = _get_move_coords_action_chains(left, top, driver)
    chain.w3c_actions.pointer_action.release()
    chain.w3c_actions.perform()


def execute_scroll_coords(
    left: float,
    top: float,
    scroll_amount: int,
    scroll_time: int,
    driver: ChromeDriver,
):
    """Use the scroll wheel to scroll at coordinates (left, top)."""
    chain = ActionChains(driver)
    chain.w3c_actions.wheel_action.scroll(
        x=int(left),
        y=int(top),
        delta_y=scroll_amount,
        duration=scroll_time,
    )
    chain.w3c_actions.perform()


def execute_click_element(ref: int, driver: ChromeDriver):
    """Click on the DOM element specified by a ref ID."""
    result = driver.execute_script(f"return core.elementClick({ref});")
    if result is not True:
        logging.warning("Clicking %s failed: %s", ref, result)


def execute_press_key(key: str, driver: ChromeDriver):
    """Press the key or key combination.

    The syntax for `key` is as follows:
    - Modifiers are specified using prefixes "C-" (control), "S-" (shift),
        "A-" (alternate), or "M-" (meta).
    - Printable character keys (a, 1, etc.) are specified directly.
        Shifted characters (A, !, etc.) will cause shift to be pressed.
    - Special keys are inclosed in "<...>"; see the list in constants.py.

    Args:
        key: Key or key combination.
        driver: ChromeDriver object.
    """
    raw_key = key
    modifiers = []
    while raw_key[:2] in WEBDRIVER_MODIFIER_KEYS:
        modifiers.append(WEBDRIVER_MODIFIER_KEYS[raw_key[:2]])
        raw_key = raw_key[2:]
    if raw_key in WEBDRIVER_SPECIAL_KEYS:
        raw_key = WEBDRIVER_SPECIAL_KEYS[raw_key]
    if len(raw_key) != 1:
        logging.warning("Invalid key %s (raw: %s)", repr(key), repr(raw_key))
    chain = ActionChains(driver, duration=0)
    for modifier in modifiers:
        chain.w3c_actions.key_action.key_down(modifier)
    chain.w3c_actions.key_action.key_down(raw_key)
    chain.w3c_actions.key_action.key_up(raw_key)
    for modifier in reversed(modifiers):
        chain.w3c_actions.key_action.key_up(modifier)
    chain.perform()


def execute_type_text(text: str, driver: ChromeDriver):
    """Send keystrokes to the focused element."""
    chain = ActionChains(driver, duration=0)
    for key in text:
        chain.w3c_actions.key_action.key_down(key)
        chain.w3c_actions.key_action.key_up(key)
    chain.perform()


_SELENIUM_COORDS_ACTIONS = {
    ActionTypes.MOVE_COORDS: execute_move_coords,
    ActionTypes.CLICK_COORDS: execute_click_coords,
    ActionTypes.DBLCLICK_COORDS: execute_dblclick_coords,
    ActionTypes.MOUSEDOWN_COORDS: execute_mousedown_coords,
    ActionTypes.MOUSEUP_COORDS: execute_mouseup_coords,
}


def execute_action_on_chromedriver(
    action: Action,
    fields: Sequence[Tuple[str, str]],
    config: ActionSpaceConfig,
    driver: ChromeDriver,
):
    """Execute the action on the ChromeDriver."""
    action_type = config.action_types[action["action_type"]]
    if action_type == ActionTypes.NONE:
        return
    # Coords actions
    if action_type in COORDS_ACTIONS:
        left, top = config.compute_raw_coords(action)
        if action_type in SCROLL_ACTIONS:
            scroll_amount = config.scroll_amount
            if action_type == ActionTypes.SCROLL_UP_COORDS:
                scroll_amount = -scroll_amount
            execute_scroll_coords(left, top, scroll_amount, config.scroll_time, driver)
        else:
            _SELENIUM_COORDS_ACTIONS[action_type](left, top, driver)
        return
    # Key press action
    if action_type == ActionTypes.PRESS_KEY:
        key_idx = int(action["key"])
        key = config.allowed_keys[key_idx]
        execute_press_key(key, driver)
        return
    # Element and typing actions
    if action_type in ELEMENT_ACTIONS:
        ref = int(action["ref"])
        execute_click_element(ref, driver)
    if action_type in TEXT_ACTIONS:
        text = action["text"]
        execute_type_text(text, driver)
    elif action_type in FIELD_ACTIONS:
        field_idx = int(action["field"])
        if field_idx >= len(fields):
            # Treat the value as empty
            text = ""
        else:
            text = fields[field_idx][1]
        execute_type_text(text, driver)
