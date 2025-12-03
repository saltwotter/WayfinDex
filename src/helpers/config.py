# Handles configuration settings for the application
import os
import yaml
from .models import WayfinDexConfig


class WayfinDexConfigLoader:
    """Configuration handler for WayfinDex application."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config: WayfinDexConfig = self.load_config()

    def load_config(self) -> WayfinDexConfig:
        """Load configuration from a YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file {self.config_path} not found.")
        with open(self.config_path, "r") as file:
            config_data = yaml.safe_load(file)
            return WayfinDexConfig(**config_data)

    def save_config(self) -> None:
        """Save the current configuration to a YAML file."""
        with open(self.config_path, "w") as file:
            yaml.safe_dump(self.config.model_dump(), file)
