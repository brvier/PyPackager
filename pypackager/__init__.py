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

__version__ = '4.0.0'
__build__ = '1'
__author__ = "khertan"
__mail__ = "khertan@khertan.net"
__changelog__ = '''* 3.6.0: Fix permission on script post/pre inst/rm."
* 3.7.0 : Add experimental specfile creation
* 3.7.1 : fix incorrect generation of the spec file
* 3.7.2 : fix error in spec file
* 3.7.3 : add possibilities to have different dependancies for spec / deb
* 4.0.0 : Put builded packages in different sub folder as changes file for
          debian and rpm source have same name but different structure.
          Cleaning code'''


class PyPackagerException(Exception):
    pass


class PyPackager(object):

    def __setitem__(self, path, files):
        if not type(files) == list:
            raise PyPackagerException("value of key path '%s' is not a list"
                                      % path)
        if not files:
            raise PyPackagerException("value of key path '%s'"
                                      " should'nt be empty" % path)
        if not path.startswith("/"):
            raise PyPackagerException("key path '%s' malformed"
                                      " (don't start with '/')" % path)
        if path.endswith("/"):
            raise PyPackagerException("key path '%s' malformed"
                                      " (shouldn't ends with '/')" % path)
        nfiles = []
        for file in files:
            if ".." in file:
                raise PyPackagerException("file '%s' contains"
                                          " '..', please avoid that!" % file)
            if "|" in file:
                if file.count("|") != 1:
                    raise PyPackagerException("file '%s' is incorrect"
                                              " (more than one pipe)" % file)
                file, nfile = file.split("|")
            else:
                nfile = file  # same localisation
            if os.path.isdir(file):
                raise PyPackagerException("file '%s' is a folder,"
                                          " and PyPackager refuse folders !"
                                          % file)
            if not os.path.isfile(file):
                raise PyPackagerException("file '%s' doesn't exist" % file)
            if file.startswith("/"):    # if an absolute file is defined
                if file == nfile:         # and not renamed (pipe trick)
                    nfile = os.path.basename(file)  # it's simply
                                                    #copied to 'path'
            nfiles.append((file, nfile))
        #sort according new name (nfile)
        nfiles.sort(lambda a, b: cmp(a[1], b[1]))
        self.__files[path] = nfiles

    def __delitem__(self, k):
        del self.__files[k]

    def __init__(self, name):
        self.name = name
        self.display_name = name
        self.summary = 'No summary'
        self.description = "No description"
        self.license = "gpl"
        self.depends = "python"
        self.rpm_depends = None
        self.suggests = ""
        self.section = "user/other"
        self.arch = ""

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

        self.url = "http://"
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
        from ppkg_constants import PPKG_RETURN
        paths = self.__files.keys()
        paths.sort()
        files = []
        for path in paths:
            for afile, nfile in self.__files[path]:
                rfile = os.path.join(path, nfile)
                if nfile == afile:
                    files.append(rfile)
                else:
                    files.append(rfile + " (%s)" % afile)
        files.sort()
        self.files = "\n".join(files)

        lscripts = [self.preinst and "preinst",
                    self.postinst and "postinst",
                    self.prerm and "prerm",
                    self.postrm and "postrm", ]
        self.scripts = lscripts and \
            ", ".join([i for i in lscripts if i]) or "None"
        return PPKG_RETURN % self.__dict__

    def _create_dist_folder(self):
        if not os.path.exists('dists'):
            os.mkdir('dists')
        self._dist_dir = os.path.join(os.path.join('dists',
                                                   self.version
                                                   + '-'
                                                   + self.buildversion))
        if not os.path.exists(self._dist_dir):
            os.mkdir(self._dist_dir)

    def generate(self, options):
        self._create_dist_folder()

        if 'debian_binary' in options:
            self.generate_debian_binary()
        if 'debian_source' in options:
            self.generate_debian_source()
        if 'rpm_source' in options:
            self.generate_rpm_source()

    def generate_debian_binary(self):
        from ppkg_debfile import MaemoPackage, ControlFile
        import base64

        #Create debian binary dist folder
        _dist_dir = os.path.join(self._dist_dir, 'debian_binary')
        if not os.path.exists(_dist_dir):
            os.mkdir(_dist_dir)

        try:
            iconb64 = "".join(base64.encodestring(
                open(self.icon).read()).split("\n")[0:-1])
        except:
            iconb64 = ''

        theMaemoPackage = MaemoPackage(
            ControlFile(Icon=str(iconb64),
                        BugTracker=self.bugtracker,
                        DisplayName=self.display_name,
                        PreInst=self.preinst,
                        PostInst=self.postinst,
                        PreRm=self.prerm,
                        PostRm=self.postrm,
                        Package=self.name,
                        Version=self.version + '-' + self.buildversion,
                        Section=self.section,
                        Priority='low',
                        Architecture=self.arch,
                        Maintainer=self.maintainer,
                        Depends=self.depends,
                        Suggest=self.suggests,
                        Description=self.description,
                        UpgradeDescription=self.upgrade_description,
                        MaemoFlags=self.maemo_flags,
                        MeegoDesktopEntryFilename=
                        self.meego_desktop_entry_filename,
                        createDigsigsums=self.createDigsigsums,
                        aegisManifest=self.aegisManifest),
            self.__files)

        open(os.path.join(_dist_dir, self.name
                          + '_'
                          + self.version
                          + '-' + self.buildversion
                          + '_' + self.arch
                          + '.deb'), "wb").write(theMaemoPackage.packed())

        #Dsc
        from ppkg_dscfile import DscFile
        import locale
        try:
            old_locale, iso = locale.getlocale(locale.LC_TIME)
            locale.setlocale(locale.LC_TIME, 'en_US')
        except:
            pass

        print os.path.join(_dist_dir, "%(name)s_%(version)s-"
                           "%(buildversion)s_%(arch)s.deb" % self.__dict__)
        dsccontent = DscFile("%(version)s-%(buildversion)s" % self.__dict__,
                             "%(depends)s" % self.__dict__,
                             (os.path.join(_dist_dir, "%(name)s_%(version)s-"
                             "%(buildversion)s_%(arch)s.deb"
                             % self.__dict__), ),
                             Format='1.0',
                             Source="%(name)s" % self.__dict__,
                             Version="%(version)s-%(buildversion)s"
                             % self.__dict__,
                             Maintainer="%(maintainer)s <%(email)s>"
                             % self.__dict__,
                             Architecture="%(arch)s" % self.__dict__,)
        f = open(os.path.join(_dist_dir,
                              "%(name)s_%(version)s-%(buildversion)s.dsc"
                              % self.__dict__), "wb")
        f.write(dsccontent._getContent())
        f.close()

        #Changes
        from ppkg_changesfile import ChangesFile
        changescontent = ChangesFile(
            "%(author)s <%(email)s>" % self.__dict__,
            "%(description)s" % self.__dict__,
            "%(changelog)s" % self.__dict__,
            (os.path.join(_dist_dir,
                          "%(name)s_%(version)s-%(buildversion)s_%(arch)s.deb"
             % self.__dict__,),
             os.path.join(_dist_dir,
                          "%(name)s_%(version)s-%(buildversion)s.dsc"
             % self.__dict__, ),),
            "%(section)s" % self.__dict__,
            "%(repository)s" % self.__dict__,
            Format='1.7',
            Date=time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                               time.gmtime()),
            Source="%(name)s" % self.__dict__,
            Architecture="%(arch)s" % self.__dict__,
            Version="%(version)s-%(buildversion)s" % self.__dict__,
            Distribution="%(distribution)s" % self.__dict__,
            Urgency="%(urgency)s" % self.__dict__,
            Maintainer="%(maintainer)s <%(email)s>" % self.__dict__)
        f = open(os.path.join(_dist_dir,
                              "%(name)s_%(version)s-%(buildversion)s.changes"
                              % self.__dict__), "wb")
        f.write(changescontent.getContent())
        f.close()
        try:
            locale.setlocale(locale.LC_TIME, old_locale)
        except:
            pass

    def generate_common_source(self, _dist_dir):
        from ppkg_constants import PPKG_SECTIONS, PPKG_ARCHS, PPKG_LICENSES, \
            PPKG_DEBIAN_CHANGESLOG, PPKG_DEBIAN_CONTROL, PPKG_LICENSES_TEXT, \
            PPKG_COPYRIGHT, PPKG_DEBIAN_RULE

        if not sum([len(i) for i in self.__files.values()]) > 0:
            raise PyPackagerException("no files are defined")

        if not self.changelog:
            self.changelog = "  * no changelog"

        if self.section not in PPKG_SECTIONS:
            raise PyPackagerException("section '%s' is unknown (%s)"
                                      % (self.section,
                                      str(PyPackager.SECTIONS)))

        if self.arch not in PPKG_ARCHS:
            raise PyPackagerException("arch '%s' is unknown (%s)"
                                      % (self.arch,
                                      str(PyPackager.ARCHS)))

        if self.license not in PPKG_LICENSES:
            raise PyPackagerException("License '%s' is unknown (%s)"
                                      % (license,
                                      str(PyPackager.LICENSES)))

        # create dates (buildDate,buildDateYear)
        d = datetime.now()
        self.buildDate = d.strftime("%a, %d %b %Y %H:%M:%S +0000")
        self.buildDateYear = str(d.year)

        #clean description (add a space before each next lines)
        self.description = self.description.replace("\r", "").strip()
        self.description = "\n ".join(self.description.split("\n"))

        #clean upgrade_description (add a space before each next lines)
        self.upgrade_description = \
            self.upgrade_description.replace("\r", "").strip()
        self.upgrade_description = \
            "\n ".join(self.upgrade_description.split("\n"))

        #Really crappy
        self.changelog = self.changelog.replace('\r', '').strip()
        changeslog = ''
        for line in self.changelog.split('\n'):
            changeslog = changeslog + '  ' + line + '\n'
        self.changelog = changeslog

        self.TEMP = ".pypackager_build_folder"
        DEST = os.path.join(self.TEMP, self.name)
        DEBIAN = os.path.join(DEST, "debian")

        # let's start the process
        try:
            shutil.rmtree(self.TEMP)
        except:
            pass

        os.makedirs(DEBIAN)
        try:
            rules = []
            dirs = []
            for path in self.__files:
                for ofile, nfile in self.__files[path]:
                    if os.path.isfile(ofile):
                        # it's a file

                        if ofile.startswith("/"):  # if absolute path
                            # we need to change dest
                            dest = os.path.join(DEST, nfile)
                        else:
                            dest = os.path.join(DEST, ofile)

                        # copy file to be packaged
                        destDir = os.path.dirname(dest)
                        if not os.path.isdir(destDir):
                            os.makedirs(destDir)

                        shutil.copy2(ofile, dest)

                        ndir = os.path.join(path, os.path.dirname(nfile))
                        nname = os.path.basename(nfile)

                        # make a line RULES to be sure the destination folder
                        # and one for copying the file is created
                        fpath = "/".join(["$(CURDIR)", "debian",
                                self.name + ndir])
                        rules.append('mkdir -p "%s"' % fpath)
                        rules.append('cp -a "%s" "%s"'
                                     % (ofile, os.path.join(fpath, nname)))

                        # append a dir
                        dirs.append(ndir)

                    else:
                        # shouldn't be raised (because controlled before)
                        raise PyPackagerException("unknown file '' " % ofile)

            # make rules right
            self.rules = "\n\t".join(rules) + "\n"

            # make dirs right
            dirs = [i[1:] for i in set(dirs)]
            dirs.sort()

            #===================================================
            # CREATE debian/dirs
            #===================================================
            open(os.path.join(DEBIAN, "dirs"), "wb").write("\n".join(dirs))

            #===================================================
            # CREATE debian/changelog
            #===================================================
            clog = PPKG_DEBIAN_CHANGESLOG % self.__dict__

            open(os.path.join(DEBIAN, "changelog"), "wb").write(clog)

            #===================================================
            #Create pre/post install/remove
            #===================================================
            def mkscript(name, dest):
                if name and name.strip() != "":
                    if (os.path.isfile(name)):
                        content = file(name).read()
                    else:   # it's a script
                        content = name
                    print os.path.join(DEBIAN, dest)
                    open(os.path.join(DEBIAN, dest), "wb").write(content)

            mkscript(self.preinst, "preinst")
            mkscript(self.postinst, "postinst")
            mkscript(self.prerm, "prerm")
            mkscript(self.postrm, "postrm")

            #===================================================
            # CREATE debian/compat
            #===================================================
            open(os.path.join(DEBIAN, "compat"), "w").write("7\n")

            #===================================================
            # CREATE icon
            #===================================================
            self.iconstr = ""
            if self.icon is not None and os.path.exists(self.icon):
                try:
                    import base64
                    iconb64 = "".join(base64.encodestring(
                        open(self.icon).read()).split("\n")[0:-1])
                    self.iconstr = "XB-Maemo-Icon-26: %s" % (iconb64)
                except:
                    pass

            #===================================================
            # CREATE bugtracker
            #===================================================
            self.bugtrackerstr = "XSBC-Bugtracker: %s" % (self.bugtracker)

            self.build_depends = 'debhelper (>= 8.0.0)'
            self.build_depends = self.build_depends \
                + ", pkg-config, aegis-builder" \
                if (self.aegisManifest) else ''

            #===================================================
            # CREATE debian/control
            #===================================================
            txt = PPKG_DEBIAN_CONTROL % self.__dict__

            open(os.path.join(DEBIAN, "control"), "wb").write(txt)

            #===================================================
            # CREATE debian/copyright
            #===================================================

            self.txtLicense = PPKG_LICENSES_TEXT[self.license]
            self.pv = __version__
            txt = PPKG_COPYRIGHT % self.__dict__
            open(os.path.join(DEBIAN, "copyright"), "wb").write(txt)

            #===================================================
            # CREATE debian/rules
            #===================================================
            txt = PPKG_DEBIAN_RULE % self.__dict__
            if self.aegisManifest:
                txt = txt + ('\taegis-deb-add -control debian/%(name)s/'
                             'DEBIAN/control ..'
                             ' debian/%(name)s.aegis=_aegis' % self.__dict__)
            txt = txt + """
binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install configure
""" % self.__dict__
            open(os.path.join(DEBIAN, "rules"), "wb").write(txt)
            os.chmod(os.path.join(DEBIAN, "rules"), 0755)

            #===================================================
            # CREATE debian/digsigsums
            #===================================================
            if self.createDigsigsums:
                from ppkg_digsigsums import generate_digsigsums
                open(os.path.join(DEBIAN, "digsigsums"), "wb") \
                    .write(generate_digsigsums(self.name, self.__files))

            #===================================================
            # CREATE debian/_aegis manifest
            # <aegis name="...">
            #  <provide> ... </provide>
            #  <constraint> ... </constraint>
            #  <account> ... </account>
            #  <request> ... </request>
            #  <domain> ... </domain>
            #  <docstring> ... </docstring>
            #</aegis>'''
            #===================================================

            if self.aegisManifest:
                mkscript(self.aegisManifest, '%s.aegis'
                         % self.__dict__['name'])

            #Tar
            from ppkg_tarfile import myTarFile
            tarcontent = myTarFile("%(DEST)s" % locals())
            open("%(TEMP)s/%(name)s_%(version)s-%(buildversion)s.tar.gz"
                 % self.__dict__, "wb").write(tarcontent.packed())

            l = glob("%(TEMP)s/%(name)s*.tar.gz" % self.__dict__)
            if len(l) != 1:
                raise PyPackagerException("don't find source package tar.gz")
            tar = os.path.join(_dist_dir, os.path.basename(l[0]))
            shutil.move(l[0], tar)
        except:
            return False
        return True

    def generate_rpm_source(self):
        _dist_dir = os.path.join(self._dist_dir, 'rpm_source')
        if not os.path.exists(_dist_dir):
            os.mkdir(_dist_dir)
        if self.generate_common_source(_dist_dir):

            #Specs
            from ppkg_specfile import SpecFile
            import locale
            try:
                old_locale, iso = locale.getlocale(locale.LC_TIME)
                locale.setlocale(locale.LC_TIME, 'en_US')
            except:
                pass

            #Write spec
            self.builddepends = 'python-devel'
            if self.rpm_depends is None:
                self.rpm_depends = self.depends
            else:
                self.depends = self.rpm_depends
            self.sources = os.path.join(_dist_dir,
                                        "%(name)s_%(version)s-"
                                        "%(buildversion)s.tar.gz"
                                        % self.__dict__)
            specfile = SpecFile(self.__dict__)
            f = open(os.path.join(_dist_dir,
                                  "%(name)s_%(version)s"
                                  "-%(buildversion)s.spec"
                                  % self.__dict__), "wb")

            #Write changes
            changeslog = ('* ' + time.strftime("%a %b %d %Y", time.gmtime())
                          + (" %(author)s <%(email)s> - "
                             "%(version)s-%(buildversion)s\n")
                          % self.__dict__)
            for index, line in enumerate(self.changelog.split('\n')):
                if line.startswith('-'):
                    changeslog = changeslog + line + '\n'
                else:
                    changeslog = changeslog + '- %s\n' % line

            f.write(specfile.content)
            f = open(os.path.join(_dist_dir,
                                  "%(name)s_%(version)s"
                                  "-%(buildversion)s.changes"
                                  % self.__dict__), "wb")
            f.write(changeslog)
            f.close()

            try:
                locale.setlocale(locale.LC_TIME, old_locale)
            except:
                pass

            shutil.rmtree(self.TEMP)

    def generate_debian_source(self):
        _dist_dir = os.path.join(self._dist_dir, 'debian_source')
        if not os.path.exists(_dist_dir):
            os.mkdir(_dist_dir)
        if self.generate_common_source(_dist_dir):

            #Dsc
            from ppkg_dscfile import DscFile
            import locale
            try:
                old_locale, iso = locale.getlocale(locale.LC_TIME)
                locale.setlocale(locale.LC_TIME, 'en_US')
            except:
                pass
            dsccontent = DscFile('%(version)s-%(buildversion)s'
                                 % self.__dict__,
                                 self.build_depends,
                                 (os.path.join(_dist_dir,
                                               '%(name)s_%(version)s'
                                               '-%(buildversion)s.tar.gz'
                                               % self.__dict__, ),),
                                 Format='1.0',
                                 Source="%(name)s" % self.__dict__,
                                 Version="%(version)s-%(buildversion)s"
                                 % self.__dict__,
                                 Maintainer="%(maintainer)s <%(email)s>"
                                 % self.__dict__,
                                 Architecture="%(arch)s" % self.__dict__, )

            f = open(os.path.join(_dist_dir,
                                  "%(name)s_%(version)s-%(buildversion)s.dsc"
                                  % self.__dict__), "wb")
            f.write(dsccontent._getContent())
            f.close()

            #Changes
            from ppkg_changesfile import ChangesFile
            changescontent = ChangesFile(
                "%(author)s <%(email)s>" % self.__dict__,
                "%(description)s" % self.__dict__,
                "%(changelog)s" % self.__dict__,
                (
                    os.path.join(_dist_dir,
                                 "%(name)s_%(version)s-%(buildversion)s.tar.gz"
                                 % self.__dict__,),
                    os.path.join(_dist_dir,
                                 "%(name)s_%(version)s-%(buildversion)s.dsc"
                                 % self.__dict__,),
                ),
                "%(section)s" % self.__dict__,
                "%(repository)s" % self.__dict__,
                Format='1.7',
                Date=time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                   time.gmtime()),
                Source="%(name)s" % self.__dict__,
                Architecture="%(arch)s" % self.__dict__,
                Version="%(version)s-%(buildversion)s"
                % self.__dict__,
                Distribution="%(distribution)s" % self.__dict__,
                Urgency="%(urgency)s" % self.__dict__,
                Maintainer="%(maintainer)s <%(email)s>" % self.__dict__)
            f = open(os.path.join(_dist_dir,
                                  "%(name)s_%(version)s-"
                                  "%(buildversion)s.changes"
                                  % self.__dict__), "wb")
            f.write(changescontent.getContent())
            f.close()

            try:
                locale.setlocale(locale.LC_TIME, old_locale)
            except:
                pass

            shutil.rmtree(self.TEMP)

if __name__ == "__main__":
    print 'Look at make.py in the git repository to see how to use it'

