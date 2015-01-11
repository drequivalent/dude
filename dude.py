#!/usr/bin/python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import sys

def builddictionary(dirlist):
    """Builds an initial dictionary, just with directory name and its size. Returns a dictionary with list as a value."""
    init_dictionary={}
    for string in dirlist:
        splitstring=string.split("\t")
        if len(splitstring) == 2:
            init_dictionary[splitstring[1].strip("\n")] = [int(splitstring[0]), 0]
    return init_dictionary

def addtodictionary(dict, dirlist):
    """Builds an intermediate dictionary, with directory names and their old and new sizes. Returns a dictionary with list as a value."""
    for string in dirlist:
        splitstring=string.split("\t")
        if len(splitstring) == 2:
            if splitstring[1].strip("\n") in dict:
                dict[splitstring[1].strip("\n")][1] = int(splitstring[0])
            else:
                dict[splitstring[1].strip("\n")] = [0, int(splitstring[0])]
    return dict

def adddifftodictionary(dict):
    """Adds a difference in size to the intermediate dictionary, completing it. Returns a dictionary with list as a value."""
    for directory in dict:
        if len(dict[directory]) == 2:
            dict[directory].append(dict[directory][1] - dict[directory][0])
    return dict

def buildcompletedict(oldfile, newfile):
    """Performs all dictionary-building steps. Requires two filenames. File-opening happens here. Returns a dictionary with list as a value."""
    return adddifftodictionary(addtodictionary(builddictionary(open(oldfile).readlines()), open(newfile).readlines()))

def printtable(dict):
    """Prints out a table with sizes and differences into stdout."""
    for dirname in dict:
        if dict[dirname][2] != 0:
            sys.stdout.write("{0:4} {1:4} {2:4} {3}\n".format(dict[dirname][2], dict[dirname][0], dict[dirname][1], dirname))

def cleanup(dict):
    """Cleans a dictionary up, removing parent directories with duplicate data for them, leaving only directories that changed."""
    from itertools import groupby
    from operator import itemgetter
    tuplelist = []
    for dirname, data in groupby(sorted(dict.items(),key=itemgetter(1)),key=itemgetter(1)):
        data = list(data)
        mx = max(data,key=lambda x:len(x[0]))
        tuplelist += [x for x in data if len(x[0]) == len(mx[0])]
    tuplelist.sort()
    dict = {}
    for dirname, data in tuplelist:
        #print(dirname, data)
        dict[dirname] = data
    return dict

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog = 'dude', description = 'Dude: A neat tool to determine where your free space actually goes. Relies on files created by "du" utility. The first value in the table is a size difference, the second is old size, the third is new size.')
    parser.add_argument("oldlist", help = "an old du-created text file")
    parser.add_argument("newlist", help = "a new du-created text file")
    parser.add_argument( "-c", "--clean", action = "store_true", help = "clean the resulting list up a little, removing parent directories")
    args = parser.parse_args()
    if args.clean == True:
        printtable(cleanup(buildcompletedict(args.oldlist, args.newlist)))
    else:
        printtable(buildcompletedict(args.oldlist, args.newlist))
