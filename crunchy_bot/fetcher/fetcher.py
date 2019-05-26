from typing import Sequence


class Fetcher(object):
    def fetch(self, debug: bool = False) -> Sequence[str]:
        """
        Return a sequence of Guest Pass strings.

        :param debug: Enable debugging mode. It is up to the implementor to define what this means.
        :return: Sequence of Guest Pass strings.
        """
        raise NotImplementedError("fetch is not implemented")
