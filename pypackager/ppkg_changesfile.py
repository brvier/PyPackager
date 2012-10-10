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
#    This version of py2deb is a dirty hack made by Khertan based on a mix of
#    PyPackager and Original Py2Deb 0.3
#    Copyright (C) 2007 manatlan manatlan[at]gmail(dot)com


import os
import ppkg_md5hash


class ChangesFile(object):

    """
    """
    def __init__(self, ChangedBy, description, changes,
                 files, category, repository, **kwargs):
        self.options = kwargs  # TODO: Is order important?
        self.description = description
        self.changes = changes
        self.files = files
        self.category = category
        self.repository = repository
        self.ChangedBy = ChangedBy

    def getContent(self):
        """
        """
        content = ["%s: %s" % (k, v)
                   for k, v in self.options.iteritems()]

        if self.description:
            description = self.description.replace("\n", "\n ")
            content.append('Description: ')
            content.append(' %s' % description)

        if self.changes:
            changes = self.changes.replace("\n", "\n ")
            content.append('Changes: ')
            content.append(' %s' % changes)

        if self.ChangedBy:
            content.append("Changed-By: %s" % self.ChangedBy)

        content.append('Files:')

        for onefile in self.files:
            print onefile
            md5 = ppkg_md5hash.md5sum(onefile)
            size = os.stat(onefile).st_size.__str__()
            content.append(' ' + md5 + ' ' + size + ' ' + self.category + ' '
                           + self.repository + ' ' + os.path.basename(onefile))

        print "\n".join(content) + "\n"
        return "\n".join(content) + "\n\n"
