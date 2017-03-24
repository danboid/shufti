# shufti

## The persistent image viewer

### By Dan MacDonald, 2017

**shufti** is a lightweight, PyQt-based image viewer. It automatically saves and restores the zoom level, rotation, window size, desktop location and the scrollbar positions (ie viewing area) for every image it loads, on a per-image/location basis. It supports viewing .jpg, .png, .gif, .tif and .bmp files, amongst others.

shufti has no GUI to consume precious image viewing space. It aims to be efficient and lightweight - it will never edit images, play videos or do you a brew. Its complete, uncompressed source code is approx. 12KB.

shufti is free and open source software licensed under the latest GNU Affero GPL license and should run on any platform that can run PyQt - that includes GNU/Linux, *BSD, macOS and Windows.

## INSTALLATION

On Debian and Ubuntu-based distros:

```
 $ sudo apt install git python-pyqt5
 $ git clone https://github.com/danboid/shufti.git
 $ chmod +x ./shufti/shufti.py
 $ sudo cp ./shufti/shufti.py /usr/local/bin/shufti
```

## USAGE

Run:

```
 $ shufti /full/path/to/image/file
```

To view the file. The view settings are saved when you close a window or choose to view the next/previous image. These settings are restored next time you open or browse to the file.

You will need to right-click on your image files in your file manager and use the **Open with command** option (which is usually under the **Open with** tab under the right-click **Properties** menu of the image file), when selected under your desktop's file manager to set shufti as the command to use to open image files.

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

Note that the easiest way to resize windows under most Linux/BSD desktops is to hold the ALT key then right-click and drag near the window edge you wish to resize. This saves the user from having to precisely position the cursor over a window edge to resize it.

## LIMITATIONS

Due to its nature, shufti will only be of use if you maintain the same display configuration ie screen / desktop config and resolution(s).

Whilst shufti allows you to view images fullscreen, it is intended for the viewing of images in non-fullscreen windows. If you use its directory browsing ability, you should exit fullscreen mode before moving to the next image.

shufti isn't able to dynamically resize its window when browsing images within a directory if its window has been maximised vertically or horizontally by the window manager. This is the case for both KDE (Kwin) and MATE (Marco) at least. If you wish to maximise a window horizontally or vertically, do it using shufti's maximise features or do it manually instead of using your window manager / desktop to do it.
