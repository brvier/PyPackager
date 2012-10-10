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
#
#
# Author: follower@rancidbacon.com
#
# Date: 13 September 2006
#
# License: GPL 2.0
#
# Note:
#
#  * This has been written based on the format described in the AR(5) man page.
#
#  * This module does not fully implement the file format as described--there
#    is no support for file names longer than 16 characters--nor is there
#    any error checking that this does not occur.
#
#  * There is no functionality for reading `ar` format files--only writing for
#    them.
#
#  * The motivation for writing this was for creating a pure-Python way
#    of constructing ".deb" files--which is an archive file with 3 specific
#    files in it--thus a limited functionality requirement.
#
import os

MAGIC_STRING = "!<arch>\n"


def paddedString(text, length):
    """

    Return a string with (possibly no) trailing spaces so the total
    length of the string is `length` characters.

    """
    return (text + length * " ")[:length]


NAME_BUFFER_LENGTH = 16
MOD_TIME_BUFFER_LENGTH = 12
ID_BUFFER_LENGTH = 6
FILE_MODE_BUFFER_LENGTH = 8
FILE_SIZE_BUFFER_LENGTH = 10

NO_PADDING_CHAR = ""
PADDING_CHAR = "\n"

FILE_HEADER_TRAILER = "`\n"


class FileInfo(object):
    """

    Represents a single file in the archive.

    The name is a little of a misnomer as it also (currently) holds the
    file content.

    """

    def __init__(self,
                 name,
                 modificationTime,
                 userId, groupId,
                 fileMode,
                 fileSize,
                 data):
        """
        """
        self.name = name  # TODO: Ensure ar-compatible
        self.modificationTime = modificationTime
        self.userId = userId
        self.groupId = groupId
        self.fileMode = fileMode
        self.fileSize = fileSize
        self.data = data

    def _getHeader(self):
        """

        Returns the header for the file as documented in AR(5).

        """
        data = []

        data.append(paddedString(self.name, NAME_BUFFER_LENGTH))

        data.append(paddedString(str(self.modificationTime),
                                 MOD_TIME_BUFFER_LENGTH))

        data.append(paddedString(str(self.userId), ID_BUFFER_LENGTH))

        data.append(paddedString(str(self.groupId), ID_BUFFER_LENGTH))

        data.append(paddedString("%o" % self.fileMode,
                                 FILE_MODE_BUFFER_LENGTH))

        data.append(paddedString(str(self.fileSize), FILE_SIZE_BUFFER_LENGTH))

        data.append(FILE_HEADER_TRAILER)

        return "".join(data)

    header = property(_getHeader, doc="")

    def packed(self):
        """

        Returns the "packed" form suitable for appended to an `ar` file.

        The packing concatenates the header, data and--if
        necessary--trailing padding. The padding is required to obey
        the "Objects in the archive are always an even number of bytes
        long;" requirement of the file format.

        """
        return self.header + \
            self.data + \
            [NO_PADDING_CHAR, PADDING_CHAR][self.fileSize % 2]  # Pad odd size

    def _fromFilePath(filepath):
        """
        """
        statResult = os.stat(filepath)
        return FileInfo(name=os.path.basename(filepath),
                        modificationTime=statResult.st_mtime,
                        userId=statResult.st_uid,
                        groupId=statResult.st_gid,
                        fileMode=statResult.st_mode,
                        fileSize=statResult.st_size,
                        data=open(filepath, "rb").read())  # Hardly efficient!

    fromFilePath = staticmethod(_fromFilePath)


class ArFile(object):
    """

    Represents a complete archive.

    Files can be added by appending the paths to the `files` list.

    """

    def __init__(self):
        """
        """
        self.files = []  # Can be a string file path or a FileInfo instance.

    def packed(self):
        """

        Returns the "packed" form of the archive--suitable for writing
        to disc.

        """
        content = []

        content.append(MAGIC_STRING)

        for theFile in self.files:
            if isinstance(theFile, FileInfo):
                packedFile = theFile.packed()
            else:
                packedFile = FileInfo.fromFilePath(theFile).packed()

            content.append(packedFile)

        return "".join(content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print "Usage: %s  <filepath> [...]" % sys.argv[0]
        raise SystemExit

    #print FileInfo.fromFilePath(filepath).header
    #print FileInfo.fromFilePath(filepath).packed()

    archiveFile = ArFile()

    for theFilepath in sys.argv[1:]:
        archiveFile.files.append(theFilepath)

    sys.stdout.write(archiveFile.packed())
