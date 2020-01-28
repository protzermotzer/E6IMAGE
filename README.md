# E6IMAGE
A piece of software to provide images to you given tags on the furry image sharing website, e621.net. 
# Installation
Make sure you have a Python compiler, or preferably python3 from the python download website: https://www.python.org/downloads/

Open your terminal/cmd, type in the following commands, and wait until the modules are downloaded:
```
pip3 install PIL
pip3 install PySimpleGUI
pip3 install images2gif
```

Once complete, type in:
```
python3 /file/path/of/where/you/saved/the/file/to/ESIXimage.py
```

The two filepaths at the bottom of the window are for downloading the image to display a resized version, and a directory to store the image, should you decide to save it.

To set the default filepaths, go to lines 30 and 31, and replace the double brackets with the respective filepaths.
```
previewfiledest = '/this/is/an/example'
savefiledest = '/this/is/another/example'
```
**Make sure neither ends with a forward slash! This is added automatically by the code!**

If there are any issues, please do not hesitate to contact me.






