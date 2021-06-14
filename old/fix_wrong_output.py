#!/usr/bin/env python
"""
This script check if there are some output names in the
_outputs list that are not attributes of the protocol.
These 'missing' outputs will be removed from the list
to enable the project to open again.
"""
import sys, os

from pyworkflow.project import Manager
import pyworkflow.utils as pwutils


def usage(error):
    print """
    ERROR: %s

    Usage: scipion python fix_wrong_output.py PROJECT
        PROJECT: provide the project name
    """ % error
    sys.exit(1)

argc = len(sys.argv)

if argc != 2:
    usage("Incorrect number of input parameters")

projName = sys.argv[1]

manager = Manager()

if not manager.hasProject(projName):
    usage("Unexistent project: %s" % pwutils.red(projName))
    
project = manager.loadProject(projName)

for prot in project.getRuns(refresh=False):
    print(prot.getRunName())
    missingList = []
    for o in prot._outputs:
        missing = not prot.hasAttribute(o)
        print("   %s %s" % (o, 'MISSING' if missing else ''))
        if missing:
            missingList.append(o)
    if missingList:
        for o in missingList:
            prot._outputs.remove(o)
        print("   new output: %s" % prot._outputs)
        project.mapper.store(prot)

project.mapper.commit()



