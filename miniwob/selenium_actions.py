"""Methods that execute actions in Selenium."""
import logging

from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def execute_coord_click(left: float, top: float, driver: ChromeDriver):
    """Click at coordinates (left, top)."""
    body = driver.find_element(By.TAG_NAME, "body")
    # The offset is from the center, not top-left.
    x = -body.size["width"] / 2 + left
    y = -body.size["height"] / 2 + top
    chain = ActionChains(driver)
    chain.move_to_element_with_offset(body, x, y).click().perform()


def execute_element_click(ref: int, driver: ChromeDriver):
    """Click on the DOM element specified by a ref ID."""
    # TODO: Handle <select> correctly.
    result = driver.execute_script(f"return core.elementClick({ref});")
    if result is not True:
        logging.warning("Clicking %s failed: %s", ref, result)


def execute_type(text: str, driver: ChromeDriver):
    """Send keystrokes to the focused element."""
    chain = ActionChains(driver)
    chain.send_keys(text)
    chain.perform()


def execute_focus_and_type(ref: int, text: str, driver: ChromeDriver):
    """Click the specified DOM element and then send keystrokes."""
    execute_element_click(ref, driver)
    execute_type(text, driver)
