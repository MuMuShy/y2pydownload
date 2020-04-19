from pytube import YouTube
import pyglet
import tkinter as tk
import threading
from PIL import Image, ImageTk
import time
import os
from config import config
from multiprocessing.pool import ThreadPool
from multiprocessing import Process, Queue
import pygame
from pytube import Playlist
import threadpool
from moviepy.editor import *
from pathlib import Path
yt = YouTube('https://www.youtube.com/watch?v=Z9os9Oq3bJo')
music_list = []
path =  os.getcwd()
is_pause = False
next_song_index = 0
is_Pause = False
music_name =""
base_volume = 0.5

def draw_window():
    def get_music_list():
        # 預設為 /musics資料夾
        music_path = path + config.path
        print(music_path)
        files = os.listdir(music_path)
        for file in files:
            if file.endswith('.mp3'):
                music_list.append(file)
                print(file)
    #get_music_list()
    def convert_music():
        print('converting....')
        music_path = path + config.path
        files = os.listdir(music_path)
        for file in files:
            if file.endswith('.mp4'):
                filename = file.split('.mp4')
                print(filename)
                video = VideoFileClip(music_path + '/' + file)
                video.audio.write_audiofile(music_path + '/' + filename[0] + '.mp3')
                video.close()
                os.remove(music_path + '/' + file)
        download_remain.set("轉檔完成 加入撥放列表")
        update_music_list()


    def call_convert_music_thread():
        t_convert = threading.Thread(target=convert_music())
        t_convert.start()


    def show_progress_bar(stream: yt, chunk: bytes, bytes_remaining: int):
        print("剩餘(bytes):", bytes_remaining)
    music_path = path + config.path
    musics = []

    pygame.mixer.init()
    MUSIC_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(MUSIC_END)
    pygame.mixer.music.set_volume(base_volume)


    # 建立主視窗和 Frame（把元件變成群組的容器）
    window = tk.Tk()
    window.title("Y2Box")
    window.geometry('500x400')
    window.config(bg="#FF8888")
    top_frame = tk.Frame(window, background="#FF8888")

    #
    download_remain = tk.StringVar()
    now_playing_music_name = tk.StringVar()
    # 將元件分為 top/bottom 兩群並加入主視窗
    top_frame.pack()

    bottom_frame = tk.Frame(window, background="#FF8888")
    bottom_frame.pack(side=tk.BOTTOM)


    def play_sound_pygame():
        global next_song_index
        global is_Pause
        global music_name
        music_name = list_box.get(list_box.curselection())
        pygame.mixer.music.load(music_path + '/' + music_name)
        next_song_index = music_list.index(music_name) + 1

        pygame.mixer.music.play()
        now_playing_music_name.set("目前播放:" + music_name)
        window.update()


    def check_event():
        global next_song_index
        global music_name
        for event in pygame.event.get():
            if event.type == MUSIC_END:
                print('播放完畢 下一首')
                print('歌單長度:'+str(len(music_list)))
                next_song_index = music_list.index(music_name)+1
                if next_song_index >= len(music_list):
                    print("next son index > music list get %:",next_song_index)
                    next_song_index = next_song_index % len(music_list)
                list_box.selection_clear(music_list.index(music_name))
                list_box.select_set(next_song_index)
                print('next song index:' + str(next_song_index))
                pygame.mixer.music.stop()
                time.sleep(0.5)
                print('讀取:'+music_list[next_song_index])
                pygame.mixer.music.load(music_path+'/'+music_list[next_song_index])
                pygame.mixer.music.play()
                now_playing_music_name.set("目前播放:" + music_list[next_song_index])
                music_name = music_list[next_song_index]
        window.after(100,check_event)


    def pause():
        global is_Pause
        print('click pause')
        if pygame.mixer.music.get_busy():
            if is_Pause:
                pygame.mixer.music.unpause()
                is_Pause = False
            else:
                is_Pause = True
                pygame.mixer.music.pause()


    def add_volume():
        global  base_volume
        base_volume += 0.1
        if base_volume >=1.0:
            base_volume = 1.0
        pygame.mixer.music.set_volume(base_volume)


    def dec_volume():
        global base_volume
        base_volume -= 0.1
        if base_volume <=0:
            base_volume = 0
        pygame.mixer.music.set_volume(base_volume)

    def update_music_list():
        # 預設為 /musics資料夾
        music_path = path + config.path
        files = os.listdir(music_path)
        print(files)
        index = 0
        list_box.delete(0,list_box.size())
        music_list.clear()
        for filename in files:
            if filename.endswith('.mp3'):
                list_box.insert(index,filename)
                index+=1
                musics.append(music_path+'/'+filename)
                music_list.append(filename)
        window.update()

    #call back

    def convert_to_aac(stream: yt, file_path: str):
        download_remain.set("下載完成,轉檔中...")
        call_convert_music_thread()
        update_music_list()
        print("下載完畢")

    def show_progress_bar(stream: yt, chunk: bytes, bytes_remaining: int):
        print("剩餘(bytes):", bytes_remaining)
        download_remain.set("剩餘(bytes):"+str(bytes_remaining))
        window.update()


    # 建立事件處理函式（event handler），透過元件 command 參數存取
    def download():
        download_remain.set("下載中....")
        url = input_field.get()
        yt = YouTube(url)
        yt.register_on_progress_callback(show_progress_bar)
        yt.register_on_complete_callback(convert_to_aac)
        yt.streams.get_highest_resolution().download(output_path="musics")
        print(url)


    def download_list():
        url = input_field.get()
        play_list = Playlist(url)
        play_list.download_all()

    def start_download():
        my_thread = threading.Thread(target=download())
        my_thread.start()


    # 以下為 top 群組
    top_input_Label = tk.Label(top_frame, text="Youtube影片網址:", fg="white", background="#FF8888")
    top_input_Label.pack(side=tk.LEFT)

    input_field = tk.Entry(top_frame, width=50)
    input_field.pack()

    #list box
    list_box = tk.Listbox(window,width=100,height=400,bg="#99FFFF")
    list_box.insert("123")
    list_box.insert('456')
    list_box.pack()
    update_music_list()


    # down
    play_button_open = Image.open(path+'/img/play_btn.png')
    pause_button_open = Image.open(path+'/img/pause_btn.png')
    pause_button_img = ImageTk.PhotoImage(pause_button_open)
    play_button_img = ImageTk.PhotoImage(play_button_open)
    play_button = tk.Button(bottom_frame, image=play_button_img, command = play_sound_pygame, width = 50, height = 18, bg="#FFCCCC")
    play_button.pack(side = 'left')
    pause_button = tk.Button(bottom_frame,text="pause!",image=pause_button_img,width = 50, height = 18, command=pause, bg="#FFCCCC")
    pause_button.pack(side = 'left')
    add_value_button = tk.Button(bottom_frame, text="Volumn+",width = 10, bg="#FFCCCC", command = add_volume)
    add_value_button.pack(side="left")
    dec_value_button = tk.Button(bottom_frame, text="Volumn-", width=10, bg="#FFCCCC",command = dec_volume)
    dec_value_button.pack(side="left")

    playing_info_label = tk.Label(bottom_frame,textvariable = now_playing_music_name,font=('Arial', 8), width=80, height=2,fg = "green", background="#FF8888")
    playing_info_label.pack()


    download_process_label = tk.Label(bottom_frame,textvariable=download_remain, font=('Arial', 8), width=80, height=2,fg = "green", background="#FF8888")
    download_process_label.pack()


    download_button = tk.Button(bottom_frame, text="下載!",width=15,height=2,command=start_download)
    download_button.pack()



    # 以下為 bottom 群組
    # bottom_button 綁定 echo_hello 事件處理，點擊該按鈕會印出 hello world :)
    #bottom_button = tk.Button(bottom_frame, text='Black', fg='black', command=echo_hello)
    # 讓系統自動擺放元件（靠下方）
    #bottom_button.pack(side=tk.BOTTOM)

    # 運行主程式
    window.after(250)
    check_event()
    window.mainloop()

if __name__ == '__main__':
    draw_window()