from pytube import YouTube
import pyglet
import tkinter as tk
import time
yt = YouTube('https://www.youtube.com/watch?v=Z9os9Oq3bJo')


def convert_to_aac(stream: yt, file_path: str):
    return test()


def show_progress_bar(stream: yt, chunk: bytes, bytes_remaining: int):
    print("剩餘(bytes):",bytes_remaining)


def test():
    print("download complete")


def play_audio():
    vidPath = 'musics/test.mp4'
    window = pyglet.window.Window(width=640,height=640,caption ="播放器")
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad = pyglet.media.load(vidPath)

    player.queue(MediaLoad)
    player.play()

    @window.event
    def on_draw():
        if player.source and player.source.video_format:
            player.get_texture().blit(0, 100)
    def on_close():
        player.delete()
    pyglet.app.run()


def draw_window():
    # 建立主視窗和 Frame（把元件變成群組的容器）
    window = tk.Tk()
    window.title("Yotube 音樂下載器")
    window.geometry('500x200')
    top_frame = tk.Frame(window)

    download_remain = tk.StringVar()

    # 將元件分為 top/bottom 兩群並加入主視窗
    top_frame.pack()
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(side=tk.BOTTOM)

    #call back

    def convert_to_aac(stream: yt, file_path: str):
        return play_audio()

    def show_progress_bar(stream: yt, chunk: bytes, bytes_remaining: int):
        print("剩餘(bytes):", bytes_remaining)
        download_remain.set(str(bytes_remaining))

    # 建立事件處理函式（event handler），透過元件 command 參數存取
    def download():
        download_remain.set("下載中....")
        url = input_field.get()
        yt = YouTube(url)
        yt.register_on_progress_callback(show_progress_bar)
        yt.register_on_complete_callback(convert_to_aac)
        yt.streams.get_highest_resolution().download(filename="test", output_path="musics")
        print(url)


    def search():
        keyword= input_field.get()
        keyword = "'"+keyword+"'"
        url="https://www.youtube.com/results?search_query="+keyword
        print(url)
        yt = YouTube(url)
        print(yt.streams)

    # 以下為 top 群組
    top_input_Label = tk.Label(top_frame, text="Youtube影片網址:")
    top_input_Label.pack(side=tk.LEFT)

    input_field = tk.Entry(top_frame, width=50)
    input_field.pack()


    download_process_label = tk.Label(bottom_frame,textvariable=download_remain, font=('Arial', 12), width=15, height=2)
    download_process_label.pack()

    search_button = tk.Button(bottom_frame, text="查詢", width=15, height=2, command=search)
    search_button.pack()

    download_button = tk.Button(bottom_frame, text="下載!",width=15,height=2,command=download)
    download_button.pack()



    # 以下為 bottom 群組
    # bottom_button 綁定 echo_hello 事件處理，點擊該按鈕會印出 hello world :)
    #bottom_button = tk.Button(bottom_frame, text='Black', fg='black', command=echo_hello)
    # 讓系統自動擺放元件（靠下方）
    #bottom_button.pack(side=tk.BOTTOM)

    # 運行主程式
    window.mainloop()

if __name__ == '__main__':
    draw_window()