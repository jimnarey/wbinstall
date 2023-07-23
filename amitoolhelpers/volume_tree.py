#!/usr/bin/env python3

import os
import hashlib
from collections.abc import Iterable

from amitools.fs.ADFSDir import ADFSDir
from amitools.fs.ADFSFile import ADFSFile
from amitools.fs.blkdev.BlockDevice import BlockDevice
from amitools.fs.ADFSVolume import ADFSVolume

from tools import imgfile

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
        self._populate(self.entries, self.tree)
        

    def _populate(self, root, parent):
        hash = hashlib.sha256()
        for entry in root:
            path = os.path.join(*entry.get_node_path())
            tree_entry = {'name': entry.name.get_unicode_name(), 'path': path}
            entry.read()
            if isinstance(entry, ADFSDir):    
                tree_entry['entries'] = []
                self._populate(entry.entries, tree_entry)
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
    

class VolumeSet:

    def __init__(self, *args) -> None:
        self.trees = []
        for arg in args:
            self.add(arg)

    def add(self, blkdev):
        try:
            self.trees.append(VolumeTree(blkdev))
        except Exception as e:
            print('Error creating volume from {}: {}'.format(blkdev, e))
    
    @property
    def hashes(self):
        hashes = {}
        for tree in self.trees:
            hashes.update(tree.hashes)
        return hashes

    @property
    def paths(self):
        paths = {}
        for tree in self.trees:
            paths.update(tree.paths)
        return paths


def open_volumeset(dir_path):
    blkdevs = []
    for _, __, files in os.walk(dir_path):
        for file in files:
            blkdevs.append(imgfile.open_image_file(file))
    volume_set = VolumeSet(*blkdevs)
    return volume_set

def open_volume(img_path):
    blkdev = imgfile.open_image_file(img_path)
    return VolumeTree(blkdev)