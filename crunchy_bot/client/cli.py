import json
import pathlib

import click
import praw
from prawcore import OAuthException
from selenium.common.exceptions import NoSuchElementException

from crunchy_bot.client.version import version as v
from crunchy_bot.config.json_config_parser import JsonConfigParser
from crunchy_bot.fetcher.guest_pass_fetcher import GuestPassFetcher
from crunchy_bot.logging.click_logger import ClickLogger
from crunchy_bot.publisher.reddit_publisher import RedditPublisher


class Context(object):
    def __init__(self):
        self.logger = ClickLogger()


@click.group()
@click.pass_context
def cli(context):
    context.obj = Context()


@cli.command()
@click.pass_obj
def init(context):
    """
    Initialize CrunchyBot's credentials file.
    """
    crunchy_username = click.prompt("Crunchyroll Username")
    crunchy_password = click.prompt("Crunchyroll Password", hide_input=True)
    reddit_client_id = click.prompt("Reddit Client ID")
    reddit_client_secret = click.prompt("Reddit Client Secret", hide_input=True)
    reddit_username = click.prompt("Reddit Username")
    reddit_user_agent = click.prompt(
        "Reddit User Agent",
        default=f"CrunchyBot:v4.0.0 (hosted by /u/{reddit_username})",
        show_default=True,
    )
    reddit_password = click.prompt("Reddit Password", hide_input=True)
    log_dir = click.prompt(
        "Log output directory", default="/tmp/crunchybot/logs", show_default=True
    )
    config_path = click.prompt(
        "Where to save config",
        default=pathlib.Path.home().joinpath(".crunchybot").as_posix(),
        show_default=True,
    )

    config = dict(
        crunchy_username=crunchy_username,
        crunchy_password=crunchy_password,
        reddit_client_id=reddit_client_id,
        reddit_client_secret=reddit_client_secret,
        reddit_user_agent=reddit_user_agent,
        reddit_username=reddit_username,
        reddit_password=reddit_password,
        log_dir=log_dir,
    )

    config_path = pathlib.Path(config_path).resolve()
    if config_path.exists():
        if config_path.is_dir():
            context.logger.error(f"{config_path.as_posix()} is a directory")
            exit(1)
        else:
            overwrite = click.confirm(
                f"Overwrite {config_path.as_posix()}", default=False, show_default=True
            )
            if not overwrite:
                exit(1)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=True)


@cli.command()
@click.option(
    "--config",
    type=click.Path(exists=True),
    default=pathlib.Path.home().joinpath(".crunchybot").as_posix(),
)
@click.option("--debug", "-d", type=bool, is_flag=True, default=False)
@click.pass_obj
def publish(context: Context, config: str, debug: bool):
    """
    Searches for Guest Passes and publishes it to reddit.
    """
    logger = context.logger
    data_path = pathlib.Path(config)

    config_parser = JsonConfigParser(logger=logger)
    config = None
    try:
        config = config_parser.parse(data_path)
    except ValueError as e:
        logger.error(f"Failed to parse config: {str(e)}")
        exit(1)

    fetcher = GuestPassFetcher(config, logger=logger)
    guest_passes = []
    try:
        guest_passes.extend(fetcher.fetch(debug=debug))

        if len(guest_passes) == 0:
            logger.info("No valid Guest Passes to publish")
            exit(0)
        logger.info(f"Received Guest Passes: {guest_passes}")
    except NoSuchElementException:
        logger.error(
            "Failed to fetch Guest Passes. Please check your Crunchyroll credentials."
        )
        exit(1)

    client = praw.Reddit(
        client_id=config.reddit_client_id,
        client_secret=config.reddit_client_secret,
        user_agent=config.reddit_user_agent,
        username=config.reddit_username,
        password=config.reddit_password,
    )
    publisher = RedditPublisher(client, logger=logger)

    try:
        logger.info("Publishing Guest Passes to Reddit...")
        if publisher.publish(guest_passes):
            logger.info("Published Guest Passes to Reddit")
        else:
            logger.warn("Failed to find thread to publish to Reddit")
    except OAuthException as e:
        logger.error(f"Failed to login to Reddit: {str(e)}")
        exit(1)


@cli.command()
@click.pass_obj
def version(context: Context):
    logger = context.logger
    logger.info(f"crunchy_bot {v}")
