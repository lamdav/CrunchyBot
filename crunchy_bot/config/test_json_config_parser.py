import os
from pathlib import Path
from unittest import mock
from unittest.mock import mock_open, patch

import pytest

from crunchy_bot.config.config_parser import ConfigParser, Config
from crunchy_bot.config.json_config_parser import JsonConfigParser
from crunchy_bot.logging.logger import Logger


@pytest.fixture()
def logger() -> Logger:
    return mock.create_autospec(Logger)


@pytest.fixture()
def json_config_parser(logger: Logger) -> ConfigParser:
    return JsonConfigParser(logger=logger)


@pytest.fixture()
def config_data() -> dict:
    return {
        "crunchy_username": "crunchy_user",
        "crunchy_password": "crunchy_pass",
        "reddit_client_id": "client_id",
        "reddit_client_secret": "client_secret",
        "reddit_user_agent": "CrunchyBot:v4.0.0 (hosted by /u/{YOUR_USERNAME})",
        "reddit_username": "reddit_user",
        "reddit_password": "reddit_pass",
        "log_dir": "/tmp/crunchybot/logs",
    }


def test_parse(logger: Logger, json_config_parser: ConfigParser, config_data: dict):
    with patch("crunchy_bot.config.json_config_parser.open", mock_open()) as open_mock:
        with patch("crunchy_bot.config.json_config_parser.json") as json_mock:
            json_mock.load.return_value = config_data

            config_path = Path.home()
            config = json_config_parser.parse(config_path)

            logger.info.assert_any_call("Fetching Account Data...")
            open_mock.assert_any_call(config_path.resolve().as_posix(), "r")
            json_mock.load.assert_called()
            logger.info.assert_any_call("Fetched Account Data")

            assert config == Config(**config_data)


def test_parse_file_not_found_exception(
    logger: Logger, json_config_parser: ConfigParser, config_data: dict
):
    with patch("crunchy_bot.config.json_config_parser.open", mock_open()) as open_mock:
        with patch("crunchy_bot.config.json_config_parser.json") as json_mock:
            open_mock.side_effect = FileNotFoundError

            for k, v in config_data.items():
                os.environ[k.upper()] = v

            config_path = Path.home()
            config = json_config_parser.parse(config_path)

            logger.info.assert_any_call("Fetching Account Data...")
            open_mock.assert_any_call(config_path.resolve().as_posix(), "r")
            logger.info.assert_any_call("Fetched Account Data")
            json_mock.load.assert_not_called()

            assert config == Config(**config_data)
