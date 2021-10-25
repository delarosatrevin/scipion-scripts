#!/usr/bin/env python

"""
This script loads the protocols from a project and export the workflow
 as a json file.

"""

import os
import json
import argparse


from pwem import Domain
import pyworkflow.protocol.params as pwparams
import pyworkflow.utils as pwutils
#from pwem.objects import SetOfMovies, EMSet


def get_parser():
    """ Return the argparse parser, so we can get the arguments """

    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument  # shortcut
    add('classname', metavar='CLASS NAME',
        help='Class name of the protocols to get definition from ')
    add('--output', '-o', metavar='OUTPUT',
        help='Output json file to store the definition.')

    # g = parser.add_mutually_exclusive_group()
    # g.add_argument('--output_text', action='store_true', help="Write all set items to a text file.")
    # g.add_argument('--print', action='store_true', help="Print all set's item files to a text file.")
    # g.add_argument('--copy', action='store_true', help="Copy all set's item files to a text file.")

    return parser


def printElement(param, spaces):
    print(spaces, "label: ", param.label)
    if isinstance(param, pwparams.ElementGroup):
        print(spaces, "group: ", param.getClassName())
        for name, subparam in param.iterParams():
            printElement(subparam, spaces + "   ")


def main():
    args = get_parser().parse_args()

    print("Finding class: ", args.classname)

    for key, prot in Domain.getProtocols().items():
        print("key: ", key, "class: ", prot)

    ProtClass = Domain.findClass(args.classname)
    prot = ProtClass()

    for section in prot.iterDefinitionSections():
        label = section.getLabel()
        print("Section: ", label)
        for name, param in section.iterParams():
            printElement(param, "   ")



if __name__ == "__main__":
    main()