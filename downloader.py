from pytube import YouTube
import os

youtube = YouTube('https://www.youtube.com/watch?v=r9ARwGqFyA8')

print("Downloading video stream")
video = youtube.streams.filter(res="1080p").first().download()

print("Renaming video")
os.rename(video,"video.mp4")

print("Downloading audio stream")
audio = youtube.streams.filter(subtype='mp4', only_audio=True).order_by('bitrate').desc().first().download()

print("Renaming audio")
os.rename(audio,"audio.mp4")

print("Merging video and audio")
os.system("ffmpeg -i audio.mp4 -i video.mp4 -async 1 -c copy YTvideo.mp4")

print("Done")
input("Press enter to exit;")
