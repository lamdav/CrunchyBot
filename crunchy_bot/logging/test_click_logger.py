from typing import Callable
from unittest.mock import patch

import click
import pytest

from crunchy_bot.logging.click_logger import ClickLogger
from crunchy_bot.logging.logger import LogColor, Logger, LogTag


@pytest.fixture()
def click_logger():
    return ClickLogger()


def test_success(click_logger: Logger):
    run_test(click_logger.success, "testing", LogTag.SUCCESS, LogColor.SUCCESS)


def test_info(click_logger: Logger):
    run_test(click_logger.info, "testing", LogTag.INFO, LogColor.INFO)


def test_warn(click_logger: Logger):
    run_test(click_logger.warn, "testing", LogTag.WARN, LogColor.WARN)


def test_error(click_logger: Logger):
    run_test(click_logger.error, "testing", LogTag.ERROR, LogColor.ERROR)


def test_critical(click_logger: Logger):
    run_test(click_logger.critical, "testing", LogTag.CRITICAL, LogColor.CRITICAL)


@patch("crunchy_bot.logging.click_logger.click", autospec=True)
def test_log(click_mock: click, click_logger: Logger):
    tag, message, color = LogTag.INFO, "testing", LogColor.CRITICAL
    click_logger.log(tag, message, color)
    click_mock.secho.assert_called_with(f"[ {tag.name[:4]} ] {message}", fg=color.value)


def run_test(
    logging_method: Callable[[str], None], message: str, tag: LogTag, color: LogColor
):
    with patch("crunchy_bot.logging.click_logger.click", autospec=True) as click_mock:
        logging_method(message)
        click_mock.secho.assert_called_with(
            f"[ {tag.name[:4]} ] {message}", fg=color.value
        )
