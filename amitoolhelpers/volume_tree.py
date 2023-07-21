#!/usr/bin/env python3

from collections.abc import Iterable

from amitools.fs.ADFSDir import ADFSDir
from amitools.fs.blkdev.BlockDevice import BlockDevice
from amitools.fs.ADFSVolume import ADFSVolume


class VolumeTree:

    def __init__(self, blkdev: BlockDevice):
        self.blkdev = blkdev
        self.volume = ADFSVolume(blkdev)
        self.volume.open()
        self.volume.root_dir.read(recursive=True)
        self.entries = self.volume.root_dir.entries
        self.flat_entries = [item for item in self.flatten(self.entries)]
        # self.files = [item for item in self.flat_entries if ]


    def flatten(self, root):
        for entry in root:
            if isinstance(entry, ADFSDir):
                entry.read()
                yield from self.flatten(entry.entries)
            else:
                print(entry)
                yield entry