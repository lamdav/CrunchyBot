from typing import Sequence


class Publisher(object):
    def publish(self, guest_passes: Sequence[str]) -> bool:
        raise NotImplementedError("publish is not implemented")
