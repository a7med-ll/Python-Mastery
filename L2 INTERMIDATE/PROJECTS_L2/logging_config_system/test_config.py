import json

import pytest

from config import ConfigManager


def setup_function():
    ConfigManager._instance = None


def test_config_singleton():
    config1 = ConfigManager()
    config2 = ConfigManager()

    assert config1 is config2


def test_config_load(tmp_path):
    test_data = {
        "app_name": "TestApp",
        "database": {
            "host": "test-host",
            "port": 1234
        }
    }

    config_file = tmp_path / "test_config.json"

    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(test_data, file)

    config = ConfigManager()
    config.load(config_file)

    assert config.get_config("app_name") == "TestApp"
    assert config.get_config("database.host") == "test-host"
    assert config.get_config("database.port") == 1234


def test_missing_config_key(tmp_path):
    test_data = {
        "app_name": "TestApp"
    }

    config_file = tmp_path / "test_config.json"

    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(test_data, file)

    config = ConfigManager()
    config.load(config_file)

    assert config.get_config("database.password") is None


def test_missing_config_file():
    config = ConfigManager()

    with pytest.raises(FileNotFoundError):
        config.load("missing_config.json")

