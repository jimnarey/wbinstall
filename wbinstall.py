#!/usr/bin/env python3

import os
import argparse
import hashlib
from dotenv import load_dotenv
# from tools import imgfile
from amitoolhelpers import volume_tree

from pprint import pprint as pp

load_dotenv()

def compare(args):
    adf_set = volume_tree.open_volumeset(args['adfdir'])
    hdf = volume_tree.open_volume(args['hdfpath'])
    both, source_only, comparator_only = hdf.compare(adf_set)
    print('both: ', len(both))
    print('source only: ', len(source_only))
    print('comparator_only: ', len(comparator_only))
    # for e in source_only:
    #     print(e.path)


commands = {
    'compare': {'args': [{'name': 'adfdir'},
                         {'name': 'hdfpath'}],
                'handler': compare
                }
}


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