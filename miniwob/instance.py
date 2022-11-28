import json
import logging
import pathlib
import time
import traceback
import urllib.parse
from queue import Queue
from threading import Thread

import numpy as np
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from miniwob.action import to_action_object
from miniwob.fields import Fields, get_field_extractor
from miniwob.reward import get_original_reward
from miniwob.screenshot import get_screenshot
from miniwob.state import MiniWoBState

HTML_DIR = pathlib.Path(__file__).parent.parent / "html"
DEFAULT_BASE_URL = f"file://{HTML_DIR}/"


class MiniWoBInstance(Thread):
    """Interface between Python and Chrome driver via Selenium.
    Manages a single instance.
    """

    # Added some space for title bar
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 240
    TASK_WIDTH = 160
    TASK_HEIGHT = 210

    FLIGHT_WINDOW_WIDTH = 600
    FLIGHT_WINDOW_HEIGHT = 700
    FLIGHT_TASK_WIDTH = 375
    FLIGHT_TASK_HEIGHT = 667

    def __init__(
        self,
        index,
        subdomain=None,
        headless=False,
        base_url=None,
        cache_state=False,
        threading=True,
        reward_processor=None,
        wait_ms=0.0,
        block_on_reset=True,
        refresh_freq=0,
        data_mode="train",
    ):
        """Starts a new Selenium WebDriver session.

        Args:
            index (int): Instance index
            subdomain (str): MiniWoB task name (e.g., "click-test")
            headless (bool): Whether to render GUI
            base_url (str): Base URL, which is usually one of the following
                - http://localhost:8000/     (served by http-serve)
                - file:///path/to/miniwob-plusplus/html/
                If None, infers the file:// path from this module's location.
            cache_state (bool): Whether to cache and return the initial
                state; only make sense if the task interface never changes
            threading (bool): Whether to run this instance as a Thread
            reward_processor (callable; optional): A function that takes
                the metadata and return a reward (see miniwob.reward)
            wait_ms (float): Pause the instance after each action for this
                amount of time (in milliseconds).
            block_on_reset (bool): On reset, block until the page loads.
            refresh_freq (int): Every this number of episodes,
                refresh the page at the beginning of the next episode.
                Takes time but cleans up any lingering states and memory leaks.
                *** Must specify `seeds` at each reset call.
            data_mode (str): Data mode (e.g., "train", "test")
        """
        super().__init__()
        # Overrides Thread.daemon: Kill this thread when the parent is killed
        self.daemon = True
        self.died = False
        self.index = index
        self.headless = headless
        base_url = base_url or DEFAULT_BASE_URL
        if subdomain.startswith("flight."):
            assert not base_url.startswith("file://"), (
                "For {} domain, MINIWOB_BASE_URL cannot be file://. "
                ' See "Run a simple server" in README'
            ).format(subdomain)
            self.url = urllib.parse.urljoin(
                base_url, subdomain.replace(".", "/") + "/wrapper.html"
            )
            self.window_width = self.FLIGHT_WINDOW_WIDTH
            self.window_height = self.FLIGHT_WINDOW_HEIGHT
            self.task_width = self.FLIGHT_TASK_WIDTH
            self.task_height = self.FLIGHT_TASK_HEIGHT
        else:
            self.url = urllib.parse.urljoin(base_url, f"miniwob/{subdomain}.html")
            self.window_width = self.WINDOW_WIDTH
            self.window_height = self.WINDOW_HEIGHT
            self.task_width = self.TASK_WIDTH
            self.task_height = self.TASK_HEIGHT
        self.field_extractor = get_field_extractor(subdomain)
        self.cache_state = cache_state
        self.threading = threading
        self.reward_processor = reward_processor
        self.wait_ms = wait_ms
        self.block_on_reset = block_on_reset
        self.refresh_freq = refresh_freq
        self.num_episodes = 0
        self.mode = data_mode
        self.record_screenshots = False
        if reward_processor is None:
            # Use the original reward
            self.reward_processor = get_original_reward
        self.start_time = float("inf")
        self.task_queue = Queue()
        if not threading:
            # Hack: override the start method of Thread
            self.start = self.create_driver

    def run(self):
        """Overrides `Thread.run`"""
        try:
            self.create_driver()
            # Wait for command
            while True:
                func, args = self.task_queue.get()
                try:
                    func(*args)
                except Exception:
                    logging.error("Error in instance %d", self.index)
                    traceback.print_exc()
                    self.died = True
                self.task_queue.task_done()
                if func == self.close:
                    break
        finally:
            self.close()
            logging.info("Closed instance %d", self.index)

    def call(self, func, *args):
        if self.threading:
            self.task_queue.put((func, args))
        else:
            func(*args)

    def wait(self):
        if self.threading:
            self.task_queue.join()

    ################################
    # Possible Functions

    def create_driver(self):
        """Create a driver"""
        assert not hasattr(self, "driver"), "Instance {} already has a driver".format(
            self.index
        )
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("headless")
            options.add_argument("disable-gpu")
            options.add_argument("no-sandbox")
        else:
            options.add_argument("app=" + self.url)
            options.add_argument(
                f"window-size={self.window_width},{self.window_height}"
            )
            options.add_argument(
                "window-position={},{}".format(
                    9000, 30 + self.index * (self.window_height + 30)
                )
            )
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        if self.headless:
            self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, self.SYNC_SCREEN_ID))
            )
        except TimeoutException as e:
            logging.error("Page did not load properly. Wrong MINIWOB_BASE_URL?")
            raise e

    def close(self):
        """Tear down the WebDriver."""
        # Note: close() will close the current window
        # quit() closes everything, so it is probably cleaner
        try:
            self.driver.quit()
        except Exception:
            logging.error("Error closing the driver of instance %d", self.index)
            traceback.print_exc()
        self.died = True

    def reset(self, states, infos, seed):
        """Forces stop and start this instance.
        Also sets states[i] to be the initial state
        (where i = self.index).

        Args:
            states (list)
            infos (list)
            seed (object): Seed to set for the next episode
        """
        if self.refresh_freq:
            assert (
                seed is not None
            ), "reset() must specify seed if refresh_freq is specified"
        i = self.index
        self.force_stop()
        self.begin_task(seed=seed)
        states[i] = self.get_state()
        if self.cache_state:
            self.initial_state = states[i]
        metadata = self.get_metadata()
        infos[i] = metadata

    def step(self, action, states, rewards, dones, infos):
        """Applies an action on this instance.
        Also sets states[i], rewards[i], dones[i], and infos[i]
        (where i = self.index).

        Args:
            action (MiniWoBAction)
            states (list)
            rewards (list)
            dones (list)
            infos (list)
        """
        i = self.index
        self.perform(action)
        metadata = self.get_metadata()
        rewards[i] = self.reward_processor(metadata)
        dones[i] = metadata["done"]
        if not metadata["done"]:
            if not self.cache_state:
                states[i] = self.get_state()
            else:
                states[i] = self.initial_state
        metadata["elapsed"] = max(0.0, time.time() - self.start_time)
        infos[i] = metadata

    ################################
    # Primitive actions

    SYNC_SCREEN_ID = "sync-task-cover"
    RESET_BLOCK_SLEEP_TIME = 0.05  # 50ms
    RESET_BLOCK_MAX_ATTEMPT = 20  # up to 1s

    def force_stop(self):
        """Force stop the task and go back to the sync screen."""
        self.driver.execute_script("return core.endEpisode(0);")

    def begin_task(self, seed=None):
        """Start the task. Only available when done is True.
        The sync screen will disappear and the countdown timer will start.

        Args:
            seed: New seed to set for the next episode
        """
        self.num_episodes += 1
        if self.refresh_freq and self.num_episodes % self.refresh_freq == 0:
            self.driver.get(self.url)
        if seed is not None:
            self.set_seed(seed)
        self.set_mode(self.mode)
        self.driver.execute_script("core.startEpisodeReal();")
        if self.block_on_reset:
            for _ in range(self.RESET_BLOCK_MAX_ATTEMPT):
                if self.driver.execute_script("return WOB_TASK_READY;"):
                    break
                time.sleep(self.RESET_BLOCK_SLEEP_TIME)
            else:
                raise RuntimeError(f"Instance {self.index} does not load properly")
        elif self.wait_ms:
            time.sleep(self.wait_ms / 1000.0)
        self.start_time = time.time()

    def perform(self, action):
        """Perform an action.

        Args:
            action: One of the following
            - None: Do nothing
            - a callable f(driver) that takes a Selenium driver as an argument;
                issue a warning if the instance is done
        """
        if action is not None:
            if self.get_metadata()["done"]:
                logging.warning(
                    "Cannot call %s on instance %d, which is already done",
                    action,
                    self.index,
                )
            else:
                to_action_object(action)(self.driver)
        if self.wait_ms:
            time.sleep(self.wait_ms / 1000.0)

    def get_state(self):
        """Get the current state.

        Returns:
            MiniWoBState
        """
        # Get the utterance
        response = self.driver.execute_script("return core.getUtterance();")
        if isinstance(response, dict):
            utterance = response["utterance"]
            fields = Fields(response["fields"])
        else:
            utterance = response
            fields = self.field_extractor(utterance)
        # Get the DOM
        dom_info = self.driver.execute_script("return core.getDOMInfo();")
        state = MiniWoBState(utterance, fields, dom_info)
        # Get screenshot if requested
        if self.record_screenshots:
            img = get_screenshot(self.driver, self.task_width, self.task_height)
            state.set_screenshot(img)
        return state

    def get_metadata(self):
        """Get other metadata.

        Returns:
            dict with the following keys:
            - done (bool)
            - env_reward (float; only well-defined when done is True):
                Environment-defined reward, possibly scaled by time
            - raw_reward (float; only well-defined when done is True):
                Environment-defined reward, NOT scaled by time
            - reason (any): reason for giving the reward (for debugging);
                will likely be None if done is False
        """
        return self.driver.execute_script(
            "return {"
            '"done": WOB_DONE_GLOBAL,'
            '"env_reward": WOB_REWARD_GLOBAL,'
            '"raw_reward": WOB_RAW_REWARD_GLOBAL,'
            '"reason": WOB_REWARD_REASON,'
            "};"
        )

    def visualize_attention(self, attention):
        """Sends the attention weights to be visualized.

        Args:
            attentions: one of the following:
                - None: Do not do anything
                - np.array or 2d list of shape (num_grid_rows, num_grid_cols)
                - np.array or 2d list of shape (0, 0): Clear the visualization
        """
        if attention is None:
            return
        # Encode as JSON
        if isinstance(attention, np.ndarray):
            attention = attention.tolist()
        encoded = json.dumps(attention)
        # Send to the driver
        self.driver.execute_script(f"core.visualizeAttention({encoded});")

    def set_seed(self, seed):
        """Set the seed to a new value.

        Args:
            seed (object)
        """
        self.driver.execute_script(f"Math.seedrandom({repr(seed)});")

    def set_mode(self, mode):
        """Set the task generation mode (e.g., "train" or "test") to a new value.

        Args:
            mode (str)
        """
        self.driver.execute_script(f'core.setDataMode("{mode}");')
