from tkinter import *
from tkinter.ttk import Progressbar
from threading import Thread
import os
import pytube
from tkinter import messagebox
import subprocess

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


def add_audio_to_video(video_file, audio_file, output_file, progressbar):
    try:
        # Use ffmpeg to add audio to the video without re-encoding the video
        subprocess.run(['ffmpeg', '-i', video_file, '-i', audio_file, '-c', 'copy', '-map', '0:v', '-map', '1:a', output_file], check=True)

        # Cleanup - delete the temporary audio file
        os.remove(audio_file)
        os.remove(video_file)

        progressbar.stop()
        # Show success message
        messagebox.showinfo("Готово", "Загрузка завершена успешно.")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Ошибка при добавлении аудио к видео: {str(e)}")

    finally:
        # Stop the progress bar after ffmpeg is done
        progressbar.stop()


def download():
    try:
        yt_link = link1.get()
        video_file, audio_file = download_video_and_audio(yt_link)

        if video_file and audio_file:
            # Use the name of the video file as the output file name
            output_file = os.path.splitext(video_file)[0] + "_downloaded.mp4"

            # Run the merging process in a new thread
            Thread(target=add_audio_to_video, args=(video_file, audio_file, output_file, progressbar)).start()

    except Exception as e:
        Result = f"Ошибка: {str(e)}"
        messagebox.showerror("Ошибка", Result)


def download_button_clicked():
    progressbar.place(x=160, y=140, width=300)
    progressbar.start()
    # Download the file in the current thread.
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
