import json

class ConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.config = {}
            self.initialized = True

    def load(self, filename):
        import os

        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist")

        try:
            with open(filename, "r") as config_file:
                self.config = json.load(config_file)

        except json.decoder.JSONDecodeError as e:
            raise json.decoder.JSONDecodeError(
                f"Invalid JSON file {filename}: {e.msg}",
                e.doc,
                e.pos
            )

    def get_config(self, key):

        parts = key.split(".")
        current_config = self.config

        for part in parts:

            if not isinstance(current_config, dict):
                return None

            if part not in current_config:
                return None

            current_config = current_config[part]

        return current_config


