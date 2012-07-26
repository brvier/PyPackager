#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
##    Copyright (C) 2007 Benoit HERVIER (Khertan) khertan@khertan.net
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
import sys
import shutil
import time
import string
from glob import glob
from datetime import datetime
import socket

import pypackager

__build__ = '1'
__author__ = "khertan"
__mail__ = "khertan@khertan.net"


if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("pypackager")
    p.display_name = 'PyPackager'
    p.version = pypackager.__version__
    p.buildversion = __build__
    p.description="Generate simple deb or source deb from python"
    p.upgrade_description="Add support for harmattan"
    p.author=__author__
    p.maintainer=__author__
    p.email=__mail__
    p.depends = "python"
    p.suggests = "khteditor"
    p.section="user/development"
    p.arch="armel"
    p.urgency="low"
    p.icon='pypackager.png'
    p.distribution="harmattan"
    p.repository="Khertan Repository"
    p.bugtracker = 'http://khertan.net/pypackager/bugs'
    p.changelog = "* fix various bug in harmattan source package creation"
    p.maemo_flags = 'visible'
    p.meego_desktop_entry_filename = ''
    p.createDigsigsums = True
    p.aegisManifest = '''<aegis name="...">
  <provide></provide>
  <constraint></constraint>
  <account></account>
  <request></request>
  <domain></domain>
  <docstring></docstring>
</aegis>'''
    files = []

    #Src
    for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/pypackager/pypackager'):
      for f in fs:
        #print os.path.basename(root),dirs,f
        prefix = 'pypackager/'
        if os.path.basename(root) != 'pypackager':
            prefix = prefix + os.path.basename(root) + '/'
        files.append(prefix+os.path.basename(f))
    print files


    p["/usr/lib/pymodules/python2.6"] = files

    print p
    print p.generate(build_binary=True,build_src=True)
#    print p.generate(build_binary=True,build_src=False)
