"""Configuration loader for KidGuard."""

import yaml
from pathlib import Path
from loguru import logger


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from YAML file."""
    path = Path(config_path)
    
    if not path.exists():
        logger.warning(f"Config file not found: {path}")
        logger.info("Using default configuration. Copy config.example.yaml to config.yaml")
        return get_default_config()
    
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    logger.info(f"Loaded config from {path}")
    return config


def get_default_config() -> dict:
    """Return default configuration."""
    return {
        "claude": {
            "model": "claude-sonnet-4-5"
        },
        "family": [],
        "rules": {
            "max_child_age": 12,
            "action": "redirect",
            "check_interval": 30,
            "clip_duration": 5
        },
        "safe_channels": [],
        "analysis": {
            "block_categories": ["violence", "horror", "adult"],
            "confidence_threshold": 0.7
        },
        "notifications": {
            "enabled": False
        },
        "privacy": {
            "delete_clips": True,
            "local_only": True
        }
    }
