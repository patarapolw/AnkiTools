import pytest

from pathlib import Path


def pytest_logger_config(logger_config):
    logger_config.add_loggers(['debug'], stdout_level='debug')
    logger_config.add_loggers(['info'], stdout_level='notset')
    logger_config.add_loggers(['record'], stdout_level='notset')
    logger_config.set_log_option_default('debug,info,record')


def pytest_logger_logdirlink(config):
    return str(Path(__file__).parent.joinpath('logs').absolute())


@pytest.fixture(scope="module")
def module_path():
    return Path(__file__).parent
