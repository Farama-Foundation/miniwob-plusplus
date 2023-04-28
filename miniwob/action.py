"""MiniWoB action space."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Sequence, Set, Tuple, Union

import numpy as np
from gymnasium import spaces
from selenium.webdriver import Chrome as ChromeDriver

from miniwob import selenium_actions
from miniwob.constants import (
    ASCII_CHARSET,
    DEFAULT_ALLOWED_KEYS,
    DEFAULT_SCROLL_AMOUNT,
    DEFAULT_SCROLL_TIME,
    MAX_FIELDS,
    MAX_REF,
    TYPING_MAX_LENGTH,
)

Action = Dict[str, Any]


class ActionTypes(str, Enum):
    """Valid action types for MiniWoB environments."""

    # No-op
    NONE = "NONE"
    # Mouse actions with coordinates
    MOVE_COORDS = "MOVE_COORDS"
    CLICK_COORDS = "CLICK_COORDS"
    DBLCLICK_COORDS = "DBLCLICK_COORDS"
    MOUSEDOWN_COORDS = "MOUSEDOWN_COORDS"
    MOUSEUP_COORDS = "MOUSEUP_COORDS"
    # Mouse wheel
    SCROLL_UP_COORDS = "SCROLL_UP_COORDS"
    SCROLL_DOWN_COORDS = "SCROLL_DOWN_COORDS"
    # Mouse actions with elements
    CLICK_ELEMENT = "CLICK_ELEMENT"
    # Keyboard
    PRESS_KEY = "PRESS_KEY"
    TYPE_TEXT = "TYPE_TEXT"
    TYPE_FIELD = "TYPE_FIELD"
    FOCUS_ELEMENT_AND_TYPE_TEXT = "FOCUS_ELEMENT_AND_TYPE_TEXT"
    FOCUS_ELEMENT_AND_TYPE_FIELD = "FOCUS_ELEMENT_AND_TYPE_FIELD"


COORDS_ACTIONS = {
    ActionTypes.MOVE_COORDS,
    ActionTypes.CLICK_COORDS,
    ActionTypes.DBLCLICK_COORDS,
    ActionTypes.MOUSEDOWN_COORDS,
    ActionTypes.MOUSEUP_COORDS,
    ActionTypes.SCROLL_UP_COORDS,
    ActionTypes.SCROLL_DOWN_COORDS,
}
SCROLL_ACTIONS = {
    ActionTypes.SCROLL_UP_COORDS,
    ActionTypes.SCROLL_DOWN_COORDS,
}
ELEMENT_ACTIONS = {
    ActionTypes.CLICK_ELEMENT,
    ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT,
    ActionTypes.FOCUS_ELEMENT_AND_TYPE_FIELD,
}
TEXT_ACTIONS = {
    ActionTypes.TYPE_TEXT,
    ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT,
}
FIELD_ACTIONS = {
    ActionTypes.TYPE_FIELD,
    ActionTypes.FOCUS_ELEMENT_AND_TYPE_FIELD,
}


@dataclass
class ActionSpaceConfig:
    """Configurations for the action space.

    Attributes:
        action_types: An ordered sequence of action types to include.
            The order will be used for interpreting the Discrete space.
        screen_width: Screen width. Will be overridden by MiniWoBEnvironment.
        screen_height: Screen height. Will be overridden by MiniWoBEnvironment.
        coord_bins: If specified, bin the x and y coordinates to these numbers
            of bins. Mouse actions will be executed at the middle of the
            specified partition.
        scroll_amount: The amount to scroll for scroll actions.
        scroll_time: Time in milliseconds to wait for scroll action animation.
        allowed_keys: An ordered sequence of allowed keys and key combinations
            for the PRESS_KEY action. The order will be used for interpreting
            the Discrete space.
        text_max_len: Maximum text length for the TYPE_TEXT action.
        text_charset: Character set for the TYPE_TEXT action.
    """

    action_types: Sequence[ActionTypes]
    screen_width: Optional[float] = None
    screen_height: Optional[float] = None
    coord_bins: Optional[Tuple[int, int]] = None
    scroll_amount: int = DEFAULT_SCROLL_AMOUNT
    scroll_time: int = DEFAULT_SCROLL_TIME
    allowed_keys: Sequence[str] = DEFAULT_ALLOWED_KEYS
    text_max_len: int = TYPING_MAX_LENGTH
    text_charset: Union[str, Set[str]] = ASCII_CHARSET

    @classmethod
    def get_preset(cls, name="all_supported"):
        """Returns a preset config."""
        if name == "all_supported":
            return cls(
                action_types=[
                    ActionTypes.NONE,
                    ActionTypes.MOVE_COORDS,
                    ActionTypes.CLICK_COORDS,
                    ActionTypes.DBLCLICK_COORDS,
                    ActionTypes.MOUSEDOWN_COORDS,
                    ActionTypes.MOUSEUP_COORDS,
                    ActionTypes.SCROLL_UP_COORDS,
                    ActionTypes.SCROLL_DOWN_COORDS,
                    ActionTypes.CLICK_ELEMENT,
                    ActionTypes.PRESS_KEY,
                    ActionTypes.TYPE_TEXT,
                    ActionTypes.TYPE_FIELD,
                    ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT,
                    ActionTypes.FOCUS_ELEMENT_AND_TYPE_FIELD,
                ]
            )
        else:
            raise ValueError(f"Unknown preset name {name}")

    def get_action_space(self) -> spaces.Space:
        """Returns the space of serialized actions."""
        space = {}
        space["action_type"] = spaces.Discrete(len(self.action_types))
        if COORDS_ACTIONS.intersection(self.action_types):
            if not self.screen_width or not self.screen_height:
                raise ValueError("screen_width and screen_height must be specified.")
            if self.coord_bins:
                space["coords"] = spaces.MultiDiscrete(np.array(self.coord_bins))
            else:
                space["coords"] = spaces.Box(
                    np.array([0.0, 0.0], dtype=np.float32),
                    np.array([self.screen_width, self.screen_height], dtype=np.float32),
                )
        if ELEMENT_ACTIONS.intersection(self.action_types):
            space["ref"] = spaces.Discrete(MAX_REF)
        if ActionTypes.PRESS_KEY in self.action_types:
            space["key"] = spaces.Discrete(len(self.allowed_keys))
        if TEXT_ACTIONS.intersection(self.action_types):
            space["text"] = spaces.Text(self.text_max_len, charset=self.text_charset)
        if FIELD_ACTIONS.intersection(self.action_types):
            space["field"] = spaces.Discrete(MAX_FIELDS)
        return spaces.Dict(space)

    def compute_raw_coords(self, action: Action) -> Tuple[float, float]:
        """Extract the left and top coordinates from the action."""
        if self.coord_bins:
            # Add 0.5 to click at the middle of the partition.
            if not self.screen_width or not self.screen_height:
                raise ValueError("screen_width and screen_height must be specified.")
            left = (0.5 + int(action["coords"][0])) * (
                self.screen_width / self.coord_bins[0]
            )
            top = (0.5 + int(action["coords"][1])) * (
                self.screen_height / self.coord_bins[1]
            )
        else:
            left = float(action["coords"][0])
            top = float(action["coords"][1])
        return left, top


_SELENIUM_COORDS_ACTIONS = {
    ActionTypes.MOVE_COORDS: selenium_actions.execute_move_coords,
    ActionTypes.CLICK_COORDS: selenium_actions.execute_click_coords,
    ActionTypes.DBLCLICK_COORDS: selenium_actions.execute_dblclick_coords,
    ActionTypes.MOUSEDOWN_COORDS: selenium_actions.execute_mousedown_coords,
    ActionTypes.MOUSEUP_COORDS: selenium_actions.execute_mouseup_coords,
}


def execute_action(
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
            selenium_actions.execute_scroll_coords(
                left, top, scroll_amount, config.scroll_time, driver
            )
        else:
            _SELENIUM_COORDS_ACTIONS[action_type](left, top, driver)
        return
    # Key press action
    if action_type == ActionTypes.PRESS_KEY:
        key_idx = int(action["key"])
        key = config.allowed_keys[key_idx]
        selenium_actions.execute_press_key(key, driver)
        return
    # Element and typing actions
    if action_type in ELEMENT_ACTIONS:
        ref = int(action["ref"])
        selenium_actions.execute_click_element(ref, driver)
    if action_type in TEXT_ACTIONS:
        text = action["text"]
        selenium_actions.execute_type_text(text, driver)
    elif action_type in FIELD_ACTIONS:
        field_idx = int(action["field"])
        if field_idx >= len(fields):
            # Treat the value as empty
            text = ""
        else:
            text = fields[field_idx][1]
        selenium_actions.execute_type_text(text, driver)
