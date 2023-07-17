#!/usr/bin/env python3

import os
from amitools.fs.blkdev import BlkDevFactory, BlockDevice
from dotenv import load_dotenv

load_dotenv()

bdf = BlkDevFactory.BlkDevFactory()

a = bdf.open(os.environ.get('ADF_PATH'), read_only=True)
b = bdf.open(os.environ.get('HDF_PATH'), read_only=True)


def open_img_file(path: str) -> BlockDevice:
    pass