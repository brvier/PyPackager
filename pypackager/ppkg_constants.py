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

PPKG_SECTIONS = "user/desktop, user/development, user/education, user/games," \
    " user/graphics, user/multimedia, user/navigation," \
    " user/network," \
    " user/office, user/science, user/system, user/utilities," \
    " accessories, communication, games, multimedia, office," \
    " other, programming, support, themes, tools".split(", ")

PPKG_ARCHS = "all any armel i386 ia64 alpha amd64 armeb arm hppa m32r" \
             " m68k mips mipsel powerpc ppc64 s390 s390x sh3 sh3eb sh4" \
             " sh4eb sparc darwin-i386 darwin-ia64 darwin-alpha darwin-amd64" \
             " darwin-armeb darwin-arm darwin-hppa darwin-m32r darwin-m68k" \
             " darwin-mips darwin-mipsel darwin-powerpc darwin-ppc64" \
             " darwin-s390 darwin-s390x darwin-sh3 darwin-sh3eb darwin-sh4" \
             " darwin-sh4eb darwin-sparc freebsd-i386 freebsd-ia64" \
             " freebsd-alpha freebsd-amd64 freebsd-armeb freebsd-arm" \
             " freebsd-hppa freebsd-m32r freebsd-m68k freebsd-mips" \
             " freebsd-mipsel freebsd-powerpc freebsd-ppc64 freebsd-s390" \
             " freebsd-s390x freebsd-sh3 freebsd-sh3eb freebsd-sh4" \
             " freebsd-sh4eb freebsd-sparc kfreebsd-i386 kfreebsd-ia64" \
             " kfreebsd-alpha kfreebsd-amd64 kfreebsd-armeb" \
             " kfreebsd-arm kfreebsd-hppa kfreebsd-m32r kfreebsd-m68k" \
             " kfreebsd-mips kfreebsd-mipsel kfreebsd-powerpc" \
             " kfreebsd-ppc64 kfreebsd-s390 kfreebsd-s390x kfreebsd-sh3" \
             " kfreebsd-sh3eb kfreebsd-sh4 kfreebsd-sh4eb kfreebsd-sparc" \
             " knetbsd-i386 knetbsd-ia64 knetbsd-alpha knetbsd-amd64" \
             " knetbsd-armeb knetbsd-arm knetbsd-hppa knetbsd-m32r" \
             " knetbsd-m68k knetbsd-mips knetbsd-mipsel knetbsd-powerpc" \
             " knetbsd-ppc64 knetbsd-s390 knetbsd-s390x knetbsd-sh3" \
             " knetbsd-sh3eb knetbsd-sh4 knetbsd-sh4eb knetbsd-sparc" \
             " netbsd-i386 netbsd-ia64 netbsd-alpha netbsd-amd64" \
             " netbsd-armeb netbsd-arm netbsd-hppa netbsd-m32r" \
             " netbsd-m68k netbsd-mips netbsd-mipsel netbsd-powerpc" \
             " netbsd-ppc64 netbsd-s390 netbsd-s390x netbsd-sh3" \
             " netbsd-sh3eb netbsd-sh4 netbsd-sh4eb netbsd-sparc" \
             " openbsd-i386 openbsd-ia64 openbsd-alpha" \
             " openbsd-amd64 openbsd-armeb openbsd-arm" \
             " openbsd-hppa openbsd-m32r openbsd-m68k openbsd-mips" \
             " openbsd-mipsel openbsd-powerpc openbsd-ppc64" \
             " openbsd-s390 openbsd-s390x openbsd-sh3 openbsd-sh3eb" \
             " openbsd-sh4 openbsd-sh4eb openbsd-sparc hurd-i386" \
             " hurd-ia64 hurd-alpha hurd-amd64 hurd-armeb hurd-arm" \
             " hurd-hppa hurd-m32r hurd-m68k hurd-mips" \
             " hurd-mipsel hurd-powerpc hurd-ppc64 hurd-s390" \
             " hurd-s390x hurd-sh3 hurd-sh3eb hurd-sh4" \
             " hurd-sh4eb hurd-sparc".split(" ")

PPKG_LICENSES = ["gpl", "lgpl", "bsd", "artistic", "shareware"]

PPKG_RETURN = """
----------------------------------------------------------------------
NAME        : %(name)s
----------------------------------------------------------------------
LICENSE     : %(license)s
URL         : %(url)s
AUTHOR      : %(author)s
MAIL        : %(email)s
----------------------------------------------------------------------
DEPENDS     : %(depends)s
ARCH        : %(arch)s
SECTION     : %(section)s
----------------------------------------------------------------------
DESCRIPTION :
%(description)s
----------------------------------------------------------------------
SCRIPTS : %(scripts)s
----------------------------------------------------------------------
FILES :
%(files)s
"""

PPKG_DEBIAN_CHANGESLOG =  \
    """%(name)s (%(version)s-%(buildversion)s) stable; urgency=low

  %(changelog)s

 -- %(author)s <%(email)s>  %(buildDate)s
  """

PPKG_DEBIAN_CONTROL = """Source: %(name)s
Section: %(section)s
Priority: optional
Maintainer: %(maintainer)s <%(email)s>
Build-Depends: %(build_depends)s
Standards-Version: 3.9.2

Package: %(name)s
XB-Maemo-Display-Name: %(display_name)s
Architecture: %(arch)s
Depends: %(depends)s
Suggests: %(suggests)s
Description: %(description)s
XB-Maemo-Upgrade-Description: %(upgrade_description)s
XB-Maemo-Flags: %(maemo_flags)s
XB-MeeGo-Desktop-Entry-Filename: %(meego_desktop_entry_filename)s
%(bugtrackerstr)s
%(iconstr)s"""

PPKG_LICENSES_TEXT = {
    "gpl": """
This package is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this package; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

On Debian systems, the complete text of the GNU General
Public License can be found in `/usr/share/common-licenses/GPL'.
""",
    "lgpl": """
This package is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.

This package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this package; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

On Debian systems, the complete text of the GNU Lesser General
Public License can be found in `/usr/share/common-licenses/LGPL'.
""",
    "bsd": """
Redistribution and use in source and binary forms, with or without
modification, are permitted under the terms of the BSD License.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

On Debian systems, the complete text of the BSD License can be
found in `/usr/share/common-licenses/BSD'.
""",
    "shareware": """
This product is copyrighted shareware, not public-domain software.
You may use the unregistered version at no charge for an evaluation period.
To continue to use the software beyond evaluation period, you must register it.

THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES
OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.
""",
    "artistic": """
This program is free software; you can redistribute it and/or modify it
under the terms of the "Artistic License" which comes with Debian.

THIS PACKAGE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES
OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.

On Debian systems, the complete text of the Artistic License
can be found in `/usr/share/common-licenses/Artistic'.
""",
}

PPKG_COPYRIGHT = \
    """This package was pypackaged(%(pv)s) by %(author)s <%(email)s> on
%(buildDate)s.

It was downloaded from %(url)s

Upstream Author: %(author)s <%(email)s>

Copyright: %(buildDateYear)s by %(author)s

License:

%(txtLicense)s

The Debian packaging is (C) %(buildDateYear)s, %(author)s <%(email)s> and
is licensed under the GPL, see above.


# Please also look if there are files or directories which have a
# different copyright/license attached and list them here.
"""

PPKG_DEBIAN_RULE = \
    """#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1

CFLAGS = -Wall -g

ifneq (,$(findstring noopt,$(DEB_BUILD_OPTIONS)))
\tCFLAGS += -O0
else
\tCFLAGS += -O2
endif

configure: configure-stamp
configure-stamp:
\tdh_testdir
\t# Add here commands to configure the package.
\ttouch configure-stamp

build: build-stamp

build-stamp: configure-stamp
\tdh_testdir
\ttouch build-stamp

clean:
\tdh_testdir
\tdh_testroot
\trm -f build-stamp configure-stamp
\tdh_clean

install: build
\tdh_testdir
\tdh_testroot
\tdh_clean -k
\tdh_installdirs

\t# ======================================================
\t#$(MAKE) DESTDIR="$(CURDIR)/debian/%(name)s" install
\tmkdir -p "$(CURDIR)/debian/%(name)s"

\t%(rules)s
\t# ======================================================

# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
\tdh_testdir
\tdh_testroot
\tdh_installchangelogs debian/changelog
\tdh_installdocs
\tdh_installexamples
\tdh_installman
\tdh_link
\tdh_strip
\tdh_compress
\tdh_fixperms
\tdh_installdeb
\tdh_shlibdeps
\tdh_gencontrol
\tdh_md5sums
\tdh_builddeb
"""
