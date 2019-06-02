from typing import Sequence, Optional

import praw

from crunchy_bot.logging.logger import Logger
from crunchy_bot.logging.noop_logger import NoopLogger
from crunchy_bot.publisher.publisher import Publisher


class RedditPublisher(Publisher):
    def __init__(self, client: praw.Reddit, logger: Optional[Logger] = None):
        self.client = client
        self.logger = logger if logger is not None else NoopLogger()

    def publish(self, guest_passes: Sequence[str]) -> bool:
        comment = self._build_comment_text(guest_passes)
        return self._reddit_post(comment)

    def _build_comment_text(self, guest_passes: Sequence[str]) -> str:
        """
            Generates a Reddit formatted text to display the code.

            Args:
                guest_passes:      List of valid guest passes in String form
            Returns:
                String that has been formatted for Reddit submission.
        """
        self.logger.info("Building Comment Text...")

        text = "Here are some valid passes:  \n\n"
        for guest_pass in guest_passes:
            text += f" * {guest_pass}\n"
        text += (
            "  \n*Disclaimer: This is a bot. "
            "Here is a [link](https://github.com/lamdaV/CrunchyBot/tree/master) for more detail.*"
        )

        self.logger.info("Built Comment Text")

        return text

    def _reddit_post(self, comment_text: str) -> bool:
        """
            Post Guest Passes to Reddit on given user account.

            Args:
                comment_text:    Reddit formatted String to post.
            Returns:
                Boolean of completion status.
        """
        # Return boolean.
        submission_status = False

        # Bot login.
        self.logger.info(f"Logged in as {self.client.user.me()}...")

        # Navigate to subreddit.
        subreddit = self.client.subreddit("Crunchyroll")

        # Key words to look for.
        search_list = {"weekly", "guest", "pass", "megathread"}

        # Find weekly guest pass submission.
        for submission in subreddit.hot(limit=100):
            submission_text = submission.title.lower()
            has_search = all(string in submission_text for string in search_list)
            if has_search:
                submission.reply(comment_text)
                submission_status = True
                break

        return submission_status
