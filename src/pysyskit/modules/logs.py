"""Local log analysis for Linux authentication and system logs."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Any

from pysyskit.core.logger import get_logger

logger = get_logger(__name__)

DEFAULT_LOGS = (
    "/var/log/auth.log",
    "/var/log/syslog",
    "/var/log/kern.log",
)

FAILED_AUTH_PATTERNS = (
    re.compile(r"Failed password", re.IGNORECASE),
    re.compile(r"authentication failure", re.IGNORECASE),
    re.compile(r"Invalid user", re.IGNORECASE),
)

SUCCESS_AUTH_PATTERNS = (
    re.compile(r"Accepted password", re.IGNORECASE),
    re.compile(r"Accepted publickey", re.IGNORECASE),
)


def analyze_logs(
    paths: tuple[str, ...] = DEFAULT_LOGS,
    max_lines: int = 50000,
) -> dict[str, Any]:
    """Analyze accessible local Linux logs."""

    failed = 0
    successful = 0
    invalid_users = 0

    sources: Counter[str] = Counter()

    scanned_files: list[str] = []
    inaccessible: list[str] = []

    for raw_path in paths:
        path = Path(raw_path)

        if not path.exists() or not path.is_file():
            continue

        scanned_files.append(str(path))

        try:
            with path.open(
                "r",
                encoding="utf-8",
                errors="replace",
            ) as handle:

                for number, line in enumerate(handle):

                    if number >= max_lines:
                        break

                    if any(
                        pattern.search(line)
                        for pattern in FAILED_AUTH_PATTERNS
                    ):
                        failed += 1

                        match = re.search(
                            r"(?:from|rhost=)\s*([0-9a-fA-F:.]+)",
                            line,
                            re.IGNORECASE,
                        )

                        if match:
                            sources[match.group(1)] += 1

                    if any(
                        pattern.search(line)
                        for pattern in SUCCESS_AUTH_PATTERNS
                    ):
                        successful += 1

                    if re.search(
                        r"Invalid user",
                        line,
                        re.IGNORECASE,
                    ):
                        invalid_users += 1

        except (PermissionError, OSError):
            inaccessible.append(str(path))

    return {
        "scanned_files": scanned_files,
        "inaccessible_files": inaccessible,
        "failed_authentication_attempts": failed,
        "successful_authentication_events": successful,
        "invalid_user_events": invalid_users,
        "top_failure_sources": sources.most_common(10),
    }

