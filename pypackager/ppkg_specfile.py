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


class PyPackagerException(Exception):
    pass


class SpecFile(object):

    def __init__(self, kwargs):
        self.options = kwargs
        self.__files = kwargs['_PyPackager__files']

    def _getContent(self):
        rules = []
        files = []
        for path in self.__files:
            for ofile, nfile in self.__files[path]:
                if os.path.isfile(ofile):
                    # it's a file
                    src_path = os.path.relpath(ofile, self.options['name'])
                    dst_path = "%{buildroot}" \
                               + os.path.join(path,
                                              os.path.dirname(nfile))
                    nname = os.path.basename(nfile)
                    files.append(os.path.join(path,
                                              os.path.dirname(nfile),
                                              nname))
                    rules.append('mkdir -p "%s"' % dst_path)

                    # make a line RULES to be sure the destination folder
                    # is created and one for copying the file
                    rules.append('cp -a "%s" "%s"' %
                                (src_path, os.path.join(dst_path, nname)))

                else:
                    raise PyPackagerException("unknown file '' " % ofile)
                    # shouldn't be raised (because controlled before)

        self.options['specrules'] = '\n'.join(rules)
        self.options['packedfiles'] = '\n'.join(files)

        content = """
Name: %(name)s
Version: %(version)s
Release: %(buildversion)s
Summary: %(summary)s
Group: %(section)s
License: %(license)s
URL: %(url)s
Source0: %(sources)s

BuildRoot: %%{_tmppath}/%%{name}-%%{version}-%%{release}-root-%%(%%{__id_u} -n)
BuildArch: noarch
BuildRequires: %(builddepends)s
Requires: %(depends)s

%%description
%(description)s

%%prep
%%setup -n %(name)s

%%build

%%install
%(specrules)s
""" % self.options
        if self.options['postinst']:
            content = content + """
%%post
%(postinst)s
""" % self.options
        if self.options['postrm']:
            content = content + """%%postun
%(postrm)s
""" % self.options
        if self.options['prerm']:
            content = content + """%%preun
%(prerm)s
""" % self.options
        if self.options['preinst']:
            content = content + """%%pre
%(preinst)s
"""

        content = content + """%%clean
rm -rf %%{buildroot}


%%files
%%defattr(-,root,root,-)
%(packedfiles)s

""" % self.options
        return content

    content = property(_getContent, doc="")
