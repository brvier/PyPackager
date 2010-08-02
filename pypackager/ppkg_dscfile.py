#!/usr/bin/python

import os 
import md5hash

class DscFile(object):

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
            md5=md5hash.md5sum(onefile)
            size=os.stat(onefile).st_size.__str__()
            content.append(' '+md5 + ' ' + size +' '+os.path.basename(onefile))

        print "\n".join(content)+"\n"
        return "\n".join(content)+"\n\n"

    content = property(_getContent, doc="")