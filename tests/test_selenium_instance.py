"""Test Selenium instance configuration."""
from unittest.mock import Mock

import pytest

import miniwob.selenium_instance as selenium_instance
from miniwob.selenium_instance import SeleniumInstance


def mock_driver_creation(monkeypatch):
    """Create an instance with browser startup mocked out."""
    driver = Mock()
    driver.execute_script.return_value = [800, 600]
    chrome = Mock(return_value=driver)
    service = Mock()
    wait = Mock()

    monkeypatch.setattr(selenium_instance.webdriver, "Chrome", chrome)
    monkeypatch.setattr(selenium_instance, "ChromeService", service)
    monkeypatch.setattr(selenium_instance, "WebDriverWait", wait)

    instance = SeleniumInstance(index=0, subdomain="click-test", headless=True)
    return instance, chrome, driver, service


def test_create_driver_uses_documented_chrome_paths(monkeypatch):
    """Use the browser and driver named in the public configuration contract."""
    monkeypatch.setenv("MINIWOB_CHROME_BINARY", "/tmp/chrome-for-testing/chrome")
    monkeypatch.setenv("MINIWOB_CHROMEDRIVER", "/tmp/chrome-for-testing/chromedriver")
    instance, chrome, driver, service = mock_driver_creation(monkeypatch)

    instance.create_driver()

    options = chrome.call_args.kwargs["options"]
    assert options.binary_location == "/tmp/chrome-for-testing/chrome"
    service.assert_called_once_with(
        executable_path="/tmp/chrome-for-testing/chromedriver"
    )
    chrome.assert_called_once_with(
        service=service.return_value,
        options=options,
    )
    driver.implicitly_wait.assert_called_once_with(5)


def test_create_driver_uses_selenium_discovery_by_default(monkeypatch):
    """Preserve Selenium's default discovery when no paths are configured."""
    monkeypatch.delenv("MINIWOB_CHROME_BINARY", raising=False)
    monkeypatch.delenv("MINIWOB_CHROMEDRIVER", raising=False)
    instance, chrome, _, service = mock_driver_creation(monkeypatch)

    instance.create_driver()

    options = chrome.call_args.kwargs["options"]
    assert options.binary_location == ""
    service.assert_not_called()
    chrome.assert_called_once_with(options=options)


@pytest.mark.parametrize(
    "name",
    ["MINIWOB_CHROME_BINARY", "MINIWOB_CHROMEDRIVER"],
)
def test_create_driver_rejects_incomplete_chrome_configuration(monkeypatch, name):
    """Reject a browser or driver override without its matching counterpart."""
    monkeypatch.delenv("MINIWOB_CHROME_BINARY", raising=False)
    monkeypatch.delenv("MINIWOB_CHROMEDRIVER", raising=False)
    monkeypatch.setenv(name, "/tmp/configured-path")
    instance, chrome, _, _ = mock_driver_creation(monkeypatch)

    with pytest.raises(ValueError, match="must be set together"):
        instance.create_driver()

    chrome.assert_not_called()
