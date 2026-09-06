"""
Sets up Python's built-in logging so we get readable messages like:

    2026-09-06 10:00:00 | INFO | app.main | Application startup complete

Instead of scattering print() statements everywhere, we use logging so
messages can be turned on/off, sent to files, or filtered by severity
level (INFO, WARNING, ERROR) later without touching business logic.
"""

import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
