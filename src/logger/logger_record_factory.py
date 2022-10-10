from logging import getLogger, setLoggerClass, getLogRecordFactory, setLogRecordFactory
from logging import Formatter, StreamHandler, getLogger
from logging import INFO

def setup_logger(name: str, fmt: str):

    formatter = Formatter(fmt)
    handler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(formatter)

    _logger = getLogger(name)
    _logger.addHandler(handler)
    _logger.setLevel(INFO)

    return _logger


current_factory = getLogRecordFactory()


