import tkinter as tk
import tkinter.scrolledtext as tkst
from pytube import YouTube
import os
import threading
import time

previousprogress = 0

def on_progress(stream, chunk, bytes_remaining):
    global previousprogress
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    liveprogress = int(bytes_downloaded / total_size * 100)
    if liveprogress > previousprogress:
        previousprogress = liveprogress
        write_to_console(str(liveprogress) + '%')


def download_video():
    youtube = YouTube(url_var.get())
    youtube.register_on_progress_callback(on_progress)
    write_to_console('Downloading video...')
    video = youtube.streams.filter(res=res_var.get()).first().download()
    write_to_console('Rename video...')
    os.rename(video, 'video.mp4')
    write_to_console('Download audio...')
    audio = youtube.streams.filter(subtype='mp4',
                                   only_audio=True).order_by('bitrate'
            ).desc().first().download()
    write_to_console('Rename audio...')
    os.rename(audio, 'audio.mp4')
    write_to_console('Join video and audio with FFMPEG...')
    os.system('ffmpeg -i audio.mp4 -i video.mp4 -async 1 -c copy YouTubeVideo.mp4'
              )

    write_to_console('Renaming video...')
    filename = 'YouTubeVideo.mp4'
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    new_filename = '{}_{}'.format(timestamp, filename)
    os.rename(filename, new_filename)

    write_to_console('Removal of temp files...')
    os.remove('audio.mp4')
    os.remove('video.mp4')
    write_to_console('Finished!')


def write_to_console(text):
    console.config(state='normal')
    console.insert('end', text + '\n')
    console.config(state='disabled')


root = tk.Tk()
root.title('YouTube Downloader')

url_var = tk.StringVar()
url_entry = tk.Entry(root, textvariable=url_var, width=43)
url_entry.pack()

res_var = tk.StringVar()
res_var.set('1080p')
res_dropdown = tk.OptionMenu(
    root,
    res_var,
    '4320p',
    '2160p',
    '1440p',
    '1080p',
    '720p',
    '480p',
    '360p',
    )
res_dropdown.pack()

download_button = tk.Button(root, text='Download', command=lambda : \
                            threading.Thread(target=download_video).start())
download_button.pack()

console = tkst.ScrolledText(root, state='disabled', height=10, width=50)
console.pack()

root.geometry('600x400')
root.mainloop()
