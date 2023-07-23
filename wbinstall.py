#!/usr/bin/env python3

import os
import argparse
from dotenv import load_dotenv
# from tools import imgfile
from amitoolhelpers import volume_tree

load_dotenv()

# TODO - Move this to imgfile and create something similar for an hdf file
# (put thigs generating VolumeTrees or VolumeSets in that module)




def compare(args):
    
    adf_set = volume_tree.open_volumeset(args['adfdir'])
    hdf = volume_tree.open_volume(args['hdfpath'])
    breakpoint()


commands = {
    'compare': {'args': [{'name': 'adfdir'},
                         {'name': 'hdfpath'}],
                'handler': compare
                }
}


# adfb = imgfile.open_image_file(os.environ.get('ADF_PATH'))


# tree = VolumeTree(adfb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='WBinstall',
                    description='Installs Workbench to Amiga HDF from adf files',
                    epilog='Something something')
    subparsers = parser.add_subparsers(help='Subcommand help')
    for key in commands:
        subparser = subparsers.add_parser(key, help='{} help'.format(key))
        for arg in commands[key]['args']:
            subparser.add_argument(arg['name'], help='{} help'.format(arg['name']))
            subparser.set_defaults(func=commands[key]['handler'])

    args = parser.parse_args()
    args.func(vars(args))
    # breakpoint()