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


def test_parse(logger: Logger, json_config_parser: ConfigParser):
    with patch("crunchy_bot.config.json_config_parser.open", mock_open()) as open_mock:
        with patch(
            "crunchy_bot.config.json_config_parser.json", autospec=True
        ) as json_mock:
            data = {
                "crunchy_username": "crunchy_user",
                "crunchy_password": "crunchy_pass",
                "reddit_client_id": "client_id",
                "reddit_client_secret": "client_secret",
                "reddit_user_agent": "CrunchyBot:v4.0.0 (hosted by /u/{YOUR_USERNAME})",
                "reddit_username": "reddit_user",
                "reddit_password": "reddit_pass",
                "log_dir": "/tmp/crunchybot/logs",
            }
            json_mock.load.return_value = data

            config_path = Path.home()
            config = json_config_parser.parse(config_path)

            logger.info.assert_any_call("Fetching Account Data...")
            open_mock.assert_any_call(config_path.resolve().as_posix(), "r")
            logger.info.assert_any_call("Fetched Account Data")

            assert config == Config(**data)
