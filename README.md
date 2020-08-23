# E6IMAGE
A piece of software to provide images to you given tags on the furry image sharing website, e621.net. 
# Installation
Make sure you have a Python compiler, or preferably python3 from the python download website: https://www.python.org/downloads/

Open your terminal/cmd, type in the following commands, and wait until the modules are downloaded:
```
pip3 install pillow
pip3 install PySimpleGUI
pip3 install images2gif
```

Once complete, download the ESIXimage.py file, and type in it's file destination here:
```
python3 /file/path/of/where/you/saved/the/file/to/ESIXimage.py
```

Upon running the file there are two filepaths at the bottom of the window. The first is for downloading the image to show a preview, and the second is a directory to store the image, should you decide to save it.

To set default filepaths for these two, go to lines 30 and 31, and replace the double brackets with the respective filepaths.
```
previewfiledest = '/this/is/an/example'
savefiledest = '/this/is/another/example'
```
**Do not change the double brackets on line 91!**
**Make sure neither ends with a forward slash, this is added automatically by the code!**

If there are any issues, please do not hesitate to contact me.

~~N.B. To increase framerate of gif, use up and down to change by 1, and Rshift and RCtrl to change by 10~~

# Issues
## Gifs
- Some may have unwanted transparency glitching, due to technicalities in GIF compiling. (Photosensitive Epilepsy Warning!!!)
- Framerate is slower or faster than actual file, since there's no way to access actual framerate of image.

## General
- The Cancel button while downloading is not functional, use the X in image preview, or in Tag Menu.
- If the Tag Menu keeps refreshing when you try to submit, you haven't changed the file destinations. Refer to setting
defaults above.


