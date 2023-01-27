from pytube import YouTube
import os

youtube = YouTube('https://www.youtube.com/watch?v=r9ARwGqFyA8')

video = youtube.streams.filter(res="1080p").first().download()
os.rename(video,"video.mp4")

audio = youtube.streams.filter(subtype='mp4', only_audio=True).order_by('bitrate').desc().first().download()
os.rename(audio,"audio.mp4")

os.system("ffmpeg -i audio.mp4 -i video.mp4 -async 1 -c copy YTvideo.mp4")
