#!/usr/bin/env python3

import os
from typing import Any
from amitools.fs.rdb.RDisk import RDisk
from amitools.fs.blkdev.BlkDevFactory import BlkDevFactory 
from amitools.fs.blkdev.BlockDevice import BlockDevice 
from amitools.fs.blkdev.RawBlockDevice import RawBlockDevice
from amitools.fs.ADFSVolume import ADFSVolume
from dotenv import load_dotenv

load_dotenv()

# bdf = BlkDevFactory.BlkDevFactory()

# a = bdf.open(os.environ.get('ADF_PATH'), read_only=True)
# b = bdf.open(os.environ.get('HDF_PATH'), read_only=True)

RDB_IMG_PATH = os.path.join(os.environ.get('BASE_DIR'), 'testing', 'a600-2.1-workbench-rdb-3gb.hdf')


def open_rdb(path: str, read_only: bool=True) -> Any:
    bs = 512
    rawdev = RawBlockDevice(path, read_only, block_bytes=bs)
    rawdev.open()
    # check block size stored in rdb
    rdisk = RDisk(rawdev)
    rdb_bs = rdisk.peek_block_size()
    if rdb_bs != bs:
        # adjust block size and re-open
        rawdev.close()
        bs = rdb_bs
        rawdev = RawBlockDevice(path, read_only, block_bytes=bs)
        rawdev.open()
        rdisk = RDisk(rawdev)
    if not rdisk.open():
        raise IOError("can't open rdisk of image file")
    return rdisk



def open_img(path: str, read_only: bool=True) -> BlockDevice:
    bdf = BlkDevFactory()
    blk = bdf.open(path, read_only=read_only)
    return blk, ADFSVolume(blk)

rdb = open_rdb(RDB_IMG_PATH)

# badf, vadf = open_img(os.environ.get('ADF_PATH'))
# bhdf, vhdf = open_img(os.environ.get('HDF_PATH'))
# brdb, vrdb = open_img(RDB_IMG_PATH)