"""Filesystem usage inspection."""

from __future__ import annotations

from typing import Any

import psutil

from pysyskit.core.logger import get_logger
from pysyskit.exceptions import FilesystemInformationError


logger = get_logger(__name__)


def get_disk_usage(path: str = "/") -> dict[str, Any]:
    """
    Return filesystem usage information.

    Args:
        path: Filesystem path to inspect.

    Returns:
        Dictionary containing filesystem statistics.
    """

    try:
        usage = psutil.disk_usage(path)

        return {
            "path": path,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        }

    except Exception as exc:
        logger.exception(
            "Failed to collect filesystem information."
        )

        raise FilesystemInformationError(
            f"Unable to inspect filesystem: {path}"
        ) from exc
