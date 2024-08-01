"""Constants for the package."""

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore

__version__: str = metadata.version(__package__ or __name__)
__desc__: str = metadata.metadata(__package__ or __name__)["Summary"]
AUTHOR: str = metadata.metadata(__package__ or __name__)["Author"]
GITHUB: str = metadata.metadata(__package__ or __name__)["Home-page"]
PACKAGE: str | None = __package__
