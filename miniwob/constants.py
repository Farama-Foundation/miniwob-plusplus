"""Constants for the environment and spaces."""

ASCII_CHARSET = "".join(chr(x) for x in range(32, 128))
UTTERANCE_MAX_LENGTH = 256
ATTRIBUTE_MAX_LENGTH = 256
TEXT_MAX_LENGTH = 256
TYPING_MAX_LENGTH = 64
FIELD_KEY_MAX_LENGTH = 64
FIELD_VALUE_MAX_LENGTH = 64

# TODO: Use the list of keys from Humphreys22
DEFAULT_ALLOWED_KEYS = (
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
)

MIN_REF = -1000000
MAX_REF = 1000000
MAX_FIELDS = 20

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 320
TASK_WIDTH = 160
TASK_HEIGHT = 210

FLIGHT_WINDOW_WIDTH = 600
FLIGHT_WINDOW_HEIGHT = 700
FLIGHT_TASK_WIDTH = 375
FLIGHT_TASK_HEIGHT = 667
