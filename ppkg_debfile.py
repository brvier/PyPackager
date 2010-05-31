#!/usr/bin/python
#
# debfile.py
#
# A pure Python way of producing .deb files suitable installation
# on the Maemo platform.
#
#
# Notes:
#
#  * Intended for use with companion `distutils` `bdist_maemo` command but
#    may also be able to be used standalone.
#
#  * May _also_ be used as a generic .deb packager but it's not
#    been tested for that.
#
#
#  Author: follower@rancidbacon.com
#
#    Date: 15 September 2006
#
# License: GPL 2.0
#
#

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

    def __init__(self,Icon,BugTracker,DisplayName,PreInst,PostInst,PreRm,PostRm,
                 long_description = "",
                 Description = "",
                 **kwargs
                 ):
        """
        """
        self.options = kwargs # TODO: Is order important?

        # TODO: Clean-up special handling of description
        self.description = Description
        self.long_description = long_description
        self.icon = Icon
        self.bugtracker = BugTracker
        self.displayname = DisplayName
        self.preinst=PreInst
        self.postinst=PostInst
        self.prerm=PreRm
        self.postrm=PostRm

    def _getContent(self):
        """
        """
        content = ["%s: %s" % (k, v)
                   for k,v in self.options.iteritems()]
	
        if self.bugtracker:
            content.append("Bugtracker: %s" % self.bugtracker)
        if self.displayname:
            content.append("Maemo-Display-Name: %s" % self.displayname)

        if self.description:
            self.description=self.description.replace("\n","\n ")
            content.append("Description: %s" % self.description)
            
            if self.long_description:
                self.long_description=self.long_description.replace("\n","\n ")
                content.append(" " + self.long_description)

        if self.icon:
            #self.icon=self.icon.replace("\n","\n ")
            content.append("Maemo-Icon-26: \n %s" % self.icon)
            #print self.icon

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

        theFileInfo = tarfile.TarInfo(name = name)
        theFileInfo.mtime = int(time.time()) # Absence seems to break tgz file.
        theFileInfo.size = len(content.getvalue())
        theFileInfo.uid = UID_ROOT
        theFileInfo.gid = GID_ROOT


        self.addfile(theFileInfo, fileobj = content)        


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

        return theDeb.packed()
        
    def _getSize(self):
      size = 0
      paths=self.__files.keys()
      paths.sort()
      files=[]
      CURRENT = os.path.dirname(sys.argv[0])
      for path in paths:
          for pfile,nfile in self.__files[path]:
#              rfile=os.path.join(path,nfile)
#              print pfile,nfile,rfile
#              if nfile==pfile:
#                  tarOutput.addfile(tarinfo, file(os.path.join(os.path.dirname(sys.argv[0]),pfile)))
#                  size = size + (getattr(os.stat(os.path.join(CURRENT,pfile)),'st_size')/1024)
#                    tarOutput.addfile(tarinfo, file(pfile))
#              else:
#                  tarOutput.addfile(tarinfo, file(os.path.join(path, rfile + " (%s)"%file)))
            size = size + (getattr(os.stat(os.path.join(CURRENT,pfile)),'st_size')/1024)
     
#      for folder,ufolders,files in os.walk(self._dataDirectoryPath):
#        for file in files:
#          size = size + (getattr(os.stat(os.path.join(folder,file)),'st_size')/1024)
      return size

    def _getVersionFile(self):
        """
        """
        debVersionFile = \
                ppkg_arfile.FileInfo(name = FILENAME_DEB_VERSION,
                                modificationTime = int(time.time()),
                                userId = UID_ROOT,
                                groupId = GID_ROOT,
                                fileMode = PERMS_URW_GRW_OR,
                                fileSize = len(FILE_CONTENT_DEB_VERSION),
                                data = FILE_CONTENT_DEB_VERSION)

        return debVersionFile


    def _getControlFiles(self):
        """
        """
        debControlFile = self.controlFile.content + 'Installed-Size: '+str(self._getSize())+'\n'

        outputFileObj = StringIO() # TODO: Do more transparently?

        tarOutput = TarFile.open(FILENAME_CONTROL_TAR_GZ,
                                 mode = "w:gz",
                                 fileobj = outputFileObj)

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

        tarOutput.close()

        control_tar_gz = outputFileObj.getvalue()

        controlFile = ppkg_arfile.FileInfo(name = FILENAME_CONTROL_TAR_GZ,
                                      modificationTime = int(time.time()),
                                      userId = UID_ROOT,
                                      groupId = GID_ROOT,
                                      fileMode = PERMS_URW_GRW_OR,
                                      fileSize = len(control_tar_gz),
                                      data = control_tar_gz)

        return controlFile


    def _getDataFiles(self):
        """
        """
        
        outputFileObj = StringIO()

        tarOutput = TarFile.open(FILENAME_DATA_TAR_GZ,
                                 mode = "w:gz",
                                 fileobj = outputFileObj)

        # Note: We can't use this because we need to fiddle permissions:
        #       tarOutput.add(directoryPath, arcname = "")

        # TODO: Add this as a method for TarFile and tidy-up?
        paths=self.__files.keys()
        paths.sort()
        files=[]
        CURRENT = os.path.dirname(os.path.abspath(sys.path[0]))
        for path in paths:
            print '0:',CURRENT,path,os.path.join(CURRENT)
            tarinfo = tarOutput.gettarinfo(os.path.join(CURRENT), path)
            tarinfo.uid = UID_ROOT
            tarinfo.gid = GID_ROOT
            tarinfo.uname = ""
            tarinfo.gname = ""                    
            tarOutput.addfile(tarinfo)
            
               
            
            for pfile,nfile in self.__files[path]:
                rfile=os.path.normpath( os.path.join(path,nfile) )
                #print pfile, nfile, rfile, path
                #rfile=os.path.join(path,nfile)
                if os.path.dirname(rfile)==path:
#                    tarinfo = tarOutput.gettarinfo(os.path.join(os.path.dirname(sys.argv[0]),rfile), os.path.dirname(os.path.join(os.path.dirname(sys.argv[0]),rfile)))
#                    tarinfo = tarfile.TarInfo(name=os.path.join(path,pfile))
#                    tarinfo.name = os.path.join(path,pfile)
#                    tarinfo.uid = UID_ROOT
#                    tarinfo.gid = GID_ROOT
#                    tarinfo.uname = ""
#                    tarinfo.mtime = int(time.time()) # Absence seems to break tgz file.
#                    tarinfo.size = len(content.getvalue())

#                    tarinfo.gname = ""
                    print '1:',os.path.join(path,nfile),(os.path.join(CURRENT,pfile))
                    tarOutput.addfilefromstring(os.path.join(path,nfile),file(os.path.join(CURRENT,pfile)).read())

#                    print '1:',os.path.join(path,pfile),(os.path.join(os.path.dirname(sys.argv[0]),pfile))
#                    tarOutput.addfilefromstring(os.path.join(path,pfile),file(os.path.join(os.path.dirname(sys.argv[0]),pfile)).read())
#                    tarOutput.addfile(tarinfo, file(os.path.join(os.path.dirname(sys.argv[0]),pfile)))
#                    print file(os.path.join(os.path.dirname(sys.argv[0]),pfile)).read()
#                    tarOutput.addfile(tarinfo, file(pfile))
                else:
                    print '2:',path,pfile,nfile,rfile,CURRENT
                    #print '3:',os.path.join(CURRENT,os.path.dirname(pfile)), os.path.join(path,os.path.dirname(pfile))
                    tarinfo = tarOutput.gettarinfo(os.path.join(CURRENT,os.path.dirname(pfile)), os.path.join(path,os.path.dirname(pfile)))
                    tarinfo.uid = UID_ROOT
                    tarinfo.gid = GID_ROOT
                    tarinfo.uname = ""
                    tarinfo.gname = ""
                    tarinfo.mtime = int(time.time())                    
                    tarOutput.addfile(tarinfo)            

                    tarinfo = tarOutput.gettarinfo(os.path.join(CURRENT,pfile), rfile)
                    tarinfo.uid = UID_ROOT
                    tarinfo.gid = GID_ROOT
                    tarinfo.uname = ""
                    tarinfo.gname = ""
#                    tarOutput.addfilefromstring(rfile,file(os.path.join(os.path.dirname(sys.argv[0]),pfile)).read())
                    
                    tarOutput.addfile(tarinfo, file(os.path.join(CURRENT,pfile)))
        tarOutput.close()

        data_tar_gz = outputFileObj.getvalue()

        dataFile = ppkg_arfile.FileInfo(name = FILENAME_DATA_TAR_GZ,
                                   modificationTime = int(time.time()),
                                   userId = UID_ROOT,
                                   groupId = GID_ROOT,
                                   fileMode = PERMS_URW_GRW_OR,
                                   fileSize = len(data_tar_gz),
                                   data = data_tar_gz)
        return dataFile
            
            


if __name__ == "__main__":
    # debian-binary
    # control.tgz
    # data.tgz

    import sys

    try:
        directoryPath = sys.argv[1]
    except IndexError:
        print "Usage: %s <directory path>" % sys.argv[0]
        raise SystemExit

    theMaemoPackage = MaemoPackage(
        ControlFile(Package="pyne4maemo",
                    Version="0.1.0",
                    Section="user/other",
                    Priority="optional",
                    Architecture="all",
                    Maintainer="Benoit HERVIER <khertan@khertan.net>",
                    Depends="python2.5, python2.5-hildon, python2.5-gtk2",
                    Description="Example packaged Maemo application."
                    ),
        directoryPath
        )

    open(os.path.join(directoryPath + '.deb'),
             "wb").write(theMaemoPackage.packed())
    
                                     

    

