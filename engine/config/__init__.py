"""Configuration loader entry point for BOS-FS engine."""

from .loader import ConfigLoader

_default_loader = ConfigLoader()


def get_default_config() -> dict:
    """Load and return the default configuration.
    
    Returns:
        dict: Merged default configuration from all JSON files in defaults/
    """
    return _default_loader.load_all_defaults()


__all__ = ["ConfigLoader", "get_default_config"]
