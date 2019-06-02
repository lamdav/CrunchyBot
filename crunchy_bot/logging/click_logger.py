import click

from crunchy_bot.logging.logger import Logger, LogTag, LogColor


class ClickLogger(Logger):
    """
    Logger that uses click logging utilities to log to stdout.
    Format in the form of:
        [ TAG ] MESSAGE
    """

    def success(self, message: str):
        self.log(LogTag.SUCCESS, message, LogColor.SUCCESS)

    def info(self, message: str):
        self.log(LogTag.INFO, message, LogColor.INFO)

    def warn(self, message: str):
        self.log(LogTag.WARN, message, LogColor.WARN)

    def error(self, message: str):
        self.log(LogTag.ERROR, message, LogColor.ERROR)

    def critical(self, message: str):
        self.log(LogTag.CRITICAL, message, LogColor.CRITICAL)

    def log(self, tag: LogTag, message: str, color: LogColor):
        click.secho(f"[ {tag.name[:4]} ] {message}", fg=color.value)
