"""Root `__init__` of the miniwob module."""
import sys


__version__ = "1.0"

try:
    from farama_notifications import notifications

    if (
        "miniwob-plusplus" in notifications
        and __version__ in notifications["miniwob-plusplus"]
    ):
        print(notifications["miniwob-plusplus"][__version__], file=sys.stderr)

except Exception:  # nosec
    pass
