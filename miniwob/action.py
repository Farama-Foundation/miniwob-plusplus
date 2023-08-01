"""MiniWoB action space."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Sequence, Tuple

import numpy as np
from gymnasium import spaces

from miniwob.constants import (
    DEFAULT_ALLOWED_KEYS,
    DEFAULT_ALLOWED_KEYS_MAC_OS,
    DEFAULT_SCROLL_AMOUNT,
    DEFAULT_SCROLL_TIME,
    MAX_FIELDS,
    MAX_REF,
    TYPING_MAX_LENGTH,
)
from miniwob.spaces import Unicode


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


COORDS_ACTIONS = frozenset(
    {
        ActionTypes.MOVE_COORDS,
        ActionTypes.CLICK_COORDS,
        ActionTypes.DBLCLICK_COORDS,
        ActionTypes.MOUSEDOWN_COORDS,
        ActionTypes.MOUSEUP_COORDS,
        ActionTypes.SCROLL_UP_COORDS,
        ActionTypes.SCROLL_DOWN_COORDS,
    }
)
SCROLL_ACTIONS = frozenset(
    {
        ActionTypes.SCROLL_UP_COORDS,
        ActionTypes.SCROLL_DOWN_COORDS,
    }
)
ELEMENT_ACTIONS = frozenset(
    {
        ActionTypes.CLICK_ELEMENT,
        ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT,
        ActionTypes.FOCUS_ELEMENT_AND_TYPE_FIELD,
    }
)
TEXT_ACTIONS = frozenset(
    {
        ActionTypes.TYPE_TEXT,
        ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT,
    }
)
FIELD_ACTIONS = frozenset(
    {
        ActionTypes.TYPE_FIELD,
        ActionTypes.FOCUS_ELEMENT_AND_TYPE_FIELD,
    }
)


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
    """

    action_types: Sequence[ActionTypes]
    screen_width: Optional[float] = None
    screen_height: Optional[float] = None
    coord_bins: Optional[Tuple[int, int]] = None
    scroll_amount: int = DEFAULT_SCROLL_AMOUNT
    scroll_time: int = DEFAULT_SCROLL_TIME
    allowed_keys: Sequence[str] = DEFAULT_ALLOWED_KEYS
    text_max_len: int = TYPING_MAX_LENGTH

    @classmethod
    def get_preset(cls, name="all_supported"):
        """Returns a preset config."""
        allowed_keys = DEFAULT_ALLOWED_KEYS
        if "_mac_os" in name:
            allowed_keys = DEFAULT_ALLOWED_KEYS_MAC_OS
            name = name.replace("_mac_os", "")
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
                ],
                allowed_keys=allowed_keys,
            )
        elif name == "shi17":
            # Action space from (Shi et al., 2017) "World of Bits:
            # An Open-Domain Platform for Web-Based Agents."
            # They use coordinate mouse actions and the press key action.
            # The "drag" action is approximated with mousedown + mouseup.
            return cls(
                action_types=[
                    ActionTypes.NONE,
                    ActionTypes.CLICK_COORDS,
                    ActionTypes.DBLCLICK_COORDS,
                    ActionTypes.MOUSEDOWN_COORDS,
                    ActionTypes.MOUSEUP_COORDS,
                    ActionTypes.SCROLL_UP_COORDS,
                    ActionTypes.SCROLL_DOWN_COORDS,
                    ActionTypes.PRESS_KEY,
                ],
                allowed_keys=allowed_keys,
            )
        elif name == "liu18":
            # Action space from (Liu et al., 2018) "Reinforcement Learning
            # on Web Interfaces Using Workflow-Guided Exploration."
            # They use element click and element click-and-type actions.
            # Only texts from input fields can be typed.
            return cls(
                action_types=[
                    ActionTypes.NONE,
                    ActionTypes.CLICK_ELEMENT,
                    ActionTypes.FOCUS_ELEMENT_AND_TYPE_FIELD,
                ],
                allowed_keys=allowed_keys,
            )
        elif name == "humphreys22":
            # Action space from (Humphreys et al., 2022) "A data-driven
            # approach for learning to control computers."
            # The main model uses binned coordinate mouse actions, plus the
            # press key and type field actions.
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
                    ActionTypes.PRESS_KEY,
                    ActionTypes.TYPE_FIELD,
                ],
                coord_bins=(51, 51),
                allowed_keys=allowed_keys,
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
            space["text"] = Unicode(self.text_max_len)
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
