import logging

from logger import LoggerManager


def setup_function():
    LoggerManager._loggers.clear()


def test_same_logger_is_reused():
    logger1 = LoggerManager.get_logger("payment")
    logger2 = LoggerManager.get_logger("payment")

    assert logger1 is logger2


def test_different_logger_names():
    payment_logger = LoggerManager.get_logger("payment")
    user_logger = LoggerManager.get_logger("user")

    assert payment_logger is not user_logger


def test_logger_level():
    logger = LoggerManager.get_logger("test_logger")

    assert logger.level == logging.INFO


def test_logger_has_handler():
    logger = LoggerManager.get_logger("test_logger")

    assert len(logger.handlers) > 0
    assert isinstance(logger.handlers[0], logging.StreamHandler)