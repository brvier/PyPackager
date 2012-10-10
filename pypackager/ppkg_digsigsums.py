#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
##    Copyright (C) 2007 Khertan khertan@khertan.net
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

#Original code was picked from MeeGo.com forum. Author is merlin1991

import sys
import os
import hashlib


def check_file(filePath):
    if not os.path.exists(filePath):  # To be able to hash StringIO
        return True
    fh = open(filePath, 'r')
    if fh.read(2) == '#!':
        fh.close()
        return True
    fh.close()
    return False


def hash_file(packageName, src_filepath, dst_filepath):
    # digsigsums format:
    # S 15 com.nokia.maemo H 40 xxxxxxxxxxxxxxxxxxxxx R 5 abcde
    # Source (might change) hash (sha1) relative path
    if 'DEBIAN/' in dst_filepath:
        dst_filepath = 'var/lib/dpkg/info/{0}.{1}'.format(packageName,
                       dst_filepath[8 + len(packageName):])
    if dst_filepath.startswith('/'):
        dst_filepath = dst_filepath[1:]
    if os.path.exists(src_filepath):
        fileToHash = open(src_filepath, 'rb')
        sha1 = hashlib.sha1()
        sha1.update(fileToHash.read())
        hashString = sha1.hexdigest()
        fileToHash.close()
    else:
        sha1 = hashlib.sha1()
        sha1.update(src_filepath)
        hashString = sha1.hexdigest()
    return 'S 15 com.nokia.maemo H 40 {0} R {1} {2}\n' \
           .format(hashString,
                   len(dst_filepath),
                   dst_filepath)


def generate_digsigsums(packageName, files):
    result = ''
    for path in files.keys():
        for pfile, nfile in files[path]:
            dst_filename = os.path.join(path, nfile)
            src_filename = os.path.join(sys.path[0], pfile)
            if check_file(src_filename):
                result = result + (hash_file(packageName,
                                             src_filename,
                                             dst_filename))
    return result
