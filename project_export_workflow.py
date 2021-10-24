#!/usr/bin/env python

"""
This script loads the protocols from a project and export the workflow
 as a json file.

"""

import os
import json
import argparse


from pyworkflow.project import Manager
import pyworkflow.utils as pwutils
#from pwem.objects import SetOfMovies, EMSet


def get_parser():
    """ Return the argparse parser, so we can get the arguments """

    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument  # shortcut
    add('project', metavar='PROJECT_NAME',
        help='Project from where to export the workflow.')
    add('--output', '-o', metavar='OUTPUT',
        help='Output json file to store the workflow.')
    add('--include_classes', action='store_true',
        help='Include class names in the json file.')

    # g = parser.add_mutually_exclusive_group()
    # g.add_argument('--output_text', action='store_true', help="Write all set items to a text file.")
    # g.add_argument('--print', action='store_true', help="Print all set's item files to a text file.")
    # g.add_argument('--copy', action='store_true', help="Copy all set's item files to a text file.")

    return parser


def main():
    args = get_parser().parse_args()
    projName = args.project

    # Create a manager and load the project
    manager = Manager()

    cwd = os.getcwd()  # Keep current directory to restore it later
    project = manager.loadProject(projName)

    # Export protocols as a dict
    jsonDict = project.getProtocolsDict()

    os.chdir(cwd)  # Restore after project load

    if args.output:
        print("Writing workflow to file: ", args.output)
        with open(args.output, 'w') as f:
            json.dump(list(jsonDict.values()), f, indent=4, separators=(',', ': '))
    else:
        print(json.dumps(list(jsonDict.values()), indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()