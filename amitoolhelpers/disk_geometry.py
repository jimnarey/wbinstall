#!/usr/bin/env python3

import math

from amitools.fs.blkdev.DiskGeometry import DiskGeometry


class AutoDiskGeometry(DiskGeometry):

    def __init__(self, mbs: int) -> None:
        super().__init__()
        self.mbs = mbs
        self.size = mbs * 1024 * 1024
        self.block_bytes = 512
        self.secs = 32
        self.heads = None
        self.cyls = None
        
        self.get_chs()

    def print(self):
        for key, value in self.__dict__.items():
            print('{}: {}'.format(key, value))

    def get_cylinders(self, cyl_size):
        tracks = self.size / cyl_size
        cyls = 1024
        heads = tracks / cyls
        if heads < 2:
            while (heads < 2):
                cyls = cyls - 1
                heads = int(tracks / cyls)
        return cyls
                

    def get_chs(self):
        if self.mbs < 1:
            return None
        cyl_size = self.secs * self.block_bytes # 16384
        self.cyls = int(self.get_cylinders(cyl_size))
        self.heads = int(math.ceil(self.size / (cyl_size * self.cyls)))

