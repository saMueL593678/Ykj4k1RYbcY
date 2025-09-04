# 代码生成时间: 2025-09-05 06:19:07
# config_manager.py
# This module provides a configuration manager using Falcon framework

import falcon
import json
import yaml

# Define a custom error handler for configuration errors
class ConfigNotFoundError(falcon.HTTPError):
    def __init__(self, message):
        super().__init__(falcon.HTTP_404, 'Configuration Not Found', message)

class ConfigManager:
    """Manages application configuration files in YAML format."""
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """Loads the configuration file from the provided path."""
        try:
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise ConfigNotFoundError(f"No configuration file found at {self.config_path}")
        except yaml.YAMLError as e:
            raise falcon.HTTPBadRequest(f"Invalid YAML format: {e}")

    def get_config(self):
        """Returns the entire configuration dictionary."""
        return self.config

    def get_config_value(self, key):
        """Returns a specific value from the configuration by key."""
        if key in self.config:
            return self.config[key]
        else:
            raise falcon.HTTPBadRequest(f"Configuration key not found: {key}")

# Falcon resource for handling configuration requests
class ConfigResource:
    def __init__(self, config_manager):
        self._config_manager = config_manager

    def on_get(self, req, resp):
        "