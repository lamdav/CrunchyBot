from crunchy_bot.logging.logger import Logger


class NoopLogger(Logger):
    """
    Logger that noops (passes) every call.
    """

    def success(self, message: str):
        pass

    def info(self, message: str):
        pass

    def warn(self, message: str):
        pass

    def error(self, message: str):
        pass

    def critical(self, message: str):
        pass

    def log(self, tag: str, message: str, color: str):
        pass
