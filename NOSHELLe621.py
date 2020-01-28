#1494390
import os
from time import gmtime, strftime
import urllib.request
import sys
try:
    import images2gif
except:
    print("You do not have images2gif installed! Terminating program...")
import images2gif
try:
    import PIL
except:
    print("You do not have PIL installed! Terminating program...")
    exit()
from PIL import Image, ImageSequence
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

def download_progress_hook(count, blockSize, totalSize):
    sg.OneLineProgressMeter('Image Loading Now...',  count*blockSize, totalSize, 'key')
  
def jprint(obj):
    text = json.dumps(obj, indent = 4)
    print(text)



repeat = 1
while repeat == 1:        
    sg.theme("Reddit")
    layout = [ [sg.Text("Tags"), sg.InputText(key='tags')],
               [sg.Text("Amount of posts"), sg.InputText(key='limit')],
               [sg.Checkbox("Safemode", key='safe')],
               [sg.Submit(), sg.Cancel()],
               [sg.Text("_" * 80)],
               [sg.Text('Select temporary storage for display', font='ALL 7', auto_size_text=False, justification='right'), sg.InputText('/home/pi/Desktop/temp/downloadedimageforesix'), sg.FolderBrowse()],      
    [sg.Text('Select permanant storage for image', font='ALL 7', auto_size_text=False, justification='right'), sg.InputText('/home/pi/Desktop/savedfiles'), sg.FolderBrowse()],     
    
    ]
    
    window = sg.Window("e621 Image Gen", layout)
    event, values = window.read()

    window.close()
    
    tempPath = values[0]
    destPath = values[1]
    
    tags = values['tags']
    if values['safe'] == True:
        tags += " rating:s"
    
    limit = values['limit']
    h = {"User-agent" : "MyProject/1.0 (By WibbleTime on e621"}
    e621String = "https://e621.net/post/index.json?tags=order:random {0}&limit={1}".format(tags, limit)
    response = requests.get(e621String, headers = h)
    response = response.json()


    nothing = 0
    if(len(response))== 0:
        nothing = 1
    
    for x in range(len(response)):
        #set picture details
        imageArtist = ", ".join(response[x]['artist'])
        imageId = str(response[x]['id'])
        picPosition = str(x+1) + '/' + str(len(response))

        
        #download picture
        e621file = response[x]['file_url']
        filetype = (os.path.splitext(e621file))[-1]
        if (filetype in interactiveType) or (filetype in videoType):
            continue
        actualfile = urllib.request.urlretrieve(e621file, ((tempPath)), reporthook=download_progress_hook)

        im = Image.open(tempPath)
        width, height = im.size
        ratio = height/width
        if ratio > 0.5:
            newW = round(width / height * 600)
            newH = round(height / height * 600)
        else:
            newW = round(width / width * 300)
            newH = round(height / width * 300)
        
        if filetype != '.gif':
            im = im.resize(((newW,newH)))
        elif filetype == '.gif':
            # Output (max) size
            size = 640, 480

            # Open source
            im = Image.open(tempPath)

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

        if filetype in badImageType:
            im.save(tempPath + '.png')
        if filetype in imageType:
            im.save(tempPath + '.png')

        if filetype in imageType : 
            layout = [  [sg.Text(imageArtist + " " + imageId, font='ANY 15')],
                    [sg.Image(tempPath + '.png', key='_IMAGE_', tooltip='I am ashamed of you')],
                    [sg.Text(picPosition, font='ANY 6')],
                   [sg.Text("Press Y to save or N to next")]
                 ]
            window = sg.Window('My new window', return_keyboard_events=True, use_default_focus=False).Layout(layout)
            event, values = window.Read()
            if event == "y:29":
                save = 'y'
                window.close()
            elif event == "n:57":
                save = 'n'
                window.close() 
            elif event == 'None':
                window.close()
                sys.exit()
        elif filetype in animatedType:
            layout = [  [sg.Text(imageArtist + " " + imageId, font='ANY 15')],
                    [sg.Image(tempPath + '.gif', key='_IMAGE_', tooltip='I am ashamed of you')],
                    [sg.Text(picPosition)],
                   [sg.Text("Press Y to save or N to next")]
                 ]
            
            
            window = sg.Window('My new window', return_keyboard_events=True, use_default_focus=False).Layout(layout)
            
            exit = 0
            count = 0
            oldTime = strftime("%M%S", gmtime())
            print(oldTime)
            while exit == 0:
                event, values = window.read(timeout=25)
                window.Element('_IMAGE_').UpdateAnimation(tempPath + '.gif')
                if event == "y:29":
                    save = 'y'
                    window.close()
                    exit=1
                elif event == "n:57":
                    save = 'n'
                    window.close()
                    exit=1
                elif event == 'None':
                    window.close()
                    sys.exit()
                if count == 0:
                    newTime = strftime("%M%S", gmtime())
                    print(newTime)
                    loadTime = int(newTime) - int(oldTime)
            
                    print(loadTime)
                    count = 1
        if save == "y":
            #saveFile = urllib.request.urlretrieve(e621file, (('/home/pi/Desktop/savedfiles/' + imageArtist + imageId)), reporthook=download_progress_hook)
            if filetype == ".gif":
                shutil.copyfile(tempPath + '.gif', destPath + "/" + imageArtist + imageId + '.gif')
            elif filetype in imageType:
                shutil.copyfile(tempPath + '.png', destPath + "/" + imageArtist + imageId + '.png')

        #print(Style.RESET_ALL)
    again = 0
    message = "Search Again?"
    if nothing == 1:
        message = "No results :( \nSearch again?"
    againLayout = [ [sg.Text(message)],
                    [sg.Yes(focus=True), sg.No()]
    ]
    window = sg.Window("e621 Image Gen", againLayout, return_keyboard_events=True)
    events, values = window.read()
    if events == "y:29" or events == 'Return:36':
        repeat = 1
    #again = input("Again? [Y/n] ")
    #if again != "":
    else:
        repeat = 0
    window.close()

    