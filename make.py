import pypackager
import os
p=pypackager.PyPackager("pypackager-gui")
p.display_name = "PyPackager GUI"
p.version = "1.0.0"
p.buildversion == "1"
p.description=""""""
p.author="t"
p.maintainer="t"
p.email="k"
p.depends = "python2.5, pypackager"
p.section="user/development"
p.arch="armel"
p.urgency="low"
p.distribution="fremantle"
p.repository="extras-devel"
p.bugtracker = "k"
p.postinstall="""#!/bin/sh
chmod +x /usr/bin/pychecker"""
p.changelog ="""
  * First Fremantle Release
"""
dir_name="/home/user/MyDocs/Projects/pypackager"
for root, dirs, files in os.walk(dir_name):
  real_dir = root[len(dir_name):]
  fake_file = []
  for f in files:
      fake_file.append(root + os.sep + f + "|" + f)
  if len(fake_file) > 0:
      p[real_dir] = fake_file
print p.generate(build_binary=False,build_src=True)
print p.generate(build_binary=True,build_src=False)
