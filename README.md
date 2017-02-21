# shufti

## The persistent image viewer

## By Dan MacDonald, 2017

**shufti** is a simple PyQt5, SQLite database-powered image viewer. It's main feature, and the reason it was created, is that it automatically saves and restores the zoom level, window size, desktop location and the scrollbar positions (ie viewing area) on a per-image basis, for every image it loads. It supports viewing .jpg, .png, .gif and .bmp files, amongst others.

shufti has no UI and that is by design. It aims to be efficient and lightweight, it will never edit images, play videos or do you a brew. It's complete and uncompressed source code is less that 7 Kilobytes and less than 200 lines of code.

Due to its very nature, shufti will only be of use if you maintain the same display configuration ie screen / desktop config and resolution(s).

shufti is free and open source software and should run on any platform that can run PyQt - that includes GNU/Linux, *BSD , macOS and Windows.

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

To view the file. The view settings are saved when you close the window and restored next time you open that file in that directory.

You will most likely want to right-click on your image files in your file manager and use the *Open with command* type option which is usually under the **Open with** tab under the right-click **Properties** menu of the image file, when selected under you file manager. Just enter **shufti** into the **Open with command** dialogue, **Apply**, **OK.**
