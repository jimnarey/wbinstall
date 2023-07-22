#!/usr/bin/env python3

import os
from collections.abc import Iterable

from amitools.fs.ADFSDir import ADFSDir
from amitools.fs.ADFSFile import ADFSFile
from amitools.fs.blkdev.BlockDevice import BlockDevice
from amitools.fs.ADFSVolume import ADFSVolume


class VolumeTree:

    def __init__(self, blkdev: BlockDevice):
        self.blkdev = blkdev
        self.volume = ADFSVolume(blkdev)
        self.volume.open()
        self.volume.root_dir.read(recursive=True)
        self.entries = self.volume.root_dir.entries
        # self.flat_entries = [item for item in self.flatten(self.entries)]
        self.flat_entries = []
        self.paths = [item.name.get_unicode_name() for item in self.flat_entries]
        self.files = [item for item in self.flat_entries if isinstance(item, ADFSFile)]
        self.dirs = [item for item in self.flat_entries if isinstance(item, ADFSDir)]
        self.tree = {'name': self.volume.name.get_unicode(), 'entries': []}
        self.create_tree(self.entries, self.tree)


    # def flatten(self, root):
    #     for entry in root:
    #         if isinstance(entry, ADFSDir):
    #             entry.read()
    #             yield from self.flatten(entry.entries)
    #         print(entry)
    #         yield entry

    def create_tree(self, root, parent):
        for entry in root:
            tree_entry = {'name': entry.name.get_unicode_name(), 'path': os.path.join(*entry.get_node_path())}
            if isinstance(entry, ADFSDir):
                entry.read()
                tree_entry['entries'] = []
                self.create_tree(entry.entries, tree_entry)
            self.flat_entries.append(entry)
            parent['entries'].append(tree_entry)

    # def item_from_path(self, path):


    # def paths(self):
    #     for item in self.flat_entries:
    #         path = os.path.join(*item.get_node_path())
    #         print(path)
