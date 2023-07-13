"""MiniWoB observation space."""
from typing import Any, Dict, Sequence, Tuple

import numpy as np
from gymnasium import spaces

from miniwob.constants import (
    ATTRIBUTE_MAX_LENGTH,
    FIELD_KEY_MAX_LENGTH,
    FIELD_VALUE_MAX_LENGTH,
    MAX_REF,
    MIN_REF,
    TEXT_MAX_LENGTH,
    UTTERANCE_MAX_LENGTH,
)
from miniwob.dom import DOMElement
from miniwob.spaces import Unicode


Observation = Dict[str, Any]


def get_observation_space(screen_width: int, screen_height: int) -> spaces.Space:
    """Return the space of observations."""
    utterance_space = Unicode(
        min_length=0,
        max_length=UTTERANCE_MAX_LENGTH,
    )
    element_space = spaces.Dict(
        {
            # Non-zero integer ID:
            # `ref` for normal elements start from 1, while `ref` for text
            # pseudo-elements counts down from -1.
            "ref": spaces.Discrete(MAX_REF - MIN_REF, start=MIN_REF),
            # `ref` ID of the parent (0 = no parent, for root element).
            "parent": spaces.Discrete(MAX_REF),
            # Position and size
            "left": spaces.Box(float("-inf"), float("inf")),
            "top": spaces.Box(float("-inf"), float("inf")),
            "width": spaces.Box(0.0, float("inf")),
            "height": spaces.Box(0.0, float("inf")),
            # Tag:
            # For normal elements, this is the uppercased tag name (e.g., "DIV").
            # For <input> elements, the input type is appended (e.g., "INPUT_text").
            # Non-empty text nodes become pseudo-elements with tag "t".
            "tag": Unicode(max_length=ATTRIBUTE_MAX_LENGTH),
            # Text content of leaf nodes.
            "text": Unicode(
                min_length=0,
                max_length=TEXT_MAX_LENGTH,
            ),
            # Value of <input> elements.
            "value": Unicode(
                min_length=0,
                max_length=TEXT_MAX_LENGTH,
            ),
            # HTML id attribute
            "id": Unicode(
                min_length=0,
                max_length=ATTRIBUTE_MAX_LENGTH,
            ),
            # HTML class attribute (multiple classes are separated by spaces)
            "classes": Unicode(
                min_length=0,
                max_length=ATTRIBUTE_MAX_LENGTH,
            ),
            # Colors (RGBA)
            "bg_color": spaces.Box(
                np.array([0.0] * 4, dtype=np.float32),
                np.array([255.0] * 4, dtype=np.float32),
            ),
            "fg_color": spaces.Box(
                np.array([0.0] * 4, dtype=np.float32),
                np.array([255.0] * 4, dtype=np.float32),
            ),
            # Flags:
            # focused: whether the element is being focused on
            # tampered: whether the element has been tampered (clicked, focused, typed, etc.)
            # targeted: whether the element is an event target (for recorded demonstrations)
            # is_leaf: whether the element is a leaf
            "flags": spaces.MultiBinary(n=4),
        }
    )
    screenshot_space = spaces.Box(
        # Each position stores the RGB values. Note the swapped axes (height first).
        np.zeros((screen_height, screen_width, 3), dtype=np.uint8),
        np.ones((screen_height, screen_width, 3), dtype=np.uint8) * 255.0,
        dtype=np.uint8,
    )
    fields_space = spaces.Sequence(
        spaces.Tuple(
            (
                Unicode(
                    min_length=0,
                    max_length=FIELD_KEY_MAX_LENGTH,
                ),
                Unicode(
                    min_length=0,
                    max_length=FIELD_VALUE_MAX_LENGTH,
                ),
            )
        )
    )
    observation_space = spaces.Dict(
        {
            "utterance": utterance_space,
            "dom_elements": spaces.Sequence(element_space),
            "screenshot": screenshot_space,
            "fields": fields_space,
        }
    )
    return observation_space


def serialize_dom_element(element: DOMElement) -> Dict[str, Any]:
    """Serialize the given DOMElement to fit the element space."""
    serialized = {
        "ref": element.ref,
        "parent": element.parent.ref if element.parent else 0,
        "left": np.array([element.left], dtype=np.float32),
        "top": np.array([element.top], dtype=np.float32),
        "width": np.array([element.width], dtype=np.float32),
        "height": np.array([element.height], dtype=np.float32),
        "tag": element.tag[:ATTRIBUTE_MAX_LENGTH],
        "text": (element.text or "")[:TEXT_MAX_LENGTH],
        "value": str(element.value or "")[:TEXT_MAX_LENGTH],
        "id": element.id[:ATTRIBUTE_MAX_LENGTH],
        "classes": element.classes[:ATTRIBUTE_MAX_LENGTH],
        "bg_color": np.array(element.bg_color, dtype=np.float32),
        "fg_color": np.array(element.fg_color, dtype=np.float32),
        "flags": np.array(
            [
                element.focused,
                element.tampered,
                element.targeted,
                element.is_leaf,
            ],
            dtype=np.int8,
        ),
    }
    return serialized


def create_empty_screenshot(screen_width: int, screen_height: int) -> np.ndarray:
    """Returns an all-black screenshot."""
    return np.zeros((screen_height, screen_width, 3), dtype=np.uint8)


def create_empty_observation(screen_width: int, screen_height: int) -> Observation:
    """Returns an empty observation for a terminated session."""
    observation = {
        "utterance": "",
        "dom_elements": tuple(),
        "screenshot": create_empty_screenshot(screen_width, screen_height),
        "fields": tuple(),
    }
    return observation


def create_observation(
    utterance: str,
    root_dom: DOMElement,
    screenshot: np.ndarray,
    fields: Sequence[Tuple[str, str]],
) -> Observation:
    """Returns an observation that fits in the observation space.

    Args:
        utterance: Instruction text extracted from the task.
        root_dom: DOMElement object for the root element.
        screenshot: Screenshot as an RGB array.
        fields: Fields extracted from the utterance.

    Returns:
        the observation object
    """
    dom_elements = root_dom.subtree_elements
    serialized_elements = [serialize_dom_element(element) for element in dom_elements]
    observation = {
        "utterance": utterance[:UTTERANCE_MAX_LENGTH],
        "dom_elements": tuple(serialized_elements),
        "screenshot": screenshot,
        "fields": tuple(fields),
    }
    return observation
