from mumar.utils.config import config
from mumar.utils.logger import create_logger


def test_config():
    assert config.LOG_LEVEL == "DEBUG"


def test_logger():
    logger = create_logger("test")
    assert logger.name == "test"
