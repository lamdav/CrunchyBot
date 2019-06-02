import pathlib
from typing import Any
from unittest import mock
from unittest.mock import patch

import pytest
from selenium.webdriver.common.keys import Keys

from crunchy_bot.config.config_parser import Config
from crunchy_bot.fetcher.guest_pass_fetcher import GuestPassFetcher
from crunchy_bot.logging.logger import Logger


@pytest.fixture()
def config() -> Config:
    return Config(
        crunchy_username="username",
        crunchy_password="password",
        reddit_client_id="",
        reddit_client_secret="",
        reddit_user_agent="",
        reddit_username="",
        reddit_password="",
        log_dir="/path/to/logdir",
    )


@pytest.fixture()
def logger() -> Logger:
    return mock.create_autospec(Logger)


class Row(object):
    def __init__(
        self,
        created_at: str,
        guest_pass: str,
        description: str,
        status: str,
        expiration: str,
        redeemer: str,
        action: str,
    ):
        self.cells = [
            Cell(created_at),
            Cell(guest_pass),
            Cell(description),
            Cell(status),
            Cell(expiration),
            Cell(redeemer),
            Cell(action),
        ]


class Cell(object):
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"Cell text={self.text}"


@patch("crunchy_bot.fetcher.guest_pass_fetcher.WebDriverWait", autospec=True)
@patch("crunchy_bot.fetcher.guest_pass_fetcher.webdriver", autospec=True)
@patch("crunchy_bot.fetcher.guest_pass_fetcher.Options", autospec=True)
@patch("crunchy_bot.fetcher.guest_pass_fetcher.pathlib", autospec=True)
def test_fetch(
    pathlib_mock, options_mock, webdriver_mock, webdriver_wait_mock, config, logger
):
    path_mock = mock.create_autospec(pathlib.Path)
    pathlib_mock.Path.return_value = path_mock
    path_mock.exists.return_value = True
    path_mock.joinpath.return_value = path_mock
    log_path = f"{config.log_dir}/chrome.log"
    path_mock.as_posix.return_value = log_path
    driver_mock = webdriver_mock.Chrome()
    table_mock = mock.MagicMock()
    guest_pass_tables = [table_mock]
    driver_mock.find_elements_by_class_name.return_value = guest_pass_tables
    valid_row_mock = mock.MagicMock()
    invalid_row_mock = mock.MagicMock()
    table_mock.find_elements_by_tag_name.return_value = [
        valid_row_mock,
        invalid_row_mock,
    ]
    valid_guest_pass = "abcd123"
    valid_row = Row(
        created_at="1/1/2000",
        guest_pass=valid_guest_pass,
        description="description",
        status="Valid",
        expiration="1/2/2000",
        redeemer="",
        action="",
    )
    valid_row_mock.find_elements_by_tag_name.return_value = valid_row.cells
    invalid_row = Row(
        created_at="12/30/1999",
        guest_pass="invalid",
        description="description",
        status="Expired",
        expiration="12/31/1999",
        redeemer="",
        action="",
    )
    invalid_row_mock.find_elements_by_tag_name.return_value = invalid_row.cells

    fetcher = GuestPassFetcher(config, logger=logger)
    assert fetcher.fetch() == [valid_guest_pass]

    logger.info.assert_any_call("Fetching Guest Passes...")
    pathlib_mock.Path.assert_any_call(config.log_dir)
    path_mock.mkdir.assert_not_called()
    options_mock.assert_any_call()
    options_mock().add_argument.assert_any_call(f"--log-path={log_path}")
    options_mock().add_argument.assert_any_call("--headless")
    webdriver_mock.Chrome.assert_any_call(options=options_mock())
    driver_mock.get.assert_any_call("https://www.crunchyroll.com/login?next=%2F")
    webdriver_wait_mock.assert_any_call(driver_mock, 20)
    # EC does not implement __eq__ or __hash__
    webdriver_wait_mock(driver_mock, 20).until.assert_called()
    webdriver_wait_mock(driver_mock, 20).until(Any).send_keys.assert_any_call(
        config.crunchy_username
    )
    webdriver_wait_mock(driver_mock, 20).until(Any).send_keys.assert_any_call(
        config.crunchy_password
    )
    webdriver_wait_mock(driver_mock, 20).until(Any).send_keys.assert_any_call(
        Keys.ENTER
    )
    driver_mock.quit.assert_not_called()
    driver_mock.get.assert_any_call(
        "https://www.crunchyroll.com/acct/?action=guestpass"
    )
    driver_mock.close.assert_any_call()
    logger.info.assert_any_call("Fetched Guest Passes")
