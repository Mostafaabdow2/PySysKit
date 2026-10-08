"""Process inspection functionality."""

from __future__ import annotations

from typing import Any

import psutil

from pysyskit.core.logger import get_logger
from pysyskit.exceptions import ProcessInformationError


logger = get_logger(__name__)


def get_process_list() -> list[dict[str, Any]]:
    """
    Return information about currently running processes.

    Returns:
        List of process information dictionaries.
    """

    processes: list[dict[str, Any]] = []

    try:
        for process in psutil.process_iter(
            ["pid", "name", "status", "username", "memory_percent"]
        ):
            try:
                processes.append(
                    {
                        "pid": process.info["pid"],
                        "name": process.info["name"],
                        "status": process.info["status"],
                        "username": process.info["username"],
                        "memory_percent": round(
                            process.info["memory_percent"] or 0.0,
                            2,
                        ),
                    }
                )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return processes

    except Exception as exc:
        logger.exception("Failed to collect process information.")
        raise ProcessInformationError(
            "Unable to collect process information."
        ) from exc
