import os

from hyfi import HyFI

from ._version import __version__

# Read the package name from the current directory
__package_name__ = os.path.basename(os.path.dirname(__file__))

# Initialize the global HyFI object
HyFI.initialize_global_hyfi(package_name=__package_name__, version=__version__)

# Initialize the logger
HyFI.setLogger()


def get_version() -> str:
    """Get the package version."""
    return __version__


__all__ = ["HyFI", "get_version"]
