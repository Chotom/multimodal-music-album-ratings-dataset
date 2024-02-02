from mumar.utils.config import config
from mumar.utils.logger import create_logger


def test_config():
    assert config.LOG_LEVEL == "DEBUG"


def test_logger():
    logger = create_logger("test")
    handlers_number = len(logger.handlers)
    logger2 = create_logger("test")

    assert logger == logger2
    assert logger2.name == "test"
    assert len(logger2.handlers) == handlers_number
