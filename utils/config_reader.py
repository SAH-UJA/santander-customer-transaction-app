"""
Module for handling configuration settings.

This module provides a Config class for reading configuration settings from a YAML file.
It includes error handling, logging, and support for environment variables.
"""

import yaml
import os
import logging


class SingletonMeta(type):
    """
    Metaclass for creating singleton classes.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        config_path = kwargs.get("config_path", "default")
        if (
            cls not in cls._instances
            or cls._instances[cls].get("config_path") != config_path
        ):
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = {"instance": instance, "config_path": config_path}
        return cls._instances[cls]["instance"]


class Config(metaclass=SingletonMeta):
    def __init__(self, config_path=None):
        """
        Initialize the Config class.

        Args:
            config_path (str, optional): Path to the configuration file. Defaults to None.
        """
        try:
            # If config_path is not provided, use CONFIG_PATH environment variable or default to "config.yaml"
            if config_path is None:
                config_path = os.environ.get("CONFIG_PATH", "config.yaml")

            with open(config_path, "r") as file:
                self.config_data = yaml.safe_load(file)
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            raise e

    def get_classification_config(self):
        """
        Get the classification configuration settings.

        Returns:
            dict: Classification configuration settings.
        """
        return self.config_data.get("classification", {}).get("inference", {})

    def get_server_config(self):
        """
        Get the server configuration settings.

        Returns:
            dict: Server configuration settings.
        """
        return self.config_data.get("server", {})


def load_config():
    """
    Load the configuration using the Config class.

    Returns:
        Config: An instance of the Config class with loaded configuration settings.
    """
    try:
        config_path = os.environ.get("CONFIG_PATH", "config.yaml")
        config_reader = Config(config_path=config_path)
        return config_reader
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        raise e


# Load config
server_config_path = os.path.join(os.getcwd(), "config", "server.yaml")
config = Config(server_config_path)
server_config = config.get_server_config()
classification_config = config.get_classification_config()

if __name__ == "__main__":
    try:
        print("Classification Config:")
        print(classification_config)
        print("\nServer Config:")
        print(server_config)
    except Exception as e:
        logging.error(f"Failed to execute config_reader: {e}")
        raise e
