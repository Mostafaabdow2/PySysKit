"""System information and resource monitoring."""

from __future__ import annotations

import platform
import socket
import time
from typing import Any

import psutil

from pysyskit.core.logger import get_logger
from pysyskit.exceptions import SystemInformationError


logger = get_logger(__name__)


def get_system_info() -> dict[str, Any]:
    """
    Collect general information about the host system.

    Returns:
        Dictionary containing system information.

    Raises:
        SystemInformationError:
            If system information cannot be collected.
    """

    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time

        return {
            "hostname": socket.gethostname(),
            "operating_system": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(logical=True),
            "physical_cpu_count": psutil.cpu_count(logical=False),
            "boot_time": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(boot_time),
            ),
            "uptime_seconds": round(uptime_seconds, 2),
        }

    except Exception as exc:
        logger.exception("Failed to collect system information.")
        raise SystemInformationError(
            "Unable to collect system information."
        ) from exc


def get_resource_usage() -> dict[str, Any]:
    """
    Collect current CPU, memory, swap, and disk usage.

    Returns:
        Dictionary containing resource usage information.
    """

    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage("/")

        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent,
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
        }

    except Exception as exc:
        logger.exception("Failed to collect resource usage.")
        raise SystemInformationError(
            "Unable to collect resource usage."
        ) from exc
