# shufti

## A WIP, PyQt5 persistent image viewer for Gahnooah slash Leenoox

shufti is currently not usable and has zero features, other than a rough design.

## THE PLAN

I'm pretty sure I have tried every image viewer available for Linux and thats quite a lot but none of them do what I want so I have been forced to create my own and there is nothing else it could possibly be called other than shufti, surely.

The main design goals of shufti are:

* Automatically and non-destructively save and restore at least (by v1.0) the zoom and pan settings and optionally window size and position of the shufti windows over multiple virtual desktops and displays. Hopefully this can be made to work regardless of the users choice of desktop and/or window manager but I'm only concerned with MATE initially as that's what I use. All these settings will be stored in a local database on a per image, absolute path basis. Every time shufti opens an image, it will first check its DB to see if this file has been accessed before. If not, it will open it on desktop/display 1 in 1:1 zoom and centred, if the image is smaller than the main display. This complete, automated process of saving and restoring image windows is the central feature and reason for the programs creation.

* No gui, or no icons or menus taking up precious screen space in the viewing window. shufti will support mouse, touch and keyboard input for panning, zooming and 'shufting' through directories but only through mouse/touch gestures and keyboard shortcuts.

* Just a viewer, it will never write to or modify any image files. 

* Free and open source.

Due to its very nature, shufti will only be of use if you maintain the same display configuration ie screen / desktop config and resolution(s).

This is my first attempt at writing a PyQt app so buyer beware!

