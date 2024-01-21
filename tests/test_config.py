from mumar.utils.config import config


def test_config():
    assert config.LOG_LEVEL == "DEBUG"
