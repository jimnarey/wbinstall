#!/usr/bin/env python3

from typing import Any
from amitools.fs.FSString import FSString
from amitools.fs.rdb.RDisk import RDisk
from amitools.fs.blkdev.BlkDevFactory import BlkDevFactory 
from amitools.fs.blkdev.BlockDevice import BlockDevice
from amitools.fs.blkdev.HDFBlockDevice import HDFBlockDevice
from amitools.fs.blkdev.PartBlockDevice import PartBlockDevice 
from amitools.fs.blkdev.RawBlockDevice import RawBlockDevice
from amitools.fs.ADFSVolume import ADFSVolume

from amitoolhelpers.disk_geometry import AutoDiskGeometry


def open_rdb(path: str, read_only: bool=True) -> Any:
    bs: int = 512
    rawdev = RawBlockDevice(path, read_only, block_bytes=bs)
    rawdev.open()
    rdisk = RDisk(rawdev)
    rdb_bs = int(rdisk.peek_block_size()) # type: ignore
    if rdb_bs != bs:
        rawdev.close()
        rawdev = RawBlockDevice(path, read_only, block_bytes=rdb_bs)
        rawdev.open()
        rdisk = RDisk(rawdev)
    if not rdisk.open():
        raise IOError("Error opening rdisk")
    return rdisk


def create_raw_block_device(path: str, mbs: int) -> RawBlockDevice:
    geo = AutoDiskGeometry(mbs)
    blkdev = RawBlockDevice(path, block_bytes=geo.block_bytes)
    blkdev.create(geo.get_num_blocks())
    blkdev.geo = geo # type: ignore
    return blkdev

def create_rdisk(blkdev: BlockDevice) -> RDisk:
    rdisk = RDisk(blkdev)
    rdisk.create(blkdev.geo) # type: ignore
    return rdisk

def create_partition(rdisk: RDisk, name='DH0') -> PartBlockDevice:
    drive_name = FSString(name)
    rdisk.add_partition(drive_name, rdisk.get_cyl_range())
    blkdev = PartBlockDevice(rdisk.rawblk, rdisk.parts[0].part_blk)
    blkdev.open()
    return blkdev
     
def create_hdf(path, mbs) -> HDFBlockDevice:
    geo = AutoDiskGeometry(mbs)
    blkdev = HDFBlockDevice(path)
    blkdev.create(geo)
    blkdev.geo = geo
    return blkdev

def create_volume(blkdev: BlockDevice, name: str='Worbench', is_ffs: bool=True) -> ADFSVolume:
    vol = ADFSVolume(blkdev)
    vol.create(FSString(name), is_ffs=is_ffs)
    return vol

def open_image_file(path: str, read_only: bool=True) -> ADFSVolume:
    bdf = BlkDevFactory()
    try:
        blkdev = bdf.open(path, read_only=read_only)
    except Exception as e:
        print('Error opening {}: {}'.format(path, e))
        return None
    return blkdev
