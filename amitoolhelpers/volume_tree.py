#!/usr/bin/env python3

import os
import hashlib
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
        self.flat_entries = []
        self.hashes = {}
        self.paths = {}
        self.tree = {'name': self.volume.name.get_unicode(), 'entries': []}        
        self.create_tree(self.entries, self.tree)
        

    def create_tree(self, root, parent):
        hash = hashlib.sha256()
        for entry in root:
            path = os.path.join(*entry.get_node_path())
            tree_entry = {'name': entry.name.get_unicode_name(), 'path': path}
            entry.read()
            if isinstance(entry, ADFSDir):    
                tree_entry['entries'] = []
                self.create_tree(entry.entries, tree_entry)
            else:
                hash.update(entry.data)
                digest = hash.hexdigest()
                tree_entry['sha256'] = digest
                self.hashes[digest] = entry
            self.paths[path] = entry
            self.flat_entries.append(entry)
            parent['entries'].append(tree_entry)

    def dirs(self):
        return [item for item in self.flat_entries if isinstance(item, ADFSDir)]
    
    def files(self):
        return [item for item in self.flat_entries if isinstance(item, ADFSFile)]