import os
import logging

try:
    from tokens import config
except ImportError:
    config = os.environ
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)

OWNERS = [792414733, 441399484, 268486177, 1217967168]
MAX_WARNS = os.environ.get("MAX_WARNS") or 3
TIME_POLL_WARN = 300 # in seconds
