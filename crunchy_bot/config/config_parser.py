import pathlib


class Config(object):
    def __init__(self, crunchy_username, crunchy_password, reddit_client_id, reddit_client_secret, reddit_user_agent,
                 reddit_username, reddit_password, log_dir):
        self.crunchy_username = crunchy_username
        self.crunchy_password = crunchy_password
        self.reddit_client_id = reddit_client_id
        self.reddit_client_secret = reddit_client_secret
        self.reddit_user_agent = reddit_user_agent
        self.reddit_username = reddit_username
        self.reddit_password = reddit_password
        self.log_dir = log_dir


class ConfigParser(object):
    def parse(self, path: pathlib.Path) -> Config:
        """
        Given a path, parse and return a Config object with data.

        :param path: Path to configuration file to parse.
        :return: Config object with data from configuration file.
        """
        raise NotImplementedError("parse is not implemented")
