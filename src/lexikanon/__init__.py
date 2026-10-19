"""Tokenizers, normalizers, and stopwords. Importing lexikanon does not import HyFI."""

from ._version import __version__


def get_version() -> str:
    """Get the package version."""
    return __version__


__all__ = ["__version__", "get_version"]
