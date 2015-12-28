from pytube import YouTube
from pprint import pprint
from subprocess import call
import sys
import os

#check for arguments
if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], " input_list.txt"
    sys.exit(1)

#define paths
dw_path = "./videos/"
mp3_path = "./mp3/"

#create paths if they don't exist
if not os.path.exists(dw_path):
        os.makedirs(dw_path)
if not os.path.exists(mp3_path):
        os.makedirs(mp3_path)

lst_file = open(str(sys.argv[1]), "r")

#read all lines of the given file
for line in lst_file:
    tmp = line.split(";")

    #first element is the URL
    url = tmp[0].strip()

    #second element is the filename
    name = tmp[1].strip()
    yt = YouTube(url)
    yt.set_filename(name)

    #get all available video formats
    available = yt.get_videos()
    quali = 0

    #try to get a 720p version, else 480p, else 360p
    for x in available:
        if "720p" in str(x):
            quali = 720
            break
        if "480p" in str(x):
            if quali < 480:
                quali = 480
        if "360p" in str(x):
            if quali < 360:
                quali = 360

    print str(quali) + "p", "selected for:", name, " URL:", url

    #get the mp4 version with the highest quality
    video = yt.get('mp4', str(quali)+"p")
    pprint(video)
    video.download(dw_path)

    #convert the video to mp3 with ffmpeg
    call(["ffmpeg", "-i", dw_path + name + ".mp4", mp3_path + name + ".mp3"])

print "\nFinish!\nDownloaded all videos and converted them to mp3."

