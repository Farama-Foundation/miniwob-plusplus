"""Methods that execute actions in Selenium."""
import logging

from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.common.action_chains import ActionChains


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


def execute_click_element(ref: int, driver: ChromeDriver):
    """Click on the DOM element specified by a ref ID."""
    # TODO: Handle <select> correctly.
    result = driver.execute_script(f"return core.elementClick({ref});")
    if result is not True:
        logging.warning("Clicking %s failed: %s", ref, result)


def execute_type_text(text: str, driver: ChromeDriver):
    """Send keystrokes to the focused element."""
    chain = ActionChains(driver)
    chain.send_keys(text)
    chain.perform()


def execute_focus_element_and_type_text(ref: int, text: str, driver: ChromeDriver):
    """Click the specified DOM element and then send keystrokes."""
    execute_click_element(ref, driver)
    execute_type_text(text, driver)
