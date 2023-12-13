from tkinter import *
from tkinter.ttk import Progressbar
from threading import Thread
import os
import pytube
from tkinter import messagebox
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import ffmpeg

root = Tk()
root.geometry("500x250")
root.resizable(False, False)
root.title("Код")
root.config(bg='#D3D3D3')


def download_video_and_audio(url, output_path="."):
    try:
        youtube_link = pytube.YouTube(url)

        # Download video
        video_stream = youtube_link.streams.filter(adaptive=True).filter(mime_type='video/webm').first()
        video_stream.download(output_path)

        # Download audio
        audio_stream = youtube_link.streams.filter(only_audio=True).first()
        audio_stream.download(output_path)

        return video_stream.default_filename, audio_stream.default_filename

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при загрузке видео и аудио: {str(e)}")
        return None, None


def merge_video_and_audio(video_file, audio_file, output_file):
    try:
        video = VideoFileClip(video_file)
        audio = AudioSegment.from_file(audio_file, format="webm")

        # Set the audio of the video file to the downloaded audio
        video = video.set_audio(audio)

        # Write the merged video with audio to a file
        video.write_videofile(output_file, codec="libx264", audio_codec="aac")

        # Cleanup - delete the individual video and audio files
        video.close()
        audio.close()

        # Delete the original video and audio files
        os.remove(video_file)
        os.remove(audio_file)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при совмещении видео и аудио: {str(e)}")


def download():
    try:
        yt_link = link1.get()
        video_file, audio_file = download_video_and_audio(yt_link)

        if video_file and audio_file:
            progressbar.stop()
            Result = "Загрузка завершена"
            messagebox.showinfo("Готово", Result)

            output_file = "merged_video.mp4"
            merge_video_and_audio(video_file, audio_file, output_file)
    except Exception as e:
        Result = f"Ошибка: {str(e)}"
        messagebox.showerror("Ошибка", Result)


def download_button_clicked():
    progressbar.place(x=160, y=140, width=300)
    progressbar.start()
    # Download the file in a new thread.
    Thread(target=download).start()


def reset():
    link1.set("")


def _exit():
    root.destroy()


lb = Label(root, text="---Загрузка видео с YouTube---", font='Arial,15,bold', bg='#D3D3D3')
lb.pack(pady=15)

progressbar = Progressbar(mode="indeterminate")

lb1 = Label(root, text="Ссылка на видео :", font='Arial,15,bold', bg='#D3D3D3')
lb1.place(x=10, y=80)

link1 = StringVar()
En1 = Entry(root, textvariable=link1, font='Arial,15,bold')
En1.place(x=220, y=80)

btn1 = Button(root, text="Скачать", font='Arial,10,bold', bd=4, command=download_button_clicked)
btn1.place(x=30, y=130)

btn2 = Button(root, text="Очистить", font='Arial,10,bold', bd=4, command=reset)
btn2.place(x=150, y=190)

btn3 = Button(root, text=" Выход ", font='Arial,10,bold', bd=4, command=_exit)
btn3.place(x=260, y=190)

root.mainloop()
