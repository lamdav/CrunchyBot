import json
import pathlib
from typing import Optional

from crunchy_bot.config.config_parser import ConfigParser, Config
from crunchy_bot.logging.logger import Logger
from crunchy_bot.logging.noop_logger import NoopLogger


class JsonConfigParser(ConfigParser):
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger if logger is not None else NoopLogger()

    def parse(self, path: pathlib.Path) -> Config:
        self.logger.info("Fetching Account Data...")
        posix_path = path.resolve().as_posix()
        with open(posix_path, "r") as data_file:
            data_dictionary = json.load(data_file)

        crunchy_username = data_dictionary.get("crunchy_username", None)
        if crunchy_username is None:
            raise ValueError(f"Missing crunchy_username in {posix_path}")
        crunchy_password = data_dictionary.get("crunchy_password", None)
        if crunchy_password is None:
            raise ValueError(f"Missing crunchy_password in {posix_path}")
        reddit_client_id = data_dictionary.get("reddit_client_id", None)
        if reddit_client_id is None:
            raise ValueError(f"Missing reddit_client_id in {posix_path}")
        reddit_client_secret = data_dictionary.get("reddit_client_secret", None)
        if reddit_client_secret is None:
            raise ValueError(f"Missing reddit_client_secret in {posix_path}")
        reddit_user_agent = data_dictionary.get("reddit_user_agent", None)
        if reddit_user_agent is None:
            raise ValueError(f"Missing reddit_user_agent in {posix_path}")
        reddit_username = data_dictionary.get("reddit_username", None)
        if reddit_username is None:
            raise ValueError(f"Missing reddit_username in {posix_path}")
        reddit_password = data_dictionary.get("reddit_password", None)
        if reddit_password is None:
            raise ValueError(f"Missing reddit_password in {posix_path}")
        log_dir = data_dictionary.get("log_dir", None)
        if log_dir is None:
            raise ValueError(f"Missing log_dir in {posix_path}")

        self.logger.info("Fetched Account Data")

        return Config(
            crunchy_username=crunchy_username,
            crunchy_password=crunchy_password,
            reddit_client_id=reddit_client_id,
            reddit_client_secret=reddit_client_secret,
            reddit_user_agent=reddit_user_agent,
            reddit_username=reddit_username,
            reddit_password=reddit_password,
            log_dir=log_dir,
        )
