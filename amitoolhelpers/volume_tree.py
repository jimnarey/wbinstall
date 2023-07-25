#!/usr/bin/env python3

import os
import hashlib
from functools import cached_property
from collections.abc import Iterable

from amitools.fs.ADFSDir import ADFSDir
from amitools.fs.ADFSFile import ADFSFile
from amitools.fs.blkdev.BlockDevice import BlockDevice
from amitools.fs.ADFSVolume import ADFSVolume

from tools import imgfile


class TreeNode:

    def __init__(self, adfsobj: ADFSDir | ADFSFile) -> None:
        self.obj = adfsobj
        self.sha256 = None
        if self.is_file():
            self._hash()

    def _check_open(self):
        self.obj.read()

    def _hash(self):
        self._check_open()
        sha256 = hashlib.sha256()
        sha256.update(self.obj.data)
        self.sha256 = sha256.hexdigest()
    
    def is_file(self):
        if isinstance(self.obj, ADFSFile):
            return True
        return False

    @cached_property
    def path(self):
        self._check_open()
        return os.path.join(*self.obj.get_node_path())
    
    @cached_property
    def parent_path(self):
        self._check_open()
        return self.obj.parent.get_node_path() or '/'
    
    @cached_property
    def child_paths(self):
        self._check_open()
        if hasattr(self.obj, 'entries'):
            return [os.path.join(*child.get_node_path()) for child in self.obj.entries]


class VolumeTree:

    def __init__(self, blkdev: BlockDevice):
        self.blkdev = blkdev
        self.volume = ADFSVolume(blkdev)
        self.volume.open()
        self.volume.root_dir.read(recursive=True)
        self.entries = []
        self._populate(self.volume.root_dir.entries)

    def _populate(self, root):
        for entry in root:
            entry.read()    
            if isinstance(entry, ADFSDir): 
                self._populate(entry.entries)
            self.entries.append(TreeNode(entry))

    @cached_property
    def dirs(self):
        return [item for item in self.entries if not item.is_file()]
    
    @cached_property
    def files(self):
        return [item for item in self.entries if item.is_file()]
    
    def get_by_hash(self, sha256):
        return [d for d in self.flat_tree if d['sha256'] == sha256]
    

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

    def _get_all(self, attribute):
        items = []
        for tree in self.trees:
            items += getattr(tree, attribute)
        return items

    @property
    def entries(self):
        return self._get_all('entries')

    @property
    def files(self):
        return self._get_all('files')
    
    @property
    def dirs(self):
        return self._get_all('dirs')



def open_volumeset(dir_path):
    blkdevs = []
    for root, _, files in os.walk(dir_path):
        for file in files:
            blkdevs.append(imgfile.open_image_file(os.path.join(root, file)))
    volume_set = VolumeSet(*blkdevs)
    return volume_set

def open_volume(img_path):
    blkdev = imgfile.open_image_file(img_path)
    return VolumeTree(blkdev)