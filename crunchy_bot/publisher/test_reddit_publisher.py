from unittest import mock

import praw
import pytest

from crunchy_bot.logging.logger import Logger
from crunchy_bot.publisher.reddit_publisher import RedditPublisher


@pytest.fixture()
def client():
    return mock.MagicMock(name="reddit_mock")


@pytest.fixture()
def logger():
    return mock.create_autospec(Logger)


def test_publish(client: praw.Reddit, logger: Logger):
    username = "reddit_username"
    client.user.me.return_value = username
    subreddit_mock = mock.MagicMock(name="subreddit_mock")
    client.subreddit.return_value = subreddit_mock
    submission_mock = mock.MagicMock()
    submission_mock.title = "Unrelated post"
    guest_pass_submission_mock = mock.MagicMock()
    guest_pass_submission_mock.title = (
        "Weekly Guest Pass MegaThread for the week of May 27, 2019, "
        "Please use this thread to ask or give away Guest Passes."
    )
    subreddit_mock.hot.return_value = [submission_mock, guest_pass_submission_mock]

    publisher = RedditPublisher(client, logger=logger)
    guest_passes = ["123", "abc", "foo"]
    assert publisher.publish(guest_passes)

    logger.info.assert_any_call("Building Comment Text...")
    logger.info.assert_any_call("Built Comment Text")
    logger.info.assert_any_call(f"Logged in as {username}...")
    client.user.me.assert_any_call()
    client.subreddit.assert_any_call("Crunchyroll")
    guest_pass_submission_mock.reply.assert_any_call(
        "Here are some valid passes:  \n\n"
        " * 123\n"
        " * abc\n"
        " * foo\n"
        "  \n*Disclaimer: This is a bot. Here is a [link](https://github.com/lamdaV/CrunchyBot/tree/master) for more detail.*"
    )
