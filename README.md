PyPackager
==========

**Licence :** GPLv3
**Source :** [GitHub Repository](https://github.com/khertan/pypackager)
**Download (Maemo):** [PyPackager on Maemo Repository](http://maemo.org/packages/view/pypackager/)
**Download (Meego):** [PyPackager on MeeGo Repository](http://repo.pub.meego.com/home:/khertan/Harmattan/armel/)
**Bugs Tracker :** [PyPackager Bug Tracker](https://github.com/khertan/pypackager/issues)
**Plateform :** Maemo Diablo, Maemo Fremantle

PyPackager is an onboard developpers tools which is usefull to create sources
and binary Maemo package.

![PyPackager Source screenshot](http://khertan.net/medias/pypackager.jpg)

## PyPackager HowTo

On the maemo platform, software is distributed using the Debian package
system. If you don't develop in Scratchbox, but directly on the device, you
need a tool to properly put together your software for distribution as such a
.deb package. To solve this, i've created PyPackager. PyPackager 3.x.x is the
same as Py2Deb, except that with the same script you can prepare package to be
uploaded to the extras maemo builder or build a debian package for maemo
directly on your device.

## Install PyPackager

Last version of pypackager is available in Maemo Extras-devel, so you can
install it with the application Manager.

## Prerequisites

Create a folder /myapp under your home folder (e.g. ”/home/user/myapp”). Then
add the following files and folders: * A subfolder /src that contains all your
source files in a folder structure which represents the way your app files
will install on the device - and with the correct permissions set (so do not
use the fat partition ~/MyDocs)! * The icon for your software package (e.g.
myapp.png, 48×48 pixels), the one that will be visible for your package in the
application manager. * And the make.py file

## programs and libraries with distutils

If you want to package a python program or library that is set up correctly
with distutils, you can use

    
    $ python setup.py bdist_dumb

to compile and generate a .tar.gz package in dist/ subdirectory. Just unpack
that package in the src/ folder and add the hildon desktop integration files
(see below) there.

## Example /src folder structure

Files needed for the Hildon desktop integration:

    
    /src/usr/share/applications/hildon/myapp.desktop
    /src/usr/share/dbus-1/services/myapp.service
    /src/usr/share/icons/hicolor/48x48/hildon/myapp.png
    /src/usr/share/icons/hicolor/scalable/hildon/myapp.png (64x64 pixel)

## myapp.desktop file

~~~~~~~~~~~~~~~~~~~~~~~~~~
    [Desktop Entry]
    Version=1.0.0
    Encoding=UTF-8
    Name=myApp
    Comment=Clock & day/night map
    Exec=/opt/myApp/myApp.py
    Icon=myapp
    X-Icon-path=/usr/share/icons
    X-Window-Icon=myapp
    Type=Application
    X-Osso-Service=net.khertan.myapp
    X-Osso-Type=application/x-executable
    StartupWMClass=myApp
~~~~~~~~~~~~~~~~~~~~~~~~~~

*Version* is version of the desktop file, NOT of the app. Keep it at 1.0.0
*Name* is Name of the app as seen in Menu
*Description* is Description of the app as seen as subtitle in Menu in Finger
mode
*Exec* is link to the app
*Icon* is Name of our icon file, without the trailing .png part
*X-Icon-path* is Path to the icon
*X-Window-Icon* is Name of our icon file, without the trailing .png part
*StartupWMClass* is only needed because if it programs use direct screen
rendering librairy like PyGame, XLib or OpenGL.

Note that you need the X-Osso-Service line only if you actually use osso
services. Including that line in the .desktop file without proper handling of
osso events in the application will result in the application being terminated
shortly after startup.

##myapp.service
~~~~~~~~~~~~~~~~~~~~~~~~~~
    [D-BUS Service]
    Name=net.khertan.myapp
    Exec=/opt/myApp/myApp.py Link to the app
~~~~~~~~~~~~~~~~~~~~~~~~~~

## Files of the application itself

~~~~~~~~~~~~~~~~~~~~~~~~~~
    /src/opt/myApp
    /src/opt/myApp/myApp.py
    /src/opt/myApp/myApp_other_class.py
    /src/opt/myApp/datas/myApp_image.png
~~~~~~~~~~~~~~~~~~~~~~~~~~

myApp.py should begin with:

~~~~~~~~~~~~~~~~~~~~~~~~~~
    #!/usr/bin/env python
~~~~~~~~~~~~~~~~~~~~~~~~~~

and be executable

## Setup the build_myapp.py code

Copy the following code to create your own build_myapp.py, then edit according
to your needs:

~~~~~~~~~~~~~~~~~~~~~~~~~~
    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    ## This program is free software; you can redistribute it and/or modify
    ## it under the terms of the GNU General Public License as published
    ## by the Free Software Foundation; version 2 only.
    ##
    ## This program is distributed in the hope that it will be useful,
    ## but WITHOUT ANY WARRANTY; without even the implied warranty of
    ## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    ## GNU General Public License for more details.
    ##
    import pypackager
    import os
     
    if __name__ == "__main__":
        try:
            os.chdir(os.path.dirname(sys.argv[0]))
        except:
            pass
     
        p=pypackager.PyPackager("khteditor")
        p.version='0.0.1'
        p.buildversion='1'
        p.display_name='KhtEditor'
        p.description="KhtEditor is a source code editor specially designed for devices running Maemo and Meego Handset."
        p.author="Benoît HERVIER"
        p.maintainer="Khertan"
        p.email="khertan@khertan.net"
        p.depends = "python2.5-qt4-gui,python2.5-qt4-core, python2.5-qt4-maemo5"
        p.suggests = "pylint"
        p.section="user/development"
        p.arch="armel"
        p.urgency="low"
        p.bugtracker='http://khertan.net/flyspray/index.php?project=7'
        p.distribution="fremantle"
        p.repository="extras-devel"
        p.icon='khteditor.png'
        p["/usr/bin"] = ["khteditor_launch.py",]
        p["/usr/share/dbus-1/services"] = ["khteditor.service",]
        p["/usr/share/pixmaps"] = ["khteditor.png",]
        p["/usr/share/applications/hildon"] = ["khteditor.desktop",]
        #Specific flags for meego
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
        for root, dirs, fs in os.walk('/home/user/MyDocs/Projects/khteditor/khteditor'):
          for f in fs:
            #print os.path.basename(root),dirs,f
            prefix = 'khteditor/'
            if os.path.basename(root) != 'khteditor':
                prefix = prefix + os.path.basename(root) + '/'
            files.append(prefix+os.path.basename(f))
        print files
     
     
        p["/usr/lib/python2.5/site-packages"] = files
     
        p.postinst = """#!/bin/sh
    chmod +x /usr/bin/khteditor_launch.py
    python -m compileall /usr/lib/python2.5/site-packages/khteditor"""
     
        p.changelog="""First Release
    """
     
    print p.generate(build_binary=False,build_src=True)
    #print p.generate(build_binary=True,build_src=True)
~~~~~~~~~~~~~~~~~~~~~~~~~~

## Run your make.py code

Open “X Terminal” on your device and change directory into your folder (e.g.
“cd /home/user/myapp”). Then run your code using “python2.5 make.py” in Xterm.
PyPackager will now package your files. Once this is done successfully,
depending on build option your ~/myapp folder will contain new files ready to
be uploaded to Maemo Auto Builder or ready to be upload to your own repository
  * myapp_0.5.6-1.changes (the changelog)
  * myapp_0.5.6-1.dsc (the package
description)
  * myapp_0.5.6-1.tar.gz (the packed source files)

This article is derivate from the [http://wiki.maemo.org/Py2Deb](http://wiki.maemo.org/Py2Deb) page. 