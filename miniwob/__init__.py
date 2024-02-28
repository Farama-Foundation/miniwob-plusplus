"""Root `__init__` of the miniwob module."""
import sys

from miniwob.registration import register_miniwob_envs


__version__ = "1.0"

register_miniwob_envs()

try:
    from farama_notifications import notifications

    if (
        "miniwob-plusplus" in notifications
        and __version__ in notifications["miniwob-plusplus"]
    ):
        print(notifications["miniwob-plusplus"][__version__], file=sys.stderr)

except Exception:  # nosec
    pass
