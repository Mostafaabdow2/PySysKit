"""Logging configuration for PySysKit."""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Logger name.

    Returns:
        Configured logging.Logger instance.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
