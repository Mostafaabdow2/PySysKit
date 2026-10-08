"""Custom exceptions used by PySysKit."""


class PySysKitError(Exception):
    """Base exception for PySysKit."""


class SystemInformationError(PySysKitError):
    """Raised when system information cannot be collected."""


class ProcessInformationError(PySysKitError):
    """Raised when process information cannot be collected."""


class NetworkInformationError(PySysKitError):
    """Raised when network information cannot be collected."""


class FilesystemInformationError(PySysKitError):
    """Raised when filesystem information cannot be collected."""
