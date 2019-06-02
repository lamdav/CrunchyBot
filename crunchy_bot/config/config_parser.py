import pathlib


class Config(object):
    def __init__(
        self,
        crunchy_username,
        crunchy_password,
        reddit_client_id,
        reddit_client_secret,
        reddit_user_agent,
        reddit_username,
        reddit_password,
        log_dir,
    ):
        self.crunchy_username = crunchy_username
        self.crunchy_password = crunchy_password
        self.reddit_client_id = reddit_client_id
        self.reddit_client_secret = reddit_client_secret
        self.reddit_user_agent = reddit_user_agent
        self.reddit_username = reddit_username
        self.reddit_password = reddit_password
        self.log_dir = log_dir

    def __eq__(self, other):
        if not isinstance(other, Config):
            return False
        return (
            self.crunchy_username == other.crunchy_username
            and self.crunchy_password == other.crunchy_password
            and self.reddit_client_id == other.reddit_client_id
            and self.reddit_client_secret == other.reddit_client_secret
            and self.reddit_user_agent == other.reddit_user_agent
            and self.reddit_username == other.reddit_username
            and self.reddit_password == other.reddit_password
            and self.log_dir == other.log_dir
        )

    def __hash__(self):
        return hash(
            (
                self.crunchy_username,
                self.crunchy_password,
                self.reddit_client_id,
                self.reddit_client_secret,
                self.reddit_user_agent,
                self.reddit_username,
                self.reddit_password,
                self.log_dir,
            )
        )


class ConfigParser(object):
    def parse(self, path: pathlib.Path) -> Config:
        """
        Given a path, parse and return a Config object with data.

        :param path: Path to configuration file to parse.
        :return: Config object with data from configuration file.
        """
        raise NotImplementedError("parse is not implemented")
