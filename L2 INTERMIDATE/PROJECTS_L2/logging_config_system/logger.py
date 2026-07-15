import logging

class LoggerManager:
    _loggers = {}

    @classmethod
    def get_logger(cls, name):

        if name in cls._loggers:
            return cls._loggers[name]

        else:

            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            logger.propagate = False

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '%(asctime)s | %(name)s |  %(levelname)s | %(message)s')

            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            cls._loggers[name] = logger
            return logger
