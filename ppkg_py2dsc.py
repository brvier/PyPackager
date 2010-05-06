#!/usr/bin/python
# -*- coding: utf-8 -*-
##    This file is a part of py2deb
##    This version of py2deb is a dirty hack made by Khertan based on a mix of PyPackager and Original Py2Deb 0.3
##    Copyright (C) 2007 manatlan manatlan[at]gmail(dot)com
##    Copyright (C) 2008 Khertan khertan[at]khertan(dot)net
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 2 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
import os 
import ppkg_md5hash

class py2dsc(object):

    """
    """
    def __init__(self, StandardsVersion,BuildDepends,files, **kwargs):
      self.options = kwargs # TODO: Is order important?
      self.StandardsVersion = StandardsVersion
      self.BuildDepends=BuildDepends
      self.files=files
      #self.category=category
      #self.repository=repository
      #self.ChangedBy=ChangedBy

    def _getContent(self):
        """
        """
        content = ["%s: %s" % (k, v)
                   for k,v in self.options.iteritems()]

        #if self.description:
        #    self.description=self.description.replace("\n","\n ")
        #    content.append("Description: %s" % self.description)

        #if self.changes:
        #    self.changes=self.changes.replace("\n","\n ")
        #    content.append("Changes: %s" % self.changes)

        if self.BuildDepends:
            content.append("Build-Depends: %s" % self.BuildDepends)
        if self.StandardsVersion:
            content.append("Standards-Version: %s" % self.StandardsVersion)

        content.append('Files:')

        for onefile in self.files:
            print onefile
            md5=ppkg_md5hash.md5sum(onefile)
            size=os.stat(onefile).st_size.__str__()
            content.append(' '+md5 + ' ' + size +' '+os.path.basename(onefile))

        print "\n".join(content)+"\n"
        return "\n".join(content)+"\n\n"

    content = property(_getContent, doc="")