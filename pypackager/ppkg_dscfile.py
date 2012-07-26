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

import os 
import md5hash

class DscFile(object):

    """
    """
    def __init__(self, StandardsVersion,BuildDepends,files, **kwargs):
      self.options = kwargs 
      self.StandardsVersion = StandardsVersion
      self.BuildDepends=BuildDepends
      self.files=files


    def _getContent(self):
        """
        """
        content = ["%s: %s" % (k, v)
                   for k,v in self.options.iteritems()]

        if self.BuildDepends:
            content.append("Build-Depends: %s" % self.BuildDepends)
        if self.StandardsVersion:
            content.append("Standards-Version: %s" % self.StandardsVersion)
            
        content.append('Files:')

        for onefile in self.files:
            print onefile
            md5=md5hash.md5sum(onefile)
            size=os.stat(onefile).st_size.__str__()
            content.append(' '+md5 + ' ' + size +' '+os.path.basename(onefile))

        print "\n".join(content)+"\n"
        return "\n".join(content)+"\n\n"

    content = property(_getContent, doc="")