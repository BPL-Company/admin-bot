import os
import logging

try:
    from tokens import config
except ImportError:
    config = os.environ
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)

OWNERS = [792414733, 441399484, 268486177]
MAX_WARNS = os.environ.get("MAX_WARNS") or 2
TIME_POLL_WARN = 10  # in seconds
