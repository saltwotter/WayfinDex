"""
Configuration management for WayfinDex.

This module handles loading, validating, and managing YAML configuration files,
including environment selection and agent activation.
"""

import os
from pathlib import Path
import yaml
from dotenv import load_dotenv
from .type_models import WayfinDexConfig


class WayfinDexConfigLoader:
    """
    Configuration handler for WayfinDex application.

    Loads and manages YAML configuration, including environment selection
    and agent activation. Validates configuration against WayfinDexConfig model.

    Attributes:
        config_path: Path to the YAML configuration file
        config: Loaded and validated WayfinDexConfig instance
    """

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the configuration loader.

        Loads environment variables from .env file if it exists in the repository root,
        then loads and validates the YAML configuration.

        Args:
            config_path: Path to the YAML configuration file (default: config.yaml)
        """
        # Load .env file from repository root if it exists
        env_path = Path(config_path).parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)

        self.config_path = config_path
        self.config: WayfinDexConfig = self.load_config()

    def load_config(self) -> WayfinDexConfig:
        """
        Load and validate configuration from YAML file.

        Reads the YAML file and validates it against the WayfinDexConfig Pydantic model.

        Returns:
            Validated WayfinDexConfig instance

        Raises:
            FileNotFoundError: If the configuration file doesn't exist
            yaml.YAMLError: If the YAML is malformed
            pydantic.ValidationError: If the configuration is invalid
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file {self.config_path} not found.")
        with open(self.config_path, "r") as file:
            config_data = yaml.safe_load(file)
            return WayfinDexConfig(**config_data)

    def save_config(self) -> None:
        """
        Save the current configuration to the YAML file.

        Serializes the WayfinDexConfig instance to YAML format and writes
        it to the configured file path.
        """
        with open(self.config_path, "w") as file:
            yaml.safe_dump(self.config.model_dump(), file)

    def set_environment(self, environment_name: str) -> None:
        """
        Set the active agents based on the specified environment.

        Args:
            environment_name: The name of the environment to activate

        Raises:
            ValueError: If the environment name is not found in the configuration
        """
        for env in self.config.environments:
            if env.name == environment_name:
                self.config.active_agents = env.agents
                return

        available_envs = [env.name for env in self.config.environments]
        raise ValueError(
            f"Environment '{environment_name}' not found. "
            f"Available environments: {', '.join(available_envs)}"
        )

    def get_available_environments(self) -> list[str]:
        """
        Get list of all configured environment names.

        Returns:
            List of environment name strings (e.g., ['prod', 'dev', 'testing'])
        """
        return [env.name for env in self.config.environments]
