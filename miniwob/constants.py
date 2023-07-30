"""Constants for the environment and spaces."""
import itertools


ASCII_CHARSET = "".join(chr(x) for x in range(32, 127))
UTTERANCE_MAX_LENGTH = 256
ATTRIBUTE_MAX_LENGTH = 256
TEXT_MAX_LENGTH = 256
TYPING_MAX_LENGTH = 64
FIELD_KEY_MAX_LENGTH = 64
FIELD_VALUE_MAX_LENGTH = 64

DEFAULT_SCROLL_AMOUNT = 50
DEFAULT_SCROLL_TIME = 150

# Special key mapping, as specified in the WebDriver API:
# https://www.w3.org/TR/webdriver/#keyboard-actions
# Some of these are not on usual keyboard layouts.
WEBDRIVER_SPECIAL_KEYS = {
    "<Unidentified>": "\uE000",
    "<Cancel>": "\uE001",
    "<Help>": "\uE002",
    "<Backspace>": "\uE003",
    "<Tab>": "\uE004",
    "<Clear>": "\uE005",
    "<Enter>": "\uE006",
    "<NumpadEnter>": "\uE007",
    "<Shift>": "\uE008",
    "<Control>": "\uE009",
    "<Alt>": "\uE00A",
    "<Pause>": "\uE00B",
    "<Escape>": "\uE00C",
    "<Space>": "\uE00D",  # " "
    "<PageUp>": "\uE00E",
    "<PageDown>": "\uE00F",
    "<End>": "\uE010",
    "<Home>": "\uE011",
    "<ArrowLeft>": "\uE012",
    "<ArrowUp>": "\uE013",
    "<ArrowRight>": "\uE014",
    "<ArrowDown>": "\uE015",
    "<Insert>": "\uE016",
    "<Delete>": "\uE017",
    "<Semicolon>": "\uE018",  # ";"
    "<Equal>": "\uE019",  # "="
    "<Numpad0>": "\uE01A",  # "0"
    "<Numpad1>": "\uE01B",  # "1"
    "<Numpad2>": "\uE01C",  # "2"
    "<Numpad3>": "\uE01D",  # "3"
    "<Numpad4>": "\uE01E",  # "4"
    "<Numpad5>": "\uE01F",  # "5"
    "<Numpad6>": "\uE020",  # "6"
    "<Numpad7>": "\uE021",  # "7"
    "<Numpad8>": "\uE022",  # "8"
    "<Numpad9>": "\uE023",  # "9"
    "<NumpadMultiply>": "\uE024",  # "*"
    "<NumpadAdd>": "\uE025",  # "+"
    "<NumpadComma>": "\uE026",  # ","
    "<NumpadSubtract>": "\uE027",  # "-"
    "<NumpadDecimal>": "\uE028",  # "."
    "<NumpadDivide>": "\uE029",  # "/"
    "<F1>": "\uE031",
    "<F2>": "\uE032",
    "<F3>": "\uE033",
    "<F4>": "\uE034",
    "<F5>": "\uE035",
    "<F6>": "\uE036",
    "<F7>": "\uE037",
    "<F8>": "\uE038",
    "<F9>": "\uE039",
    "<F10>": "\uE03A",
    "<F11>": "\uE03B",
    "<F12>": "\uE03C",
    "<Meta>": "\uE03D",
    "<ZenkakuHankaku>": "\uE040",
    "<RightShift>": "\uE050",
    "<RightControl>": "\uE051",
    "<RightAlt>": "\uE052",
    "<RightMeta>": "\uE053",
    "<NumpadPageUp>": "\uE054",
    "<NumpadPageDown>": "\uE055",
    "<NumpadEnd>": "\uE056",
    "<NumpadHome>": "\uE057",
    "<NumpadArrowLeft>": "\uE058",
    "<NumpadArrowUp>": "\uE059",
    "<NumpadArrowRight>": "\uE05A",
    "<NumpadArrowDown>": "\uE05B",
    "<NumpadInsert>": "\uE05C",
    "<NumpadDelete>": "\uE05D",
}

WEBDRIVER_MODIFIER_KEYS = {
    "A-": WEBDRIVER_SPECIAL_KEYS["<Alt>"],
    "C-": WEBDRIVER_SPECIAL_KEYS["<Control>"],
    "M-": WEBDRIVER_SPECIAL_KEYS["<Meta>"],
    "S-": WEBDRIVER_SPECIAL_KEYS["<Shift>"],
}

# List of all possible key combinations for keypress actions.
# Some of these are probably not safe (e.g., "A-<F4>").
ALL_POSSIBLE_KEYS = tuple(
    "".join(combo)
    for combo in itertools.product(
        *[("", modifier) for modifier in WEBDRIVER_MODIFIER_KEYS],
        (list(WEBDRIVER_SPECIAL_KEYS) + list(ASCII_CHARSET)),
    )
)

# List of safe key combinations from Humphreys et al., 2022:
# "A Data-Driven Approach for Learning to Control Computers"
# (https://arxiv.org/abs/2202.08137).
DEFAULT_ALLOWED_KEYS = (
    "<Enter>",
    "<PageUp>",
    "<PageDown>",
    "<Backspace>",
    "<Delete>",
    "<Tab>",
    "<Space>",
    "<ArrowUp>",
    "<ArrowRight>",
    "<ArrowDown>",
    "<ArrowLeft>",
    "[",
    "]",
    "-",
    "=",
    ";",
    '"',
    "\\",
    ",",
    ".",
    "/",
    "`",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "<Numpad0>",
    "<Numpad1>",
    "<Numpad2>",
    "<Numpad3>",
    "<Numpad4>",
    "<Numpad5>",
    "<Numpad6>",
    "<Numpad7>",
    "<Numpad8>",
    "<Numpad9>",
    "<NumpadAdd>",
    "<NumpadMultiply>",
    "<NumpadSubtract>",
    "<NumpadDivide>",
    "<NumpadDecimal>",
    "<NumpadEnter>",
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
    "C-a",
    "C-c",
    "C-x",
    "C-v",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
)

DEFAULT_ALLOWED_KEYS_MAC_OS = tuple(x.replace("C-", "M-") for x in DEFAULT_ALLOWED_KEYS)

MIN_REF = -1000000
MAX_REF = 1000000
MAX_FIELDS = 20

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 320
TASK_WIDTH = 160
TASK_HEIGHT = 210

FLIGHT_WINDOW_WIDTH = 600
FLIGHT_WINDOW_HEIGHT = 800
FLIGHT_TASK_WIDTH = 375
FLIGHT_TASK_HEIGHT = 667
