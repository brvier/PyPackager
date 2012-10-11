import os

from setuptools import setup
import pypackager

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pypackager",
    version = pypackager.__version__,
    author = "Benoit HERVIER",
    author_email = "khertan@khertan.net",
    description = ("PyPackager is an onboard developpers tools"+
                   "which is usefull to create sources and binary"+
                   "Maemo/Harmattan/MeeGo package."),
    license = "GPL",
    keywords = "package debian maemo",
    url = "http://khertan.net/pypackager",
    packages= ['pypackager'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",]
,)
