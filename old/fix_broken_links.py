#!/usr/bin/env python

"""
Fix broken links to input raw movies.
"""

import os
import argparse


class Main:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Create movie stacks from the individual "
                        "frame files.")
        add = parser.add_argument  # shortcut
        add('inputPath', default='',
            help='Input path where the broken links are. '
                 'Usually something like: ~/ScipionUserData/projects/ProjectA/Runs/000002_ProtImportMovies/extra')
        add('rawDataPath',
            help='Where the raw movies are located. The last directoy name of this value should be'
                 'contained in the name of the link files. If not, you should provide the --root_prefix parameter.')
        add('--root_prefix',
            help='')

        add('--absolute', action='store_true',
            help='Provide this option if you want to create absolute links. '
                 'By default relative links are created to the raw data path. ')
            
        args = parser.parse_args()
        rawDataPath = args.rawDataPath.rstrip('/')
        rawDataFolder = os.path.basename(rawDataPath)

        if not os.path.exists(args.inputPath):
            raise Exception("Input path '%s' does not exists. " % args.inputPath)

        if not os.path.exists(args.rawDataPath):
            raise Exception("Raw data path '%s' does not exists. " % args.rawDataPath)

        broken_links = [f for f in os.listdir(args.inputPath)]

        dataFolderDst = os.path.join(args.inputPath, rawDataFolder)
        if args.absolute:
            dataFolderSource = os.path.abspath(rawDataPath)
        else:
            dataFolderSource = os.path.relpath(os.path.realpath(rawDataPath),
                                               os.path.realpath(dataFolderDst))

        print("Creating link to raw data folder...")
        print("%s -> %s" % (dataFolderDst, dataFolderSource))
        os.symlink(dataFolderSource, dataFolderDst)

        for fn in broken_links:
            path = os.path.join(args.inputPath, fn)
            if os.path.islink(path):
                targetPath = os.readlink(path)

                parts = targetPath.split('/')
                if rawDataFolder in parts:
                    i = parts.index(rawDataFolder)
                    newTargetPath = '/'.join(parts[i:])
                    os.remove(path)
                    # Create the new link pointing to the new location
                    os.symlink(newTargetPath, path)

                print("%s \n   -> %s\n   -> %s\n" % (path, targetPath, newTargetPath))


if __name__ == "__main__":
    Main()
