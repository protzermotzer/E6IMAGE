#1494390
import os
from time import gmtime, strftime
import urllib.request
import sys
# try:
#     import images2gif
# except:
#     print("You do not have images2gif installed! Terminating program...")
# import images2gif

try:
    import PIL
except:
    print("You do not have PIL installed! Terminating program...")
    exit()
from PIL import Image, ImageSequence, ImageTk
import subprocess
import requests
try:
    import PySimpleGUI
except:
    print("You do not have PySimpleGUI installed! Terminating Program...")
    exit()
import PySimpleGUI as sg
import json
import time
import shutil
import tkinter
import keyboard


previewfiledest = 'preview_dest'
savefiledest = 'save_dest'

imageType = [
    ".png",
    ".jpeg",
    ".jpg"
]

badImageType = [
    '.jpg',
    '.jpeg'
]

animatedType = [
    ".gif"
]

videoType = [
    ".webm",
    ".mp4"
]

interactiveType = [
    ".swf"
]


# Get screen dimensions
root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

# Visuals for downloading
def download_progress_hook(count, blockSize, totalSize):
    sg.OneLineProgressMeter('Image Loading Now...',  count*blockSize, totalSize, 'key')
    if keyboard.is_pressed('esc'):
        return 0

# For debug
def jprint(obj):
    text = json.dumps(obj, indent = 4)
    print(text)


# Create image generation loop
repeat = 1
while repeat == 1:        

    tags = input('What tags? >')
    limit = input('How many images? (Max 230) >')
    safemode = input('Safemode? [0/1] >')
    
    # save destinations
    tempPath = previewfiledest + '/downloadedimageforesix'
    destPath = savefiledest
    
    # safemode
    if safemode == '1':
        tags += " rating:s"
    
    # Handle json requests and data
    headers = {"User-agent" : "MyProject/1.0 (By WibbleTime on e621"}
    e621String = "https://e621.net/posts.json?tags=order:random {0}&limit={1}".format(tags, limit)
    response = requests.get(e621String, headers = headers)
    response = response.json()

    # If no results
    nothing = 0
    if(len(response))== 0:
        nothing = 1
    
    # loop through results
    for x in range(len(response['posts'])):
        #set picture details from json
        imageArtist = ", ".join(response['posts'][x]['tags']['artist'])
        imageId = str(response['posts'][x]['id'])
        picPosition = str(x+1) + '/' + str(len(response['posts']))

        
        #download picture from url in json
        e621file = response['posts'][x]['file']['url']
        if e621file is None:
            continue
        
        # Is filetype displayable? i.e. not .webm or .swf
        filetype = (os.path.splitext(e621file))[-1]
        if (filetype in interactiveType) or (filetype in videoType):
            continue
        
        # Download data
        actualfile = urllib.request.urlretrieve(e621file, ((tempPath)), reporthook=download_progress_hook)
        
        # Resize image
        im = Image.open(tempPath)
        width, height = im.size
        ratio = height/width
        buffer = 0.8
        if ratio > HEIGHT/WIDTH:
            newW = round(width / height * HEIGHT*buffer)
            newH = round(height / height * HEIGHT*buffer)
        else:
            newW = round(width / width * WIDTH*buffer)
            newH = round(height / width * WIDTH*buffer)
            
        if filetype != '.gif':
            im = im.resize(((newW,newH)))
        elif filetype == '.gif':
            # Output (max) size
            size = WIDTH*buffer, HEIGHT*buffer

            # Open source
            im = Image.open(tempPath)
            
            # For .GIF: Calculate framerate + resize EACH frame
            def framerate(im):
                n = 0
                while 1:
                    try:
                        im.seek(n)
                    except EOFError:
                        return(n-1)
                    n += 1

            fR = framerate(im)
            frames = ImageSequence.Iterator(im)

            def thumbnails(frames):
                f = 0

                for frame in frames:
                    thumbnail = frame.copy()
                    thumbnail.thumbnail(size, Image.ANTIALIAS)
                    yield thumbnail
                    sg.OneLineProgressMeter('Resizing GIF...',  f, fR, 'key')
                    f += 1
            frames = thumbnails(frames)

            om = next(frames) # Handle first frame separately
            om.info = im.info # Copy sequence info
            om.save(tempPath + '.gif' , save_all=True, append_images=list(frames))
            im = Image.open(tempPath)
        
        
        # Change the filename for the preview depending on the extension
        if filetype in badImageType:
            im.save(tempPath + '.png')
        if filetype in imageType:
            im.save(tempPath + '.png')

        if filetype in imageType :
            file_extension = 'png'
        elif filetype in animatedType:
            file_extension = 'gif'
            
        root = tkinter.Toplevel()
        canvas = tkinter.Canvas(root, width = newW, height = newH)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open(f'preview_dest/downloadedimageforesix.{file_extension}'))
        canvas.create_image(0, 0, anchor = 'nw', image = img)
        root.update()
        
        key_pressed = False
        while not key_pressed:
       
            if keyboard.is_pressed('y'):
                save = 'y'
                key_pressed = True
            elif keyboard.is_pressed('n'):
                save = 'n'
                key_pressed = True
        
        root.destroy()
            
            

        if save == "y":
            if filetype == ".gif":
                shutil.copyfile(tempPath + '.gif', destPath + "/" + imageArtist + imageId + '.gif')
            elif filetype in imageType:
                shutil.copyfile(tempPath + '.png', destPath + "/" + imageArtist + imageId + '.png')

    again = 0
    message = "Search Again?"
    if nothing == 1:
        message = "No results :( \nSearch again?"
    
    search_again = input(message + ' [0/1] >')
    
    if search_again == '1':
        repeat = 1
    #again = input("Again? [Y/n] ")
    #if again != "":
    else:
        repeat = 0
