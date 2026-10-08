"""Security diagnostics for the local Linux host."""

from __future__ import annotations

import pwd
import socket
from typing import Any

import psutil

from pysyskit.core.logger import get_logger

logger = get_logger(__name__)

NON_INTERACTIVE_SHELLS = {
    "/usr/sbin/nologin",
    "/sbin/nologin",
    "/bin/false",
    "/usr/bin/false",
}


def get_open_ports() -> list[dict[str, Any]]:
    """Return listening TCP/UDP sockets visible to the current user."""

    findings: list[dict[str, Any]] = []

    try:
        connections = psutil.net_connections(
            kind="inet"
        )

    except (psutil.AccessDenied, PermissionError):

        return [{
            "severity": "HIGH",
            "status": "permission_denied",
            "message": (
                "Permission denied while reading "
                "network connections."
            ),
        }]

    seen: set[tuple[str, int, str]] = set()

    for connection in connections:

        if connection.status != psutil.CONN_LISTEN:
            continue

        if not connection.laddr:
            continue

        address = connection.laddr.ip
        port = connection.laddr.port

        protocol = (
            "tcp"
            if connection.type == socket.SOCK_STREAM
            else "udp"
        )

        key = (
            address,
            port,
            protocol,
        )

        if key in seen:
            continue

        seen.add(key)

        findings.append({
            "address": address,
            "port": port,
            "protocol": protocol,
            "pid": connection.pid,
            "severity": "INFO",
        })

    return sorted(
        findings,
        key=lambda item: (
            item["protocol"],
            item["port"],
        ),
    )


def inspect_accounts() -> list[dict[str, Any]]:
    """Inspect local accounts for security indicators."""

    results: list[dict[str, Any]] = []

    for entry in pwd.getpwall():

        username = entry.pw_name
        uid = entry.pw_uid
        shell = entry.pw_shell or ""

        indicators: list[str] = []

        if uid == 0 and username != "root":
            indicators.append(
                "UID 0 privileged account"
            )

        if shell not in NON_INTERACTIVE_SHELLS:
            indicators.append(
                "interactive login shell"
            )

        severity = "INFO"

        if uid == 0 and username != "root":
            severity = "HIGH"

        elif indicators:
            severity = "REVIEW"

        results.append({
            "username": username,
            "uid": uid,
            "gid": entry.pw_gid,
            "shell": shell,
            "severity": severity,
            "indicators": indicators,
        })

    return results


def run_security_audit() -> dict[str, Any]:
    """Run the local security diagnostics suite."""

    return {
        "open_ports": get_open_ports(),
        "accounts": inspect_accounts(),
    }
