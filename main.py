from tkinter import *
from tkinter.ttk import Progressbar
from threading import Thread

import pytube
from tkinter import messagebox

root = Tk()
root.geometry("500x250")
root.resizable(False, False)
root.title("Код")
root.config(bg='#D3D3D3')


def download():
    try:
        yt_link = link1.get()
        youtube_link = pytube.YouTube(yt_link)
        # video = youtube_link.streams.get_highest_resolution()
        video = youtube_link.streams.filter(adaptive=True).filter(mime_type='video/webm').first()
        video.download()
        progressbar.stop()
        Result = "Загрузка завершена"
        messagebox.showinfo("Готово", Result)
    except:
        Result = "Ссылка не работает"
        messagebox.showerror("Ошибка", Result)


def download_button_clicked():
    progressbar.place(x=150, y=140, width=300)
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
