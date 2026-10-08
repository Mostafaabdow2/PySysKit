"""Network interface inspection."""

from __future__ import annotations

from typing import Any

import psutil

from pysyskit.core.logger import get_logger
from pysyskit.exceptions import NetworkInformationError


logger = get_logger(__name__)


def get_network_info() -> list[dict[str, Any]]:
    """
    Collect network interface information.

    Returns:
        List containing interface details.
    """

    try:
        addresses = psutil.net_if_addrs()
        statistics = psutil.net_if_stats()

        interfaces: list[dict[str, Any]] = []

        for interface_name, address_list in addresses.items():
            interface_stats = statistics.get(interface_name)

            interface_data = {
                "name": interface_name,
                "is_up": interface_stats.isup if interface_stats else None,
                "speed_mbps": (
                    interface_stats.speed
                    if interface_stats
                    else None
                ),
                "addresses": [],
            }

            for address in address_list:
                interface_data["addresses"].append(
                    {
                        "family": str(address.family),
                        "address": address.address,
                        "netmask": address.netmask,
                        "broadcast": address.broadcast,
                    }
                )

            interfaces.append(interface_data)

        return interfaces

    except Exception as exc:
        logger.exception("Failed to collect network information.")
        raise NetworkInformationError(
            "Unable to collect network information."
        ) from exc
