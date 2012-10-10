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
#    This file was a part of py2deb
#    This version of py2deb is a dirty hack made by Khertan
#    based on a mix of PyPackager and Original Py2Deb 0.3
#    Copyright (C) 2007 manatlan manatlan[at]gmail(dot)com


import os
import stat
import time
import tarfile
from tarfile import TarFile as _TarFile

from cStringIO import StringIO

PERMS_URW_GRW_OR = stat.S_IRUSR | stat.S_IWUSR | \
    stat.S_IRGRP | stat.S_IWGRP | \
    stat.S_IROTH

UID_ROOT = 0
GID_ROOT = 0


class TarFile(_TarFile):
    """
    """

    def addfilefromstring(self, name, theString):
        """
        """
        content = StringIO(theString)

        theFileInfo = tarfile.TarInfo(name=name)
        # Absence seems to break tgz file.
        theFileInfo.mtime = int(time.time())
        theFileInfo.size = len(content.getvalue())
        theFileInfo.mode = 3333
        self.addfile(theFileInfo, fileobj=content)


class myTarFile(object):
    """
    """

    def __init__(self, dataDirectoryPath):
        """
        """
        self._dataDirectoryPath = dataDirectoryPath

    def packed(self):
        return self._getSourcesFiles()

    def _getSourcesFiles(self):
        """
        """
        directoryPath = self._dataDirectoryPath

        outputFileObj = StringIO()  # TODO: Do more transparently?

        tarOutput = TarFile.open('sources',
                                 mode="w:gz",
                                 fileobj=outputFileObj)

        # Note: We can't use this because we need to fiddle permissions:
        #       tarOutput.add(directoryPath, arcname = "")

        # TODO: Add this as a method for TarFile and tidy-up?
        for root, dirs, files in os.walk(directoryPath):
            archiveRoot = root[len(directoryPath):]

            tarinfo = tarOutput.gettarinfo(root, archiveRoot)
            # TODO: Make configurable?
            tarinfo.uid = UID_ROOT
            tarinfo.gid = GID_ROOT
            tarinfo.uname = ""
            tarinfo.gname = ""
            tarOutput.addfile(tarinfo)

            for f in files:
                tarinfo = tarOutput.gettarinfo(os.path.join(root, f),
                                               os.path.join(archiveRoot, f))
                tarinfo.uid = UID_ROOT
                tarinfo.gid = GID_ROOT
                tarinfo.uname = ""
                tarinfo.gname = ""
                tarOutput.addfile(tarinfo, file(os.path.join(root, f)))

        tarOutput.close()

        data_tar_gz = outputFileObj.getvalue()

        return data_tar_gz
