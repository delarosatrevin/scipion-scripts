#!/usr/bin/env python

"""
This scripts counts files and group by extension.
Initially developed to inspect files generated in a Scipion project.

"""

import os
import sys
import argparse

import pyworkflow.utils as pwutils


def get_parser():
    """ Return the argparse parser, so we can get the arguments """

    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument  # shortcut
    add('folder', help='Folder to analyze.')
    add('--sort_by_size', action='store_true', help='Sort by total size of files.')

    # g = parser.add_mutually_exclusive_group()
    # g.add_argument('--output_text', action='store_true', help="Write all set items to a text file.")
    # g.add_argument('--print', action='store_true', help="Print all set's item files to a text file.")
    # g.add_argument('--copy', action='store_true', help="Copy all set's item files to a text file.")

    #
    # add('output', metavar='OUTPUT', help='Output file or folder.')

    return parser


class ExtInfo:
    def __init__(self, ext):
        self.ext = ext
        self.files = []

    def add(self, f=None):
        self.files.append(f)

    def __len__(self):
        return len(self.files)

    def size(self):
        s = 0
        for f in self.files:
            s += pwutils.getFileSize(f)

        return s

    def __repr__(self):
        return "%s: %d (%s)" % (self.ext,
                                len(self),
                                pwutils.prettySize(self.size()))


def main():
    args = get_parser().parse_args()
    counter = {}

    for root, dirs, files in os.walk(args.folder):
        for f in files:
            name, ext = os.path.splitext(f)

            if not ext:
                continue

            filename = os.path.join(root, f)

            if not os.path.exists(filename):
                continue

            ext = ext.lower()
            if ext not in counter:
                counter[ext] = ExtInfo(ext)
            counter[ext].add(filename)

    def _sort_by_len(ei):
        return len(ei)

    def _sort_by_size(ei):
        return ei.size()

    keyfunc = _sort_by_size if args.sort_by_size else _sort_by_len

    for extInfo in sorted(counter.values(), key=keyfunc, reverse=True):
        print(extInfo)


if __name__ == "__main__":
    main()

