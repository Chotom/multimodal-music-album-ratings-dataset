"""Module with common exceptions used in the project."""
from pathlib import Path


class ExactFileNotFoundError(FileNotFoundError):
    """Raised when a file is not found on the local disk."""

    def __init__(self, path: Path | str) -> None:
        """Init custom exception class.

        Args:
            path: Path that raised this exception.
        """
        super().__init__(f"{path} file not found.")
