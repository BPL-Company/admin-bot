try:
    from tokens import config
except ImportError:
    import os
    config = os.environ
