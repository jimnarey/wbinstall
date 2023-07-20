#!/usr/bin/env python3

from amitools.fs.blkdev.DiskGeometry import DiskGeometry


class AutoDiskGeometry(DiskGeometry):

    def __init__(self, mbs: int) -> None:
        super().__init__()
        self.size = None
        self._auto_set(mbs)

    def _auto_set(self, mbs: int) ->None:
        # TODO - handle this better
        mbs = mbs if mbs > 15 else 16
        size = mbs * 1024^2
        self.size = self._guess_for_size(size)

    def print(self):
        for key, value in self.__dict__.items():
            print('{}: {}'.format(key, value))
