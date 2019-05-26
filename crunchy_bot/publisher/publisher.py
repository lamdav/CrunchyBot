from typing import Sequence


class Publisher(object):
    def publish(self, guest_passes: Sequence[str]) -> bool:
        """
        Given a sequence of guest passes, publish them to some location

        :param guest_passes: Sequence of Guest Pass strings.
        :return: True if and only if it was successful.
        """
        raise NotImplementedError("publish is not implemented")
