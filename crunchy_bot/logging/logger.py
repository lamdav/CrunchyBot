from enum import Enum


class LogTag(Enum):
    SUCCESS = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4


class LogColor(Enum):
    SUCCESS = "green"
    INFO = "blue"
    WARN = "yellow"
    ERROR = "red"
    CRITICAL = "pink"
    LOG = "white"


class Logger(object):
    def success(self, message: str):
        """
        Success level logging

        :param message: message to log
        """
        raise NotImplementedError("success is not implemented")

    def info(self, message: str):
        """
        Info level logging

        :param message: message to log
        """
        raise NotImplementedError("info is not implemented")

    def warn(self, message: str):
        """
        Warn level logging

        :param message: message to log
        """
        raise NotImplementedError("warn is not implemented")

    def error(self, message: str):
        """
        Error level logging

        :param message: message to log
        """
        raise NotImplementedError("error is not implemented")

    def critical(self, message: str):
        """
        Critical level logging

        :param message: message to log
        """
        raise NotImplementedError("critical is not implemented")

    def log(self, tag: LogTag, message: str, color: LogColor):
        """
        Custom level logging

        :param message: message to log
        """
        raise NotImplementedError("log is not implemented")
