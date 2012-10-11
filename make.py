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
from glob import glob

import pypackager

__build__ = pypackager.__build__
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
    p.summary = 'A python packaging tool : deb, dsc, spec'
    p.description="Create debian binary package, debian source package, and obs source package (specs) easily from python"
    p.upgrade_description= pypackager.__changelog__
    p.author=__author__
    p.maintainer=__author__
    p.email=__mail__
    p.depends = "python"
    p.suggests = "khteditor"
    p.section="user/development"
    p.arch="all"
    p.urgency="low"
    p.icon='pypackager.png'
    p.distribution="harmattan"
    p.repository="Khertan Repository"
    p.url = 'http://khertan.net/PyPackager'
    p.bugtracker = 'http://github.com/khertan/PyPackager/issues'
    p.changelog = pypackager.__changelog__
    p.maemo_flags = 'visible'
    p.meego_desktop_entry_filename = ''
    p.createDigsigsums = True
    p.aegisManifest = ''
    files = []

    #Remove pyc and pyo
    for filepath in glob(os.path.join(os.path.dirname(__file__), p.name, '*.pyc')):
        os.remove(filepath)
    #Remove pyc and pyo
    for filepath in glob(os.path.join(os.path.dirname(__file__), p.name, '*.pyo')):
        os.remove(filepath)

    #Src
    for root, dirs, fs in os.walk(os.path.join(os.path.dirname(__file__), p.name)):
      for f in fs:
        files.append(os.path.join(root, f))

    p["/usr/lib/pymodules/python2.6"] = files
    p["/usr/lib/pymodules/python2.7"] = files

    print p.generate(build_binary=True,build_src=True)

    if not os.path.exists('dists'):
        os.mkdir('dists')
    for filepath in glob(p.name+'_'+p.version+'-'+p.buildversion+'*'):
        os.rename(filepath, os.path.join(os.path.dirname(filepath), 'dists', os.path.basename(filepath)))
