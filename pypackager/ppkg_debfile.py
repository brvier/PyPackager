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
# A pure Python way of producing .deb files suitable installation
# on the Maemo platform.
# Original Author: follower@rancidbacon.com
# Date: 15 September 2006
# License: GPL 2.0


import os
import stat
import time
import tarfile
from tarfile import TarFile as _TarFile
import sys
from cStringIO import StringIO

import ppkg_arfile

FILENAME_DEB_VERSION = "debian-binary"
FILE_CONTENT_DEB_VERSION = "2.0\x0a"

FILENAME_CONTROL_TAR_GZ = "control.tar.gz"
FILENAME_DATA_TAR_GZ = "data.tar.gz"

PERMS_URW_GRW_OR = stat.S_IRUSR | stat.S_IWUSR | \
    stat.S_IRGRP | stat.S_IWGRP | \
    stat.S_IROTH

UID_ROOT = 0
GID_ROOT = 0


class ControlFile(object):
    """
    """

    def __init__(self, Icon, BugTracker, DisplayName, PreInst,
                 PostInst, PreRm, PostRm,
                 long_description="",
                 Description="",
                 UpgradeDescription=None,
                 MaemoFlags='visible',
                 MeegoDesktopEntryFilename=None,
                 createDigsigsums=False,
                 aegisManifest=None,
                 **kwargs
                 ):
        """
        """
        self.options = kwargs  # TODO: Is order important?

        # TODO: Clean-up special handling of description
        self.description = Description
        self.long_description = long_description
        self.icon = Icon
        self.bugtracker = BugTracker
        self.displayname = DisplayName
        self.preinst = PreInst
        self.postinst = PostInst
        self.prerm = PreRm
        self.postrm = PostRm
        self.upgrade_description = UpgradeDescription
        self.maemo_flags = MaemoFlags
        self.meego_desktop_entry_filename = MeegoDesktopEntryFilename
        self.createDigsigsums = createDigsigsums
        self.aegisManifest = aegisManifest

    def _getContent(self):
        """
        """
        content = ["%s: %s" % (k, v)
                   for k, v in self.options.iteritems()]

        if self.bugtracker:
            content.append("Bugtracker: %s" % self.bugtracker)
        if self.displayname:
            content.append("Maemo-Display-Name: %s" % self.displayname)
        if self.maemo_flags:
            content.append("Maemo-Flags: %s" % self.maemo_flags)
        if self.meego_desktop_entry_filename:
            content.append("Meego-Desktop-Entry-Filename: %s"
                           % self.meego_desktop_entry_filename)

        if self.description:
            self.description = self.description.replace("\n", "\n ")
            content.append("Description: %s" % self.description)

            if self.long_description:
                self.long_description = \
                    self.long_description.replace("\n", "\n ")
                content.append(" " + self.long_description)

        if self.upgrade_description:
            self.upgrade_description = \
                self.upgrade_description.rstrip('\n').replace("\n", "\n ")
            content.append("Maemo-Upgrade-Description: %s"
                           % self.upgrade_description)

        if self.icon:
            content.append("Maemo-Icon-26: %s" % self.icon)

        print "\n".join(content) + "\n"
        return "\n".join(content) + "\n"

    content = property(_getContent, doc="")


class TarFile(_TarFile):
    """
    """

    def addfilefromstring(self, name, theString):
        """
        """
        content = StringIO(theString)

        theFileInfo = tarfile.TarInfo(name=name)
        # Absence seems to break tgz file
        theFileInfo.mtime = int(time.time())
        theFileInfo.size = len(content.getvalue())
        theFileInfo.uid = UID_ROOT
        theFileInfo.gid = GID_ROOT
        theFileInfo.mode = 3333

        self.addfile(theFileInfo, fileobj=content)


class MaemoPackage(object):
    """
    """

    def __init__(self, controlFile, files):
        """
        """
        self.controlFile = controlFile
        self.__files = files

    def packed(self):
        """
        """
        theDeb = ppkg_arfile.ArFile()

        ## Add the debian package version
        theDeb.files.append(self._getVersionFile())

        ## Add the compressed control related file(s)
        theDeb.files.append(self._getControlFiles())

        ## Add compressed data file(s)
        theDeb.files.append(self._getDataFiles())

        ## Add _aegis if needed
        if self.controlFile.aegisManifest:
            theDeb.files.append(self._getAegisFile())

        return theDeb.packed()

    def _getSize(self):
        size = 0
        paths = self.__files.keys()
        paths.sort()
        CURRENT = os.path.dirname(sys.argv[0])
        for path in paths:
            for pfile, nfile in self.__files[path]:
                size = size + (getattr(os.stat(
                    os.path.join(CURRENT, pfile)),
                    'st_size') / 1024)
        return size

    def _getVersionFile(self):
        """
        """
        debVersionFile = \
            ppkg_arfile.FileInfo(name=FILENAME_DEB_VERSION,
                                 modificationTime=int(time.time()),
                                 userId=UID_ROOT,
                                 groupId=GID_ROOT,
                                 fileMode=PERMS_URW_GRW_OR,
                                 fileSize=len(FILE_CONTENT_DEB_VERSION),
                                 data=FILE_CONTENT_DEB_VERSION)

        return debVersionFile

    def _getControlFiles(self):
        """
        """
        debControlFile = self.controlFile.content \
            + 'Installed-Size: ' + str(self._getSize()) + '\n'

        outputFileObj = StringIO()
        tarOutput = TarFile.open(FILENAME_CONTROL_TAR_GZ,
                                 mode="w:gz",
                                 fileobj=outputFileObj)

        tarOutput.addfilefromstring("control", debControlFile)
        if (self.controlFile.preinst):
            tarOutput.addfilefromstring("preinst", self.controlFile.preinst)
        if (self.controlFile.postinst):
            tarOutput.addfilefromstring("postinst", self.controlFile.postinst)
        if (self.controlFile.prerm):
            tarOutput.addfilefromstring("prerm", self.controlFile.prerm)
        if (self.controlFile.postrm):
            tarOutput.addfilefromstring("postrm", self.controlFile.postrm)

        # TODO: Add `postinst` here if needed.
        if self.controlFile.createDigsigsums:
            from ppkg_digsigsums import generate_digsigsums, hash_file
            package_name = self.controlFile.options['Package']
            digsigsums = generate_digsigsums(package_name, self.__files)
            if (self.controlFile.preinst):
                digsigsums = digsigsums + \
                    hash_file(package_name, self.controlFile.preinst,
                              'var/lib/dpkg/info/'
                              + package_name + '.preinst')
            if (self.controlFile.postinst):
                digsigsums = digsigsums + \
                    hash_file(package_name,
                              self.controlFile.postinst,
                              'var/lib/dpkg/info/'
                              + package_name + '.postinst')
            if (self.controlFile.prerm):
                digsigsums = digsigsums + \
                    hash_file(package_name,
                              self.controlFile.prerm,
                              'var/lib/dpkg/info/'
                              + package_name + '.prerm')
            if (self.controlFile.postrm):
                digsigsums = digsigsums + \
                    hash_file(package_name,
                              self.controlFile.postrm,
                              'var/lib/dpkg/info/'
                              + package_name + '.postrm')

            tarOutput.addfilefromstring("digsigsums", digsigsums)
            print digsigsums

        if self.controlFile.aegisManifest:
            tarOutput.addfilefromstring("%s.aegis" % FILENAME_DEB_VERSION,
                                        self.controlFile.aegisManifest)

        tarOutput.close()

        control_tar_gz = outputFileObj.getvalue()

        controlFile = ppkg_arfile.FileInfo(name=FILENAME_CONTROL_TAR_GZ,
                                           modificationTime=int(time.time()),
                                           userId=UID_ROOT,
                                           groupId=GID_ROOT,
                                           fileMode=PERMS_URW_GRW_OR,
                                           fileSize=len(control_tar_gz),
                                           data=control_tar_gz)

        return controlFile

    def _getAegisFile(self):
        return \
            ppkg_arfile.FileInfo(name=FILENAME_DEB_VERSION,
                                 modificationTime=int(time.time()),
                                 userId=UID_ROOT,
                                 groupId=GID_ROOT,
                                 fileMode=PERMS_URW_GRW_OR,
                                 fileSize=len(self.controlFile.aegisManifest),
                                 data=self.controlFile.aegisManifest)

    def _getDataFiles(self):
        """
        """

        outputFileObj = StringIO()

        tarOutput = TarFile.open(FILENAME_DATA_TAR_GZ,
                                 mode="w:gz",
                                 fileobj=outputFileObj)

        # Note: We can't use this because we need to fiddle permissions:
        #       tarOutput.add(directoryPath, arcname = "")

        # TODO: Add this as a method for TarFile and tidy-up?
        paths = self.__files.keys()
        paths.sort()

        CURRENT = sys.path[0]
        for path in paths:
            tarinfo = tarOutput.gettarinfo(os.path.join(CURRENT), path)
            tarinfo.uid = UID_ROOT
            tarinfo.gid = GID_ROOT
            tarinfo.uname = ""
            tarinfo.gname = ""
            tarOutput.addfile(tarinfo)

            #We need to get all folder and create them before
            folders = []
            for pfile, nfile in self.__files[path]:
                dirpath = os.path.dirname(pfile)
                while dirpath:
                    if dirpath not in folders:
                        folders.append(dirpath)
                    dirpath = os.path.dirname(dirpath)

            folders = list(set(folders))
            folders.sort()
            print folders

            for folder in folders:
                if folder.endswith('/'):
                    folder = folder[:0]
                if folder.startswith('/'):
                    folder = folder[1:]
                tarinfo = tarOutput.gettarinfo(os.path.join(
                                               CURRENT, folder),
                                               os.path.join(path, folder))
                tarinfo.uid = UID_ROOT
                tarinfo.gid = GID_ROOT
                tarinfo.uname = ""
                tarinfo.gname = ""
                tarinfo.mtime = int(time.time())
                tarOutput.addfile(tarinfo)

            for pfile, nfile in self.__files[path]:
                rfile = os.path.normpath(os.path.join(path, nfile))
                if rfile.startswith('/'):
                    rfile = rfile[1:]
                if not rfile in folders:
                    tarOutput.addfilefromstring(
                        rfile,
                        file(os.path.join(CURRENT, pfile)).read())

        tarOutput.close()

        data_tar_gz = outputFileObj.getvalue()

        dataFile = ppkg_arfile.FileInfo(name=FILENAME_DATA_TAR_GZ,
                                        modificationTime=int(time.time()),
                                        userId=UID_ROOT,
                                        groupId=GID_ROOT,
                                        fileMode=PERMS_URW_GRW_OR,
                                        fileSize=len(data_tar_gz),
                                        data=data_tar_gz)
        return dataFile
