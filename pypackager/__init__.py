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

## Please wear sunglasses, else it could hurt your eyes

import os
import shutil
import time
from glob import glob
from datetime import datetime

__version__ = '3.7.0'
__build__ = '1'
__author__ = "khertan"
__mail__ = "khertan@khertan.net"
__changelog__ = '''* 3.6.0: Fix permission on script post/pre inst/rm."
* 3.7.0 : Add experimental specfile creation
'''

class PyPackagerException(Exception): pass

class PyPackager(object):

    SECTIONS="user/desktop, user/development, user/education, user/games, user/graphics, user/multimedia, user/navigation, user/network, user/office, user/science, user/system, user/utilities, accessories, communication, games, multimedia, office, other, programming, support, themes, tools".split(", ")
    ARCHS="all any armel i386 ia64 alpha amd64 armeb arm hppa m32r m68k mips mipsel powerpc ppc64 s390 s390x sh3 sh3eb sh4 sh4eb sparc darwin-i386 darwin-ia64 darwin-alpha darwin-amd64 darwin-armeb darwin-arm darwin-hppa darwin-m32r darwin-m68k darwin-mips darwin-mipsel darwin-powerpc darwin-ppc64 darwin-s390 darwin-s390x darwin-sh3 darwin-sh3eb darwin-sh4 darwin-sh4eb darwin-sparc freebsd-i386 freebsd-ia64 freebsd-alpha freebsd-amd64 freebsd-armeb freebsd-arm freebsd-hppa freebsd-m32r freebsd-m68k freebsd-mips freebsd-mipsel freebsd-powerpc freebsd-ppc64 freebsd-s390 freebsd-s390x freebsd-sh3 freebsd-sh3eb freebsd-sh4 freebsd-sh4eb freebsd-sparc kfreebsd-i386 kfreebsd-ia64 kfreebsd-alpha kfreebsd-amd64 kfreebsd-armeb kfreebsd-arm kfreebsd-hppa kfreebsd-m32r kfreebsd-m68k kfreebsd-mips kfreebsd-mipsel kfreebsd-powerpc kfreebsd-ppc64 kfreebsd-s390 kfreebsd-s390x kfreebsd-sh3 kfreebsd-sh3eb kfreebsd-sh4 kfreebsd-sh4eb kfreebsd-sparc knetbsd-i386 knetbsd-ia64 knetbsd-alpha knetbsd-amd64 knetbsd-armeb knetbsd-arm knetbsd-hppa knetbsd-m32r knetbsd-m68k knetbsd-mips knetbsd-mipsel knetbsd-powerpc knetbsd-ppc64 knetbsd-s390 knetbsd-s390x knetbsd-sh3 knetbsd-sh3eb knetbsd-sh4 knetbsd-sh4eb knetbsd-sparc netbsd-i386 netbsd-ia64 netbsd-alpha netbsd-amd64 netbsd-armeb netbsd-arm netbsd-hppa netbsd-m32r netbsd-m68k netbsd-mips netbsd-mipsel netbsd-powerpc netbsd-ppc64 netbsd-s390 netbsd-s390x netbsd-sh3 netbsd-sh3eb netbsd-sh4 netbsd-sh4eb netbsd-sparc openbsd-i386 openbsd-ia64 openbsd-alpha openbsd-amd64 openbsd-armeb openbsd-arm openbsd-hppa openbsd-m32r openbsd-m68k openbsd-mips openbsd-mipsel openbsd-powerpc openbsd-ppc64 openbsd-s390 openbsd-s390x openbsd-sh3 openbsd-sh3eb openbsd-sh4 openbsd-sh4eb openbsd-sparc hurd-i386 hurd-ia64 hurd-alpha hurd-amd64 hurd-armeb hurd-arm hurd-hppa hurd-m32r hurd-m68k hurd-mips hurd-mipsel hurd-powerpc hurd-ppc64 hurd-s390 hurd-s390x hurd-sh3 hurd-sh3eb hurd-sh4 hurd-sh4eb hurd-sparc".split(" ")
    LICENSES=["gpl","lgpl","bsd","artistic","shareware"]

    def __setitem__(self,path,files):
        if not type(files)==list:
            raise PyPackagerException("value of key path '%s' is not a list"%path)
        if not files:
            raise PyPackagerException("value of key path '%s' should'nt be empty"%path)
        if not path.startswith("/"):
            raise PyPackagerException("key path '%s' malformed (don't start with '/')"%path)
        if path.endswith("/"):
            raise PyPackagerException("key path '%s' malformed (shouldn't ends with '/')"%path)
        nfiles=[]
        for file in files:
            if ".." in file:
                raise PyPackagerException("file '%s' contains '..', please avoid that!"%file)
            if "|" in file:
                if file.count("|")!=1:
                    raise PyPackagerException("file '%s' is incorrect (more than one pipe)"%file)
                file,nfile = file.split("|")
            else:
                nfile=file  # same localisation
            if os.path.isdir(file):
                raise PyPackagerException("file '%s' is a folder, and py2deb refuse folders !"%file)
            if not os.path.isfile(file):
                raise PyPackagerException("file '%s' doesn't exist"%file)
            if file.startswith("/"):    # if an absolute file is defined
                if file==nfile:         # and not renamed (pipe trick)
                    nfile=os.path.basename(file)   # it's simply copied to 'path'
            nfiles.append( (file,nfile) )
        nfiles.sort( lambda a,b :cmp(a[1],b[1]))    #sort according new name (nfile)
        self.__files[path]=nfiles

    def __delitem__(self,k):
        del self.__files[k]

    def __init__(self,name):
        self.name = name
        self.display_name = name
        self.description = "No description"
        self.license = "gpl"
        self.depends = "python"
        self.suggests = ""
        self.section = "user/other"
        self.arch = ""
        self.url = "http://"
        self.author = ""
        self.maintainer = ""
        self.email = ""
        self.version = "0.0.0"
        self.buildversion = '1'
        self.__files = {}

        self.preinst = None
        self.postinst = None
        self.prerm = None
        self.postrm = None

        self.changelog = None

        self.bugtracker = ""
        self.icon = None

        #Maemo_Flags (harmattan)
        self.maemo_flags = ''
        #MeeGo_Desktop_Entry_Filename (harmattan)
        self.meego_desktop_entry_filename = ''

        #Aegis Digsigsums
        self.createDigsigsums = False
        #Aegis Manifest
        self.aegisManifest = ''

    def __repr__(self):
        paths=self.__files.keys()
        paths.sort()
        files=[]
        for path in paths:
            for file,nfile in self.__files[path]:
                rfile=os.path.join(path,nfile)
                if nfile==file:
                    files.append( rfile )
                else:
                    files.append( rfile + " (%s)"%file)
        files.sort()
        self.files = "\n".join(files)

        lscripts = [    self.preinst and "preinst",
                        self.postinst and "postinst",
                        self.prerm  and "prerm",
                        self.postrm and "postrm",
                    ]
        self.scripts = lscripts and ", ".join([i for i in lscripts if i]) or "None"
        return """
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
""" % self.__dict__

    def generate(self,build_binary=False,build_src=True):
        if build_binary:
            self.generate_binary()
        if build_src:
            self.generate_source()

    def generate_binary(self):
        from ppkg_debfile import MaemoPackage, ControlFile
        import base64
        try:
            iconb64 = "".join(base64.encodestring(open(self.icon).read()).split("\n")[0:-1])
        except:
            iconb64= ''

        theMaemoPackage = MaemoPackage(
          ControlFile(Icon=str(iconb64),
          BugTracker=self.bugtracker,
          DisplayName=self.display_name,
          PreInst=self.preinst,
          PostInst=self.postinst,
          PreRm=self.prerm,
          PostRm=self.postrm,
          Package=self.name,
          Version=self.version+'-'+self.buildversion,
          Section=self.section,
          Priority='low',
          Architecture=self.arch,
          Maintainer=self.maintainer,
          Depends=self.depends,
          Suggest=self.suggests,
          Description=self.description,
          UpgradeDescription=self.upgrade_description,
          MaemoFlags=self.maemo_flags,
          MeegoDesktopEntryFilename=self.meego_desktop_entry_filename,
          createDigsigsums=self.createDigsigsums,
          aegisManifest = self.aegisManifest),
          self.__files)

        open(self.name+'_'+self.version+'-'+self.buildversion+'_'+self.arch+ '.deb',"wb").write(theMaemoPackage.packed())

        #Dsc
        from ppkg_dscfile import DscFile
        import locale
        try:
            old_locale,iso=locale.getlocale(locale.LC_TIME)
            locale.setlocale(locale.LC_TIME,'en_US')
        except:
            pass
        dsccontent = DscFile("%(version)s-%(buildversion)s"%self.__dict__,
                   "%(depends)s"%self.__dict__,
                   ("%(name)s_%(version)s-%(buildversion)s_%(arch)s.deb"%self.__dict__,),
                   Format='1.0',
                   Source="%(name)s"%self.__dict__,
                   Version="%(version)s-%(buildversion)s"%self.__dict__,
                   Maintainer="%(maintainer)s <%(email)s>"%self.__dict__,
                   Architecture="%(arch)s"%self.__dict__,
                  )
        f = open("%(name)s_%(version)s-%(buildversion)s.dsc"%self.__dict__,"wb")
        f.write(dsccontent._getContent())
        f.close()
        #Changes
        from ppkg_changesfile import ChangesFile
        changescontent = ChangesFile(
                        "%(author)s <%(email)s>"%self.__dict__,
                        "%(description)s"%self.__dict__,
                        "%(changelog)s"%self.__dict__,
                        (
                               "%(name)s_%(version)s-%(buildversion)s_%(arch)s.deb"%self.__dict__,
                               "%(name)s_%(version)s-%(buildversion)s.dsc"%self.__dict__,
                        ),
                        "%(section)s"%self.__dict__,
                        "%(repository)s"%self.__dict__,
                        Format='1.7',
                        Date=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),
                        Source="%(name)s"%self.__dict__,
                        Architecture="%(arch)s"%self.__dict__,
                        Version="%(version)s-%(buildversion)s"%self.__dict__,
                        Distribution="%(distribution)s"%self.__dict__,
                        Urgency="%(urgency)s"%self.__dict__,
                        Maintainer="%(maintainer)s <%(email)s>"%self.__dict__
                        )
        f = open("%(name)s_%(version)s-%(buildversion)s.changes"%self.__dict__,"wb")
        f.write(changescontent.getContent())
        f.close()
        try:
            locale.setlocale(locale.LC_TIME,old_locale)
        except:
            pass

    def generate_source(self):
        """ generate a deb of version 'version', with or without 'changelog', with or without a rpm
            (in the current folder)
            return a list of generated files
        """
        if not sum([len(i) for i in self.__files.values()])>0:
            raise PyPackagerException("no files are defined")

        if not self.changelog:
            self.changelog="  * no changelog"

        if self.section not in PyPackager.SECTIONS:
            raise PyPackagerException("section '%s' is unknown (%s)" % (self.section,str(PyPackager.SECTIONS)))

        if self.arch not in PyPackager.ARCHS:
            raise PyPackagerException("arch '%s' is unknown (%s)"% (self.arch,str(PyPackager.ARCHS)))

        if self.license not in PyPackager.LICENSES:
            raise PyPackagerException("License '%s' is unknown (%s)" % (license,str(PyPackager.LICENSES)))

        # create dates (buildDate,buildDateYear)
        d=datetime.now()
        self.buildDate=d.strftime("%a, %d %b %Y %H:%M:%S +0000")
        self.buildDateYear=str(d.year)

        #clean description (add a space before each next lines)
        self.description=self.description.replace("\r","").strip()
        self.description = "\n ".join(self.description.split("\n"))

        #clean upgrade_description (add a space before each next lines)
        self.upgrade_description=self.upgrade_description.replace("\r","").strip()
        self.upgrade_description = "\n ".join(self.upgrade_description.split("\n"))

        #Really crappy
        self.changelog=self.changelog.replace('\r','').strip()
        changeslog = ''
        for line in self.changelog.split('\n'):
            changeslog = changeslog + '  '+line+'\n'
        self.changelog = changeslog

        self.TEMP = ".pypackager_build_folder"
        DEST = os.path.join(self.TEMP,self.name)
        DEBIAN = os.path.join(DEST,"debian")

        # let's start the process
        try:
            shutil.rmtree(self.TEMP)
        except:
            pass

        os.makedirs(DEBIAN)
        try:
            rules=[]
            dirs=[]
            for path in self.__files:
                for ofile,nfile in self.__files[path]:
                    if os.path.isfile(ofile):
                        # it's a file

                        if ofile.startswith("/"): # if absolute path
                            # we need to change dest
                            dest=os.path.join(DEST,nfile)
                        else:
                            dest=os.path.join(DEST,ofile)

                        # copy file to be packaged
                        destDir = os.path.dirname(dest)
                        if not os.path.isdir(destDir):
                            os.makedirs(destDir)

                        shutil.copy2(ofile,dest)

                        ndir = os.path.join(path,os.path.dirname(nfile))
                        nname = os.path.basename(nfile)

                        # make a line RULES to be sure the destination folder is created
                        # and one for copying the file
                        fpath = "/".join(["$(CURDIR)","debian",self.name+ndir])
                        rules.append('mkdir -p "%s"' % fpath)
                        rules.append('cp -a "%s" "%s"' % (ofile,os.path.join(fpath,nname)))

                        # append a dir
                        dirs.append(ndir)

                    else:
                        raise PyPackagerException("unknown file '' "%ofile) # shouldn't be raised (because controlled before)

            # make rules right
            self.rules= "\n\t".join(rules) +  "\n"

            # make dirs right
            dirs= [ i[1:] for i in set(dirs)]
            dirs.sort()

            #==========================================================================
            # CREATE debian/dirs
            #==========================================================================
            open(os.path.join(DEBIAN,"dirs"),"wb").write("\n".join(dirs))

            #==========================================================================
            # CREATE debian/changelog
            #==========================================================================
            clog="""%(name)s (%(version)s-%(buildversion)s) stable; urgency=low

  %(changelog)s

 -- %(author)s <%(email)s>  %(buildDate)s
  """ % self.__dict__

            open(os.path.join(DEBIAN,"changelog"),"wb").write(clog)

            #==========================================================================
            #Create pre/post install/remove
            #==========================================================================
            def mkscript( name , dest ):
                if name and name.strip()!="":
                    if (os.path.isfile(name)):# or (os.path.isfile(os.path.join(CURRENT,name))):    # it's a file
                        content = file(name).read()
                    else:   # it's a script
                        content = name
                    print os.path.join(DEBIAN,dest)
                    open(os.path.join(DEBIAN,dest),"wb").write(content)

            mkscript(self.preinst ,"preinst")
            mkscript(self.postinst,"postinst")
            mkscript(self.prerm  ,"prerm")
            mkscript(self.postrm ,"postrm")


            #==========================================================================
            # CREATE debian/compat
            #==========================================================================
            open(os.path.join(DEBIAN,"compat"),"w").write("7\n")

            #==========================================================================
            # CREATE icon
            #==========================================================================
            self.iconstr = ""
            if self.icon is not None and os.path.exists(self.icon):
                try:
                    import base64
                    iconb64 = "".join(base64.encodestring(open(self.icon).read()).split("\n")[0:-1])
                    self.iconstr = "XB-Maemo-Icon-26: %s" % ( iconb64 )
                except:
                    pass
            #==========================================================================
            # CREATE bugtracker
            #==========================================================================
            self.bugtrackerstr = "XSBC-Bugtracker: %s" % ( self.bugtracker )

            self.build_depends = 'debhelper (>= 8.0.0)'
            self.build_depends = self.build_depends + ", pkg-config, aegis-builder" if (self.aegisManifest) else ''
            #==========================================================================
            # CREATE debian/control
            #==========================================================================
            txt="""Source: %(name)s
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
%(iconstr)s""" % self.__dict__

            open(os.path.join(DEBIAN,"control"),"wb").write(txt)

            #==========================================================================
            # CREATE debian/copyright
            #==========================================================================
            copy={}
            copy["gpl"]="""
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
"""
            copy["lgpl"]="""
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
"""
            copy["bsd"]="""
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
"""
            copy["shareware"]="""
This product is copyrighted shareware, not public-domain software.
You may use the unregistered version at no charge for an evaluation period.
To continue to use the software beyond evaluation period, you must register it.

THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES
OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""
            copy["artistic"]="""
This program is free software; you can redistribute it and/or modify it
under the terms of the "Artistic License" which comes with Debian.

THIS PACKAGE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES
OF MERCHANTIBILITY AND FITNESS FOR A PARTICULAR PURPOSE.

On Debian systems, the complete text of the Artistic License
can be found in `/usr/share/common-licenses/Artistic'.
"""

            self.txtLicense = copy[self.license]
            self.pv=__version__
            txt="""This package was pypackaged(%(pv)s) by %(author)s <%(email)s> on
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
""" % self.__dict__
            open(os.path.join(DEBIAN,"copyright"),"wb").write(txt)

            #==========================================================================
            # CREATE debian/rules
            #==========================================================================
            txt="""#!/usr/bin/make -f
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
""" % self.__dict__
            if self.aegisManifest:
                txt = txt + '\taegis-deb-add -control debian/%(name)s/DEBIAN/control .. debian/%(name)s.aegis=_aegis' % self.__dict__
            txt = txt + """
binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install configure
""" % self.__dict__
            open(os.path.join(DEBIAN,"rules"),"wb").write(txt)
            os.chmod(os.path.join(DEBIAN,"rules"),0755)

            ###########################################################################
            ###########################################################################
            ###########################################################################

            #http://www.debian.org/doc/manuals/maint-guide/ch-build.fr.html
            #ret=os.system('cd "%(DEST)s"; dpkg-buildpackage -tc -rfakeroot -us -uc' % locals())
            #if ret!=0:
            #    raise Py2debException("buildpackage failed (see output)")

            #==========================================================================
            # CREATE debian/digsigsums
            #==========================================================================
            if self.createDigsigsums:
                from ppkg_digsigsums import generate_digsigsums
                open(os.path.join(DEBIAN,"digsigsums"),"wb").write(generate_digsigsums(self.name, self.__files))

            #==========================================================================
            # CREATE debian/_aegis manifest
            # <aegis name="...">
            #  <provide> ... </provide>
            #  <constraint> ... </constraint>
            #  <account> ... </account>
            #  <request> ... </request>
            #  <domain> ... </domain>
            #  <docstring> ... </docstring>
            #</aegis>'''
            #==========================================================================

            if self.aegisManifest:
                mkscript(self.aegisManifest, '%s.aegis' % self.__dict__['name'])


            #Tar
            from ppkg_tarfile import myTarFile
            tarcontent= myTarFile("%(DEST)s" % locals() )
            open("%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.tar.gz"%self.__dict__,"wb").write(tarcontent.packed())
            #Dsc
            from ppkg_dscfile import DscFile
            import locale
            try:
                old_locale,iso=locale.getlocale(locale.LC_TIME)
                locale.setlocale(locale.LC_TIME,'en_US')
            except:
                pass
            dsccontent = DscFile('%(version)s-%(buildversion)s' % self.__dict__,
                       self.build_depends,
                       ('%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.tar.gz' % self.__dict__, ),
                       Format='1.0',
                       Source="%(name)s"%self.__dict__,
                       Version="%(version)s-%(buildversion)s"%self.__dict__,
                       Maintainer="%(maintainer)s <%(email)s>"%self.__dict__,
                       Architecture="%(arch)s"%self.__dict__,
                      )
            f = open("%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.dsc"%self.__dict__,"wb")
            f.write(dsccontent._getContent())
            f.close()

            #Changes
            from ppkg_changesfile import ChangesFile
            changescontent = ChangesFile(
                            "%(author)s <%(email)s>"%self.__dict__,
                            "%(description)s"%self.__dict__,
                            "%(changelog)s"%self.__dict__,
                            (
                                   "%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.tar.gz"%self.__dict__,
                                   "%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.dsc"%self.__dict__,
                            ),
                            "%(section)s"%self.__dict__,
                            "%(repository)s"%self.__dict__,
                            Format='1.7',
                            Date=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()),
                            Source="%(name)s"%self.__dict__,
                            Architecture="%(arch)s"%self.__dict__,
                            Version="%(version)s-%(buildversion)s"%self.__dict__,
                            Distribution="%(distribution)s"%self.__dict__,
                            Urgency="%(urgency)s"%self.__dict__,
                            Maintainer="%(maintainer)s <%(email)s>"%self.__dict__
                            )
            f = open("%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.changes"%self.__dict__,"wb")
            f.write(changescontent.getContent())
            f.close()

            #Specs
            from ppkg_specfile import SpecFile
            #Specific for rpm
            changeslog = ('* ' + time.strftime("%a %b %d %Y", time.gmtime()) \
                         +  " %(author)s <%(email)s> - %(version)s-%(buildversion)s\n" % self.__dict__)
            for index, line in enumerate(self.changelog.split('\n')):
                if line.startswith('-'):
                    changeslog = changeslog + line + '\n'
                else:
                    changeslog = changeslog + '- %s\n' % line
            self.changeslog = changeslog
            self.builddepends = 'python-devel'
            self.sources = "%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.tar.gz"%self.__dict__
            specfile = SpecFile( self.__dict__)
            f = open("%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.spec"%self.__dict__,"wb")
            f.write(specfile.content)
            f.close()

            try:
                locale.setlocale(locale.LC_TIME,old_locale)
            except:
                pass


            ret = []
            l=glob("%(TEMP)s/%(name)s*.tar.gz"%self.__dict__)
            if len(l)!=1:
                raise PyPackagerException("don't find source package tar.gz")
            tar = os.path.basename(l[0])
            shutil.move(l[0],tar)
            ret.append(tar)
            l=glob("%(TEMP)s/%(name)s*.dsc"%self.__dict__)
            if len(l)!=1:
                raise PyPackagerException("don't find source package dsc")
            tar = os.path.basename(l[0])
            shutil.move(l[0],tar)
            ret.append(tar)
            l=glob("%(TEMP)s/%(name)s*.changes"%self.__dict__)
            if len(l)!=1:
                raise PyPackagerException("don't find source package changes")
            tar = os.path.basename(l[0])
            shutil.move(l[0],tar)
            ret.append(tar)
            l=glob("%(TEMP)s/%(name)s*.spec"%self.__dict__)
            if len(l)!=1:
                raise PyPackagerException("don't find source package spec")
            tar = os.path.basename(l[0])
            shutil.move(l[0],tar)
            ret.append(tar)

            return ret

        finally:
            shutil.rmtree(self.TEMP)

if __name__ == "__main__":
    print 'Look at make.py in the git repository to see how to use it'
