"""Root `__init__` of the miniwob module."""
import sys


__version__ = "0.0.1"

try:
    from farama_notifications import notifications

    if "gymnasium" in notifications and __version__ in notifications["gymnasium"]:
        print(notifications["gymnasium"][__version__], file=sys.stderr)

except Exception:  # nosec
    pass
