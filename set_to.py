#!/usr/bin/env python

"""
This scripts read a .sqlite file that contains some image set
and allow to do the following operations:
1) create a text file with all filenames.
2) copy all files to a given folder.

"""

import os
import sys
import argparse

from pwem.objects import SetOfMovies, EMSet
import pyworkflow.utils as pwutils


def get_parser():
    """ Return the argparse parser, so we can get the arguments """

    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument  # shortcut
    add('setFile', metavar='SQLITE_FILE', help='Sqlite file from the set.')

    g = parser.add_mutually_exclusive_group()
    g.add_argument('--output_text', action='store_true', help="Write all set items to a text file.")
    g.add_argument('--print', action='store_true', help="Print all set's item files to a text file.")
    g.add_argument('--copy', action='store_true', help="Copy all set's item files to a text file.")
    g.add_argument('--check_dims', action='store_true', help='Check images dimensions')

    add('output', metavar='OUTPUT', help='Output file or folder.')

    return parser


def main():
    # Get arguments.
    args = get_parser().parse_args()

    setObj = EMSet(filename=args.setFile)
    firstItem = setObj.getFirstItem()
    root = pwutils.findRootFrom(args.setFile, firstItem.getFileName())
    print("ROOT: ", root)

    if args.output_text:
        with open(args.output, 'w') as f:
            for movie in setObj:
                f.write('%s\n' % movie.getFileName())
    elif args.print:
        for item in setObj:
            print(item.getFileName())
    elif args.copy:
        for item in setObj:
            fn = os.path.join(root, item.getFileName())
            print('Copying %s to %s' % (fn, args.output))
            pwutils.copyFile(fn, args.output)

    elif args.check_dims:
        from pwem.emlib.image import ImageHandler
        ih = ImageHandler()

        counter = {}

        for item in setObj:
            fn = os.path.join(root, item.getFileName())
            dims = ih.getDimensions(fn)
            counter[dims] = 1 if dims not in counter else counter[dims] + 1
            print('%s: %s' % (os.path.basename(fn), dims))

        pwutils.prettyDict(counter)


if __name__ == "__main__":
    main()

