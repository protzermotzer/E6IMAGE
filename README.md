# E6IMAGE
A piece of software to provide images to you given tags on the furry image sharing website, e621.net. 
# Installation
Make sure you have a Python compiler, or preferably python3 from the python download website: https://www.python.org/downloads/

Open your terminal/cmd, type in the following commands, and wait until the modules are downloaded:
```
pip3 install pillow
pip3 install PySimpleGUI
pip3 install keyboard
```

Once complete, edit the file in your favourite code editor.

Upon opening the file there are two filepaths at the bottom of the window. The first is for downloading the image to show a preview, and the second is a directory to store the image, should you decide to save it.

To set default filepaths for these two, go to lines 30 and 31, and replace the double brackets with the respective filepaths.
```
previewfiledest = '/this/is/an/example'
savefiledest = '/this/is/another/example'
```
**Do not change the double brackets on line 91!**
**Make sure neither ends with a forward slash, this is added automatically by the code!**

If there are any issues, please do not hesitate to contact me.

~~N.B. To increase framerate of gif, use up and down to change by 1, and Rshift and RCtrl to change by 10~~
# Usage
Not too difficult, when prompted: 
- Input whatever tags you want to look up
- Input the amount of images you'd like to recieve
- Input whether you'd like the results to be SFW (`0`) or NSFW (`1`)

- When shown the images, press either `y` or `n` save the image in the specified directory, or to skip the image. These do not need to be inputted in the terminal as they are parsed immediately.


# Issues
## ~~Gifs~~ Filetypes other than Image_types (.png, .jpg, etc.)
~~- Some may have unwanted transparency glitching, due to technicalities in GIF compiling. (Photosensitive Epilepsy Warning!!!)~~
~~- Framerate is slower or faster than actual file, since there's no way to access actual framerate of image.~~
Currently files other than images will be skipped and cannot be saved.

## General
- When downloading, the visualiser's cancel button and close window button do not function properly. Please close the python window in order to end the program.

