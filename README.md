# shufti

## The persistent image viewer

### By Dan MacDonald

**shufti** is a lightweight, PyQt-based image viewer. It automatically saves and restores the zoom level, rotation, window size, desktop location and the scrollbar positions (ie viewing area) for every image it loads, on a per-image/location basis. It supports viewing .jpg, .png, .gif, .tif and .bmp files, amongst others.

**shufti** has no GUI to consume precious image viewing space. It aims to be efficient and lightweight hence it will never edit images, play videos or do you a brew. Every images view settings are saved to a local SQlite database on your computer - shufti never modifies any image files.

**shufti** is free and open source software licensed under the latest GNU Affero GPL license and should run on any platform that can run PyQt - that includes GNU/Linux, *BSD, macOS and Windows.

## INSTALLATION

Windows users can download an installer from the Releases section.

[HOWTO Install the shufti image viewer under Windows 10](https://www.youtube.com/watch?v=6Bny-1YGUHE) 

Arch users can install shufti with an AUR helper like so:

```
 $ packer -S shufti
```

For Debian and Ubuntu-based distros, run these commands to manually install shufti from Github:

```
 $ sudo apt install git python-pyqt5 python-pyqt5.qtsql
 $ git clone https://github.com/danboid/shufti.git
 $ sudo cp ./shufti/shufti.py /usr/local/bin/shufti
```

FreeBSD and TrueOS users may have to modify shufti's hashbang before it can be run from your file manager because FreeBSD doesn't create a default symlink from python to python2 (which is still the default for FreeBSD/TrueOS at the time of writing) unlike most Linux distros. shufti requires PyQt5 but it can be run with python 2 or 3. Instead of adjusting the hashbang, FreeBSD and TrueOS users can create the missing symlink like so:

```
 # ln -s /usr/local/bin/python2 /usr/local/bin/python
```

## USAGE

After installing shufti you need to right-click on an image file in your file manager (eg right click on a .jpg file under Windows Explorer, Dolphin, Thunar or whatever) and use the **Open with command** option (which is usually under the **Open with** tab under the right-click **Properties** menu of the image file), when selected under your desktop's file manager to set shufti as the command to use to open image files. You have to do this for every different type of image file you wish to open with shufti. 

You can also run shufti from the command line. This is the only way to use it under macOS currently. Under a UNIX-like OS, you'd run:

```
 $ shufti /full/path/to/image/file
```

If you're running shufti from the Windows command prompt using the .exe, the command would look more like:

```
 > shufti c:\full\path\to\image\file
```

To view a file. Shufti requires you use the full path to the image you wish to open first.

The view settings are saved when you close a window or choose to view the next/previous image. These settings are restored next time you open or browse to the file.



## CONTROLS

**+**, **-**, **e**, **d** and the **mouse wheel** zoom the view.

**F11** & **double click** toggle full screen view.

**r** rotates the image 90 degrees counter-clockwise.

**s** spins the image 90 degrees clockwise.

**BACKSPACE** view previous image in directory.

**SPACE** view next image within directory.

**z** horiZontally maximises the window.

**v** vertically maximises the window.

**f** fits the image into the window.

**right click** show context menu.

**1** resets the zoom.

**q** quits.

Note that the easiest way to resize windows under most Linux/BSD desktops is to hold the ALT key then right-click and drag near the window edge you wish to resize. This saves the user from having to precisely position the cursor over a window edge to resize it.

## LIMITATIONS

shufti requires that you maintain the same display configuration to restore image windows correctly.

Whilst shufti allows you to view images fullscreen, it is really intended for the viewing of images in non-fullscreen windows. If you use its directory browsing ability, you should exit fullscreen mode before moving to the next image.

shufti isn't able to dynamically resize its window when browsing images within a directory if its window has been maximised vertically or horizontally by the window manager. This is the case for both KDE (Kwin) and MATE (Marco), at least. If you wish to maximise a window horizontally or vertically, do so using shufti's maximise features or do it manually instead of using your window manager or desktop environment to do it.

If you use multiple displays and one is higher resolution than the others, shufti's horizontal and vertical maximise features only work properly when the largest display is configured as the primary desktop.

## DONATIONS

If you find shufti useful, please make a donation via PayPal. 

Thanks!

**allcoms at gmail dot com**
