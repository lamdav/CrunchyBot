from typing import Sequence


class Fetcher(object):
    def fetch(self, debug: bool = False) -> Sequence[str]:
        raise NotImplementedError("fetch is not implemented")
