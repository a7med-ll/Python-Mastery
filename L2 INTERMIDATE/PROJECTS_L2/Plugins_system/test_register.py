import pytest
from register import PLUGIN_REGISTRY, plugin, run_plugin

def setup_function():
    PLUGIN_REGISTRY.clear()

def test_plugin_registration():

    @plugin("test")
    def test():
        pass

    assert "test" in PLUGIN_REGISTRY
    assert PLUGIN_REGISTRY["test"] is test

def test_run_plugin():

    @plugin("test_1")
    def test_1():
        return "test_1 done"

    result = run_plugin("test_1")
    assert result == "test_1 done"

def test_plugin_arguments():

    @plugin("add")
    def add(a, b):
        return a + b

    result = run_plugin("add", 5, 10)

    assert result == 15

def test_missing_plugin():
    with pytest.raises(KeyError):
        run_plugin("missing_plugin")
