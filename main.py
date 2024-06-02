import tkinter
from tkinter import ttk
from csv import reader, writer
from PIL import Image, ImageTk, ImageDraw, ImageFont
from time import sleep
import os
from threading import Thread
from random import randint
from cryptography.fernet import Fernet
import keyboard
from pygame import mixer

Time = 0
mixer.init()

# if not os.path.exists('app_data'):
#     raise Exception('Please Enter Maze directory')
    
os.chdir('\\'.join(__file__.split('\\')[:-1]))

class User_data:
    def __init__(self) -> None:
        self.key = b'ucEuQnCBVzNydQ_fnAxk2BheGWCN9D4hoGBDZxmzasg='
        self.f = Fernet(self.key)
        self.data = dict()
        self.data['best_score_e'] = 0
        self.data['best_score_m'] = 0
        self.data['best_score_h'] = 0
        
        self.data['best_time_e'] = 0
        self.data['best_time_m'] = 0
        self.data['best_time_h'] = 0

        self.data['music_vol'] = 100
        self.data['sound_vol'] = 100
        
        self.data['mode'] = 'e'

        self.get_user_data()

    def get_user_data(self) -> None:
        if not os.path.exists('player_data.csv'):
            self.save_user_data()
        with open('player_data.csv', 'r') as player_data:
            player_data = reader(player_data)
            for i in tuple(player_data):
                if i:
                    i, v  = i[0], i[1]
                    v = self.decode(v)
                    try:
                        self.data[i] = int(v)
                    except:
                        self.data[i] = v

    def save_user_data(self) -> None:
        with open('player_data.csv', 'w') as player_data:
            player_data = writer(player_data)
            for i, v in zip(self.data.keys(), self.data.values()):
                player_data.writerow([i, self.encode(v)])

    def decode(self, data) -> None:
        return self.f.decrypt(data.encode()).decode()
        # return data
    
    def encode(self, data) -> None:
        return self.f.encrypt(str(data).encode()).decode()
        # return data

class Sounds:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.load_sounds()

        self.update_vols()

        mixer.music.play()
    
    def load_sounds(self) -> None:
        self.bg_music = mixer.music.load('app_data/background music.mp3')
        self.coin_collected = mixer.Sound('app_data/coin collected.mp3')
        self.victory = mixer.Sound('app_data/Victory.mp3')

    def update_vols(self) -> None:
        mixer.music.set_volume(float(self.gui.user_data.data['music_vol'])/100)
        self.coin_collected.set_volume(float(self.gui.user_data.data['sound_vol'])//100)
        self.victory.set_volume(float(self.gui.user_data.data['sound_vol'])//100)

class Start_screen:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.create_ui()
        
        # self.close_ui()

        self.gui.canvas.tag_bind(self.home_screen_button1, '<Button-1>', lambda event:(self.close_ui(), self.gui.choose_mode.open_ui()))

        self.gui.canvas.tag_bind(self.home_screen_button2, '<Button-1>', lambda event:(self.close_ui(), self.gui.leaderboard.open_ui()))

        self.gui.canvas.tag_bind(self.home_screen_button3, '<Button-1>', lambda event:self.gui.settings.open_ui())
        
        self.gui.canvas.tag_bind(self.home_screen_button4, '<Button-1>', lambda event:(self.close_ui(), self.gui.credits.open_ui()))

    def create_ui(self) -> None:
        self.home_screen_button1 = self.gui.canvas.create_image(self.gui.window_width*2//5 - 20, self.gui.window_height*2//5 - 20, image=self.gui.images['home_screen_button1'])
        self.home_screen_button2 = self.gui.canvas.create_image(self.gui.window_width*3//5 + 20, self.gui.window_height*2//5 - 20, image=self.gui.images['home_screen_button2'])
        self.home_screen_button3 = self.gui.canvas.create_image(self.gui.window_width*2//5 - 20, self.gui.window_height*3//5 + 20, image=self.gui.images['home_screen_button3'])
        self.home_screen_button4 = self.gui.canvas.create_image(self.gui.window_width*3//5 + 20, self.gui.window_height*3//5 + 20, image=self.gui.images['home_screen_button4'])

    def update_ui(self) -> None:
        pass
    
    def open_ui(self) -> None:
        self.update_ui()
        self.gui.canvas.itemconfig(self.home_screen_button1, state='normal')
        self.gui.canvas.itemconfig(self.home_screen_button2, state='normal')
        self.gui.canvas.itemconfig(self.home_screen_button3, state='normal')
        self.gui.canvas.itemconfig(self.home_screen_button4, state='normal')

    def close_ui(self) -> None:
        self.gui.canvas.itemconfig(self.home_screen_button1, state='hidden')
        self.gui.canvas.itemconfig(self.home_screen_button2, state='hidden')
        self.gui.canvas.itemconfig(self.home_screen_button3, state='hidden')
        self.gui.canvas.itemconfig(self.home_screen_button4, state='hidden')

    def destroy_ui(self) -> None:
        self.gui.canvas.delete(self.home_screen_button1)
        self.gui.canvas.delete(self.home_screen_button2)
        self.gui.canvas.delete(self.home_screen_button3)
        self.gui.canvas.delete(self.home_screen_button4)

class Choose_mode:
    def __init__(self, gui) -> None:
        self.gui = gui
        
        self.create_ui()

        self.close_ui()
        
        def change_data(mode):
            self.gui.user_data.data['mode'] = mode
            self.update_ui()

        self.gui.canvas.tag_bind(self.easy_button_white, '<Button-1>', lambda event: change_data('e'))

        self.gui.canvas.tag_bind(self.medium_button_white, '<Button-1>', lambda event: change_data('m'))

        self.gui.canvas.tag_bind(self.hard_button_white, '<Button-1>', lambda event: change_data('h'))

        self.gui.canvas.tag_bind(self.back_button, '<Button-1>', lambda event: (self.close_ui(), self.gui.start_screen.open_ui()))
        
        def start_maze(event):
            self.close_ui()
            self.gui.maze = Maze(self.gui)
        self.gui.canvas.tag_bind(self.start_button, '<Button-1>', start_maze)

    def create_ui(self) -> None:
        self.choose_mode_img = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['choose_mode_img'])

        self.start_button = self.gui.canvas.create_image(self.gui.window_width*599//1358, self.gui.window_height*557//764, image=self.gui.images['start_button'])

        self.back_button = self.gui.canvas.create_image(self.gui.window_width*759//1358, self.gui.window_height*557//764, image=self.gui.images['back_button'])

        self.easy_button_white = self.gui.canvas.create_image(self.gui.window_width*719//1358, self.gui.window_height*337/784, image=self.gui.images['easy_button_white'])

        self.medium_button_white = self.gui.canvas.create_image(self.gui.window_width*719//1358, self.gui.window_height*397//764, image=self.gui.images['medium_button_white'])

        self.hard_button_white = self.gui.canvas.create_image(self.gui.window_width*719//1358, self.gui.window_height*457//764, image=self.gui.images['hard_button_white'])

        self.easy_button_blue = self.gui.canvas.create_image(self.gui.window_width*719//1358, self.gui.window_height*337/784, image=self.gui.images['easy_button_blue'])
        self.gui.canvas.itemconfig(self.easy_button_blue, state='normal')

        self.medium_button_blue = self.gui.canvas.create_image(self.gui.window_width*719//1358, self.gui.window_height*397//764, image=self.gui.images['medium_button_blue'])
        self.gui.canvas.itemconfig(self.medium_button_blue, state='normal')

        self.hard_button_blue = self.gui.canvas.create_image(self.gui.window_width*719//1358, self.gui.window_height*457//764, image=self.gui.images['hard_button_blue'])
        self.gui.canvas.itemconfig(self.hard_button_blue, state='normal')

    def update_ui(self) -> None:
        self.gui.canvas.itemconfig(self.easy_button_blue, state='hidden')
        self.gui.canvas.itemconfig(self.medium_button_blue, state='hidden')
        self.gui.canvas.itemconfig(self.hard_button_blue, state='hidden')
        self.gui.canvas.itemconfig(self.easy_button_white, state='normal')
        self.gui.canvas.itemconfig(self.medium_button_white, state='normal')
        self.gui.canvas.itemconfig(self.hard_button_white, state='normal')
        self.gui.canvas.itemconfig({'e': self.easy_button_white, 'm': self.medium_button_white, 'h': self.hard_button_white}[self.gui.user_data.data['mode']], state='hidden')
        self.gui.canvas.itemconfig({'e': self.easy_button_blue, 'm': self.medium_button_blue, 'h': self.hard_button_blue}[self.gui.user_data.data['mode']], state='normal')
    
    def open_ui(self) -> None:
        self.gui.canvas.itemconfig(self.choose_mode_img, state='normal')
        self.gui.canvas.itemconfig(self.start_button, state='normal')
        self.gui.canvas.itemconfig(self.back_button, state='normal')
        self.gui.canvas.itemconfig(self.easy_button_white, state='normal')
        self.gui.canvas.itemconfig(self.medium_button_white, state='normal')
        self.gui.canvas.itemconfig(self.hard_button_white, state='normal')
        self.update_ui()

    def close_ui(self) -> None:
        self.gui.canvas.itemconfig(self.choose_mode_img, state='hidden')
        self.gui.canvas.itemconfig(self.start_button, state='hidden')
        self.gui.canvas.itemconfig(self.back_button, state='hidden')
        self.gui.canvas.itemconfig(self.easy_button_white, state='hidden')
        self.gui.canvas.itemconfig(self.medium_button_white, state='hidden')
        self.gui.canvas.itemconfig(self.hard_button_white, state='hidden')
        self.gui.canvas.itemconfig(self.easy_button_blue, state='hidden')
        self.gui.canvas.itemconfig(self.medium_button_blue, state='hidden')
        self.gui.canvas.itemconfig(self.hard_button_blue, state='hidden')
    
    def destroy_ui(self) -> None:
        self.gui.canvas.delete(self.choose_mode_img)
        self.gui.canvas.delete(self.start_button)
        self.gui.canvas.delete(self.back_button)
        self.gui.canvas.delete(self.easy_button_white)
        self.gui.canvas.delete(self.medium_button_white)
        self.gui.canvas.delete(self.hard_button_white)
        self.gui.canvas.delete(self.easy_button_blue)
        self.gui.canvas.delete(self.medium_button_blue)
        self.gui.canvas.delete(self.hard_button_blue)

class Settings:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.sound_vol = tkinter.DoubleVar()
        self.music_vol = tkinter.DoubleVar()
        
        self.create_ui()

        self.close_ui()

        def save(event):
            self.gui.user_data.data['sound_vol'] = self.get_sound_vol()
            self.gui.user_data.data['music_vol'] = self.get_music_vol()
            self.gui.sounds.update_vols()
            self.close_ui()

        self.gui.canvas.tag_bind(self.save_button, '<Button-1>', save)

        self.gui.canvas.tag_bind(self.cancel_button, '<Button-1>', lambda event: self.close_ui())

    def get_sound_vol(self):
        return '{: .2f}'.format(self.sound_vol.get())
    
    def get_music_vol(self):
        return '{: .2f}'.format(self.music_vol.get())  

    def create_ui(self) -> None:
        self.settings_img = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['settings_img'])
        
        self.sound_image = self.gui.canvas.create_image(self.gui.window_width//2 - self.gui.window_width//13.58, self.gui.window_height//2 + self.gui.window_height//15.28, image=self.gui.images['sound_image'])
        
        self.music_image = self.gui.canvas.create_image(self.gui.window_width//2 - self.gui.window_width//13.58, self.gui.window_height//2 - self.gui.window_height//15.28, image=self.gui.images['music_image'])

        self.save_button = self.gui.canvas.create_image(self.gui.window_width*599//1358, self.gui.window_height*557//764, image=self.gui.images['save_button'])

        self.cancel_button = self.gui.canvas.create_image(self.gui.window_width*759//1358, self.gui.window_height*557//764, image=self.gui.images['cancel_button'])

        self.sound_slider = ttk.Scale(self.gui.root, from_=0, to=100, orient='horizontal', variable=self.music_vol, length=self.gui.window_height*175//764)
        
        self.music_slider = ttk.Scale(self.gui.root, from_=0, to=100, orient='horizontal', variable=self.sound_vol, length=self.gui.window_height*175//764)

        self.sound_slider.place(x=self.gui.window_width*1891//4074, y=self.gui.window_height//2 - self.gui.window_height//15.28 - self.gui.window_height//44)

        self.music_slider.place(x=self.gui.window_width*1891//4074,  y=self.gui.window_height//2 + self.gui.window_height//15.28 - self.gui.window_height//44)
        
    def update_ui(self) -> None:
        self.sound_slider.set(self.gui.user_data.data['music_vol'])
        self.music_slider.set(self.gui.user_data.data['sound_vol'])
    
    def open_ui(self) -> None:
        self.update_ui()
        self.gui.canvas.itemconfig(self.settings_img, state='normal')
        self.gui.canvas.itemconfig(self.sound_image, state='normal')
        self.gui.canvas.itemconfig(self.music_image, state='normal')
        self.gui.canvas.itemconfig(self.save_button, state='normal')
        self.gui.canvas.itemconfig(self.cancel_button, state='normal')
        self.sound_slider.place(x=self.gui.window_width*1891//4074, y=self.gui.window_height//2 - self.gui.window_height//15.28 - self.gui.window_height//44)
        self.music_slider.place(x=self.gui.window_width*1891//4074,  y=self.gui.window_height//2 + self.gui.window_height//15.28 - self.gui.window_height//44)

    def close_ui(self) -> None:
        self.gui.canvas.itemconfig(self.settings_img, state='hidden')
        self.gui.canvas.itemconfig(self.sound_image, state='hidden')
        self.gui.canvas.itemconfig(self.music_image, state='hidden')
        self.gui.canvas.itemconfig(self.save_button, state='hidden')
        self.gui.canvas.itemconfig(self.cancel_button, state='hidden')
        self.sound_slider.place_forget()
        self.music_slider.place_forget()

    def destroy_ui(self) -> None:
        self.gui.canvas.delete(self.settings_img)
        self.gui.canvas.delete(self.sound_image)
        self.gui.canvas.delete(self.music_image)
        self.gui.canvas.delete(self.save_button)
        self.gui.canvas.delete(self.cancel_button)
                
class Timer:
    def __init__(self, time, update_fun, gui) -> None:
        self.time = time
        self.gui = gui
        self.update_fun = update_fun
        self.paused = False
        self.running = True
        self.start_timer()

    def start_timer(self) -> None:
        def timer():
            while self.time > 0:
                self.time -= 1
                if not self.running:
                    return
                while True:
                    sleep(1)
                    if not self.paused:
                        break
                global Time
                Time = self.time
                self.update_fun()
            self.paused = True
            self.running = False
            self.gui.game_over.open_ui()

        Thread(target=timer).start()
    
    def pause_timer(self) -> None:
        self.paused = True

    def resume_timer(self) -> None:
        self.paused = False

    def stop_timer(self) -> None:
        self.running = False

    def add_time(self, time_add) -> None:
        self.time += time_add
        
    def remove_time(self, time_remove) -> None:
        self.time -= time_remove

class Leaderboard:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.create_ui()

        self.close_ui()

        self.gui.canvas.tag_bind(self.bg, '<Button-1>', lambda event: (self.close_ui(), self.gui.start_screen.open_ui()))

    def create_ui(self):
        self.bg = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['stats_background_bg'])

        self.background_e = self.gui.canvas.create_image(self.gui.window_width*379//1358, self.gui.window_height*15//31 ,image=self.gui.images['leaderstats_background'] )
        self.headding_e = self.gui.canvas.create_text(self.gui.window_width*379//1358, self.gui.window_height*227//620, text='EASY', font='Helvitica 15 bold', fill='white')
        self.time_text_bg_e = self.gui.canvas.create_image(self.gui.window_width*379//1358, self.gui.window_height*14//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.score_text_bg_e = self.gui.canvas.create_image(self.gui.window_width*379//1358, self.gui.window_height*17//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.time_img_e = self.gui.canvas.create_image(self.gui.window_width*152//679, self.gui.window_height*14//31, image=self.gui.images['clock'])
        self.score_img_e = self.gui.canvas.create_image(self.gui.window_width*152//679, self.gui.window_height*17//31, image=self.gui.images['score'])
        self.time_text_e = self.gui.canvas.create_text(self.gui.window_width*57//194, self.gui.window_height*14//31+5, text='00:00', font='Helvitica 25 bold', fill='white')
        self.score_text_e = self.gui.canvas.create_text(self.gui.window_width*57//194, self.gui.window_height*17//31+5, text='0000', font='Helvitica 25 bold', fill='white')
        
        self.background_m = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*15//31 ,image=self.gui.images['leaderstats_background'] )
        self.headding_m = self.gui.canvas.create_text(self.gui.window_width//2, self.gui.window_height*227//620, text='MEDIUM', font='Helvitica 15 bold', fill='white')
        self.time_text_bg_m = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*14//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.score_text_bg_m = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*17//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.time_img_m = self.gui.canvas.create_image(self.gui.window_width*302//679, self.gui.window_height*14//31, image=self.gui.images['clock'])
        self.score_img_m = self.gui.canvas.create_image(self.gui.window_width*302//679, self.gui.window_height*17//31, image=self.gui.images['score'])
        self.time_text_m = self.gui.canvas.create_text(self.gui.window_width*699//1358, self.gui.window_height*14//31+5, text='00:00', font='Helvitica 25 bold', fill='white')
        self.score_text_m = self.gui.canvas.create_text(self.gui.window_width*699//1358, self.gui.window_height*17//31+5, text='0000', font='Helvitica 25 bold', fill='white')
        
        self.background_h = self.gui.canvas.create_image(self.gui.window_width*979//1358, self.gui.window_height*15//31 ,image=self.gui.images['leaderstats_background'] )
        self.headding_h = self.gui.canvas.create_text(self.gui.window_width*979//1358, self.gui.window_height*227//620, text='HARD', font='Helvitica 15 bold', fill='white')
        self.time_text_bg_h = self.gui.canvas.create_image(self.gui.window_width*979//1358, self.gui.window_height*14//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.score_text_bg_h = self.gui.canvas.create_image(self.gui.window_width*979//1358, self.gui.window_height*17//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.time_img_h = self.gui.canvas.create_image(self.gui.window_width*452//679, self.gui.window_height*14//31, image=self.gui.images['clock'])
        self.score_img_h = self.gui.canvas.create_image(self.gui.window_width*452//679, self.gui.window_height*17//31, image=self.gui.images['score'])
        self.time_text_h = self.gui.canvas.create_text(self.gui.window_width*999//1358, self.gui.window_height*14//31+5, text='00:00', font='Helvitica 25 bold', fill='white')
        self.score_text_h = self.gui.canvas.create_text(self.gui.window_width*999//1358, self.gui.window_height*17//31+5, text='0000', font='Helvitica 25 bold', fill='white')
    
    def update_ui(self):
        time_e = self.gui.user_data.data['best_time_e']
        time_m = self.gui.user_data.data['best_time_m']
        time_h = self.gui.user_data.data['best_time_h']
        self.gui.canvas.itemconfig(self.time_text_e, text=f'{time_e//60:02}:{time_e-(time_e//60)*60:02}')
        self.gui.canvas.itemconfig(self.time_text_m, text=f'{time_m//60:02}:{time_m-(time_m//60)*60:02}')
        self.gui.canvas.itemconfig(self.time_text_h, text=f'{time_h//60:02}:{time_h-(time_h//60)*60:02}')
        
        score_e = self.gui.user_data.data['best_score_e']
        score_m = self.gui.user_data.data['best_score_m']
        score_h = self.gui.user_data.data['best_score_h']
        self.gui.canvas.itemconfig(self.score_text_e, text=f'{score_e:04}')
        self.gui.canvas.itemconfig(self.score_text_m, text=f'{score_m:04}')
        self.gui.canvas.itemconfig(self.score_text_h, text=f'{score_h:04}')
    
    def open_ui(self):
        self.update_ui()
        self.gui.canvas.itemconfig(self.bg, state='normal')

        self.gui.canvas.itemconfig(self.background_e, state='normal')
        self.gui.canvas.itemconfig(self.headding_e, state='normal')
        self.gui.canvas.itemconfig(self.time_text_bg_e, state='normal')
        self.gui.canvas.itemconfig(self.score_text_bg_e, state='normal')
        self.gui.canvas.itemconfig(self.time_img_e, state='normal')
        self.gui.canvas.itemconfig(self.score_img_e, state='normal')
        self.gui.canvas.itemconfig(self.time_text_e, state='normal')
        self.gui.canvas.itemconfig(self.score_text_e, state='normal')

        self.gui.canvas.itemconfig(self.background_m, state='normal')
        self.gui.canvas.itemconfig(self.headding_m, state='normal')
        self.gui.canvas.itemconfig(self.time_text_bg_m, state='normal')
        self.gui.canvas.itemconfig(self.score_text_bg_m, state='normal')
        self.gui.canvas.itemconfig(self.time_img_m, state='normal')
        self.gui.canvas.itemconfig(self.score_img_m, state='normal')
        self.gui.canvas.itemconfig(self.time_text_m, state='normal')
        self.gui.canvas.itemconfig(self.score_text_m, state='normal')

        self.gui.canvas.itemconfig(self.background_h, state='normal')
        self.gui.canvas.itemconfig(self.headding_h, state='normal')
        self.gui.canvas.itemconfig(self.time_text_bg_h, state='normal')
        self.gui.canvas.itemconfig(self.score_text_bg_h, state='normal')
        self.gui.canvas.itemconfig(self.time_img_h, state='normal')
        self.gui.canvas.itemconfig(self.score_img_h, state='normal')
        self.gui.canvas.itemconfig(self.time_text_h, state='normal')
        self.gui.canvas.itemconfig(self.score_text_h, state='normal')
    
    def close_ui(self):
        self.gui.canvas.itemconfig(self.bg, state='hidden')

        self.gui.canvas.itemconfig(self.background_e, state='hidden')
        self.gui.canvas.itemconfig(self.headding_e, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_bg_e, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_bg_e, state='hidden')
        self.gui.canvas.itemconfig(self.time_img_e, state='hidden')
        self.gui.canvas.itemconfig(self.score_img_e, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_e, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_e, state='hidden')

        self.gui.canvas.itemconfig(self.background_m, state='hidden')
        self.gui.canvas.itemconfig(self.headding_m, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_bg_m, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_bg_m, state='hidden')
        self.gui.canvas.itemconfig(self.time_img_m, state='hidden')
        self.gui.canvas.itemconfig(self.score_img_m, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_m, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_m, state='hidden')

        self.gui.canvas.itemconfig(self.background_h, state='hidden')
        self.gui.canvas.itemconfig(self.headding_h, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_bg_h, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_bg_h, state='hidden')
        self.gui.canvas.itemconfig(self.time_img_h, state='hidden')
        self.gui.canvas.itemconfig(self.score_img_h, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_h, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_h, state='hidden')
    
    def destroy_ui(self):
        self.gui.canvas.delete(self.background_e)
        self.gui.canvas.delete(self.headding_e)
        self.gui.canvas.delete(self.time_text_bg_e)
        self.gui.canvas.delete(self.score_text_bg_e)
        self.gui.canvas.delete(self.time_img_e)
        self.gui.canvas.delete(self.score_img_e)
        self.gui.canvas.delete(self.time_text_e)
        self.gui.canvas.delete(self.score_text_e)

        self.gui.canvas.delete(self.background_m)
        self.gui.canvas.delete(self.headding_m)
        self.gui.canvas.delete(self.time_text_bg_m)
        self.gui.canvas.delete(self.score_text_bg_m)
        self.gui.canvas.delete(self.time_img_m)
        self.gui.canvas.delete(self.score_img_m)
        self.gui.canvas.delete(self.time_text_m)
        self.gui.canvas.delete(self.score_text_m)

        self.gui.canvas.delete(self.background_h)
        self.gui.canvas.delete(self.headding_h)
        self.gui.canvas.delete(self.time_text_bg_h)
        self.gui.canvas.delete(self.score_text_bg_h)
        self.gui.canvas.delete(self.time_img_h)
        self.gui.canvas.delete(self.score_img_h)
        self.gui.canvas.delete(self.time_text_h)
        self.gui.canvas.delete(self.score_text_h)

class Maze:
    def __init__(self, gui) -> None:
        self.gui = gui
        self.rows = {'e': 10, 'm': 15, 'h': 20}[self.gui.user_data.data['mode']]
        self.cols = {'e': 10, 'm': 15, 'h': 20}[self.gui.user_data.data['mode']]
        self.initilize_data()
        self.create_ui()
        self.timer = Timer({'e': 15, 'm': 30, 'h': 30}[self.gui.user_data.data['mode']] , self.scoreboard.update_timer, self.gui)

    def initilize_data(self) -> None:
        self.grids = []
        self.grid_box = []
        self.checked_walls = []
        self.checked_grids = []
        self.grids_ = []
        self.path = [[0, 0]]
        self.end = [0, 0]
        self.images = []
        self.score = 0
        
        self.grid_size_y = (self.gui.window_height - 20)//self.cols
        self.grid_size_x = self.grid_size_y

        for j in range(self.cols):
            self.grids.append([])
            self.grid_box.append([])
            self.images.append([])
            for i in range(self.rows):
                self.grids[j].append([None, None, None, None])
                self.grid_box[j].append([])
                self.images[j].append([])

    def create_ui(self) -> None:
        self.scoreboard = Scoreboard(self.gui)
        self.scoreboard.open_ui()

        self.maze_bg_image = self.gui.canvas.create_image(self.gui.window_width*9//14, self.gui.window_height//2, image=self.gui.images['maze_bg'])
        
        self.x_offset = self.gui.window_width*9//14 - self.grid_size_x*self.cols//2 - 5
        self.y_offset = self.gui.window_height//2 - self.grid_size_y*self.rows//2 - 5


        for j in range(1, self.cols):
            for i in range(self.rows):
                self.grids[j][i][3] = self.gui.canvas.create_line(self.x_offset + 2+i*self.grid_size_x, self.y_offset + 2+j*self.grid_size_y, self.x_offset + 2+(i+1)*self.grid_size_x, self.y_offset + 2+j*self.grid_size_y, fill='white', width=2)
                if j > 0:
                    self.grids[j - 1][i][1] = self.grids[j][i][3]

        for j in range(1, self.rows):
            for i in range(self.cols):
                self.grids[i][j][0] = self.gui.canvas.create_line(self.x_offset + 2+j*self.grid_size_x, self.y_offset + 2+i*self.grid_size_y, self.x_offset + 2+j*self.grid_size_x, self.y_offset + 2+(i+1)*self.grid_size_y, fill='white', width=2)
                if j > 0:
                    self.grids[i][j - 1][2] = self.grids[i][j][0]

        for i in range(self.rows):
            for j in range(self.cols):
                self.grid_box[j][i] = self.gui.canvas.create_oval(self.x_offset + i*self.grid_size_x + 2 + 13, self.y_offset + j*self.grid_size_y + 2 + 13, self.x_offset + (i + 1)*self.grid_size_x + 2 - 13, self.y_offset + (j + 1)*self.grid_size_y + 2 - 13, fill='white')
                self.gui.canvas.itemconfig(self.grid_box[j][i], state='hidden')
        self.gui.canvas.itemconfig(self.grid_box[0][0], state='normal')
        
        for _ in range({'e':2, 'm':3, 'h':5}[self.gui.user_data.data['mode']]):
            while True:
                i, j = randint(0, self.rows - 1), randint(0, self.cols - 1)
                if not self.images[j][i]:
                    break
            self.images[j][i] = self.gui.canvas.create_image((self.x_offset + i*self.grid_size_x + 2 + 10 + self.x_offset + (i + 1)*self.grid_size_x + 2 - 10)//2, (self.y_offset + j*self.grid_size_y + 2 + 10 + self.y_offset + (j + 1)*self.grid_size_y + 2 - 10)//2, image=(self.gui.images['clock_maze_'+self.gui.user_data.data['mode']])), 'clock'

        for _ in range({'e':4, 'm':5, 'h':9}[self.gui.user_data.data['mode']]):
            while True:
                i, j = randint(0, self.rows - 1), randint(0, self.cols - 1)
                if not self.images[j][i]:
                    break
            self.images[j][i] = self.gui.canvas.create_image((self.x_offset + i*self.grid_size_x + 2 + 10 + self.x_offset + (i + 1)*self.grid_size_x + 2 - 10)//2, (self.y_offset + j*self.grid_size_y + 2 + 10 + self.y_offset + (j + 1)*self.grid_size_y + 2 - 10)//2, image=(self.gui.images['coin_maze_'+self.gui.user_data.data['mode']])), 'coin'

        while True:
            i, j = randint(5, self.rows - 1), randint(5, self.cols - 1)
            if not self.images[j][i]:
                break
        self.end = [i, j]
        self.images[j][i] = self.gui.canvas.create_image((self.x_offset + i*self.grid_size_x + 2 + 10 + self.x_offset + (i + 1)*self.grid_size_x + 2 - 10)//2, (self.y_offset + j*self.grid_size_y + 2 + 10 + self.y_offset + (j + 1)*self.grid_size_y + 2 - 10)//2, image=(self.gui.images['crown_maze_'+self.gui.user_data.data['mode']])), 'crown'
        
        def get_moves(grid):
            moves = self.grids[grid[0]][grid[1]].copy()
            index = 0
            while True:
                if index == len(moves):
                    break
                wall = moves[index]
                if not wall:
                    moves.pop(index)
                    continue
                row, col = grid[0], grid[1]
                i = self.grids[row][col].index(wall)
                if i == 0:
                    col-=1
                elif i == 1:
                    row+=1
                elif i == 2:
                    col+=1
                elif i == 3:
                    row-=1
                if [row, col] in self.checked_grids:
                    moves.pop(index)
                    continue
                index += 1
            return moves
        
        self.checked_grids.append([0, 0])
        self.grids_.append([0, 0])
        
        while True:
            if len(self.checked_grids) == self.rows*self.cols:
                break
            moves = get_moves(self.grids_[-1])
            row = self.grids_[-1][0]
            col = self.grids_[-1][1]

            if moves:
                num = randint(0, len(moves) - 1)
                wall = moves[num]
                self.checked_walls.append(wall)
                index = self.grids[self.grids_[-1][0]][self.grids_[-1][1]].index(wall)
                moves.remove(wall)

                self.gui.canvas.delete(wall)
                if index == 0:
                    col-=1
                elif index == 1:
                    row+=1
                elif index == 2:
                    col+=1
                elif index == 3:
                    row-=1
                self.checked_grids.append([row, col])
                self.grids_.append([row, col])
            else:
                self.grids_.pop(-1)

    def update_ui(self, data) -> None:
        self.scoreboard.update_ui(data=data)
    
    def open_ui(self) -> None:
        pass

    def close_ui(self) -> None:
        pass

    def destroy_ui(self) -> None:
        self.scoreboard.destroy_ui()
        self.gui.canvas.delete(self.maze_bg_image)
        for j in range(self.cols):
            for i in range(self.rows):
                self.gui.canvas.delete(self.grids[i][j][0])
                self.gui.canvas.delete(self.grids[i][j][1])
                self.gui.canvas.delete(self.grid_box[i][j])
                try:
                    self.gui.canvas.delete(self.images[i][j][0])
                except:
                    pass

    def button_clicked(self, direction = None):
        if self.timer.paused or not self.timer.running:
            return
        def get_moves():
            walls = self.grids[self.path[-1][0]][self.path[-1][1]]
            directions = []
            for i in walls:
                if i and i in self.checked_walls:
                    if walls.index(i) == 0:
                        directions.append('left')
                    if walls.index(i) == 1:
                        directions.append('bot')
                    if walls.index(i) == 2:
                        directions.append('right')
                    if walls.index(i) == 3:
                        directions.append('top')
            return directions
        
        self.gui.canvas.itemconfig(self.grid_box[self.path[-1][0]][self.path[-1][1]], state=('normal', 'hidden')[0 if [self.path[-1][0], self.path[-1][1]] in self.path else 1])
        row, col = self.path[-1]
        moves = get_moves()
        
        if self.images[row][col]:
            if self.images[row][col][1] == 'clock':
                self.gui.sounds.coin_collected.play()
                self.gui.canvas.delete(self.images[row][col][0])
                self.timer.add_time(5)
                self.images[row][col] = []
            elif self.images[row][col][1] == 'coin':
                self.gui.sounds.coin_collected.play()
                self.gui.canvas.delete(self.images[row][col][0])
                self.score += 50
                self.scoreboard.update_ui({'score':self.score, 'moves':len(self.path)})
                self.images[row][col] = []
            elif self.images[row][col][1] == 'crown':
                self.gui.sounds.victory.play()
                self.timer.stop_timer()
                self.gui.victory.open_ui()

                mode = self.gui.user_data.data['mode']
                if Time >= int(self.gui.user_data.data['best_time_'+mode]):
                    self.gui.user_data.data['best_time_'+mode] = Time
                if self.gui.maze.score >= int(self.gui.user_data.data['best_score_'+mode]):
                    self.gui.user_data.data['best_score_'+mode] = Time
            return

        if not direction or direction == -1:
            if len(moves) <= 2 and (len(self.path) >= 2):
                _row, _col = self.path[-2]
                if col - _col == 1:
                    _from = 'left'
                if col - _col == -1:
                    _from = 'right'
                if row - _row == 1:
                    _from = 'top'
                if row - _row == -1:
                    _from = 'bot'
                if _from in moves:
                    moves.remove(_from)
                if moves:
                    if direction == -1:
                        direction = _from
                    else:
                        direction = moves[0]
                else:
                    return
                moves = get_moves()
            else:
                return
            
        if direction in moves:
            if direction == 'left':
                if col != 0:
                    col -= 1
            elif direction == 'bot':
                if row != self.rows - 1:
                    row += 1
            elif direction == 'right':
                if col != self.cols - 1:
                    col += 1
            elif direction == 'top':
                if row != 0:
                    row -= 1
            self.scoreboard.update_ui({'score':self.score, 'moves':len(self.path)})

            if [row, col] in self.path:
                self.gui.canvas.itemconfig(self.grid_box[self.path[-1][0]][self.path[-1][1]], state='hidden')
                self.path.pop(-1)
                sleep(0.05)
                self.button_clicked(direction=-1)
            else:
                self.path.append([row, col])
                sleep(0.05)
                self.button_clicked()

class Scoreboard:
    def __init__(self, gui) -> None:
            self.gui = gui
            self.create_ui()

            self.close_ui()

            self.gui.canvas.tag_bind(self.pause_button, '<Button-1>', lambda event: (self.gui.maze.timer.pause_timer(), self.gui.pause_screen.open_ui()))

            def restart(event):
                self.gui.maze.destroy_ui()
                self.gui.maze.timer.stop_timer()
                self.gui.maze = Maze(self.gui)
            self.gui.canvas.tag_bind(self.restart_button, '<Button-1>', restart)
            self.gui.canvas.tag_bind(self.exit_button, '<Button-1>', lambda event: (self.gui.maze.destroy_ui(), self.gui.maze.timer.stop_timer(), self.gui.start_screen.open_ui()))

    def create_ui(self) -> None:
        self.stats_background = self.gui.canvas.create_image(self.gui.window_width//6, self.gui.window_height//2, image=self.gui.images['stats_background'])

        self.clock = self.gui.canvas.create_image(self.gui.window_width//9, self.gui.window_height*6//17, image=self.gui.images['clock'])
        self.clock_text_bg = self.gui.canvas.create_image(self.gui.window_width*25//144, self.gui.window_height*6//17, image=self.gui.images['scoreboard_text_bg'])
        self.clock_text = self.gui.canvas.create_text(self.gui.window_width*23//126, self.gui.window_height*6//17, text='00:00', font='ARLRDBD 25 bold', fill='white')

        self.score = self.gui.canvas.create_image(self.gui.window_width//9, self.gui.window_height*10//21, image=self.gui.images['score'])
        self.score_text_bg = self.gui.canvas.create_image(self.gui.window_width*25//144, self.gui.window_height*10//21, image=self.gui.images['scoreboard_text_bg'])
        self.score_text = self.gui.canvas.create_text(self.gui.window_width*23//126, self.gui.window_height*10//21, text='0000', font='ARLRDBD 25 bold', fill='white')

        self.moves = self.gui.canvas.create_image(self.gui.window_width//9, self.gui.window_height*1349//2292, image=self.gui.images['moves'])
        self.moves_text_bg = self.gui.canvas.create_image(self.gui.window_width*25//144, self.gui.window_height*1349//2292, image=self.gui.images['scoreboard_text_bg'])
        self.moves_text = self.gui.canvas.create_text(self.gui.window_width*23//126, self.gui.window_height*1349//2292, text='00', font='ARLRDBD 25 bold', fill='white')

        self.pause_button = self.gui.canvas.create_image(self.gui.window_width//9, self.gui.window_height*787//1146, image=self.gui.images['pause_button'])
        self.restart_button = self.gui.canvas.create_image(self.gui.window_width*2033//12222, self.gui.window_height*787//1146, image=self.gui.images['restart_button'])
        self.exit_button = self.gui.canvas.create_image(self.gui.window_width*1354//6111, self.gui.window_height*787//1146, image=self.gui.images['exit_button'])  

    def update_timer(self) -> None:
        try:
            self.gui.canvas.itemconfig(self.clock_text, text=f'{Time//60:02}:{Time-(Time//60)*60:02}')
        except:
            pass   

    def update_ui(self, data) -> None:
        self.update_timer()
        score = data['score']
        moves = data['moves']
        self.gui.canvas.itemconfig(self.score_text, text=f'{score:04}')
        self.gui.canvas.itemconfig(self.moves_text, text=f'{moves:02}')
    
    def open_ui(self) -> None:
        self.update_ui({'score':'0000', 'moves':'00'})
        self.gui.canvas.itemconfig(self.stats_background, state='normal')
        self.gui.canvas.itemconfig(self.clock, state='normal')
        self.gui.canvas.itemconfig(self.clock_text_bg, state='normal')
        self.gui.canvas.itemconfig(self.clock_text, state='normal')
        self.gui.canvas.itemconfig(self.score, state='normal')
        self.gui.canvas.itemconfig(self.score_text_bg, state='normal')
        self.gui.canvas.itemconfig(self.score_text, state='normal')
        self.gui.canvas.itemconfig(self.moves, state='normal')
        self.gui.canvas.itemconfig(self.moves_text_bg, state='normal')
        self.gui.canvas.itemconfig(self.moves_text, state='normal')
        self.gui.canvas.itemconfig(self.pause_button, state='normal')
        self.gui.canvas.itemconfig(self.restart_button, state='normal')
        self.gui.canvas.itemconfig(self.exit_button, state='normal')

    def close_ui(self) -> None:
        self.gui.canvas.itemconfig(self.stats_background, state='hidden')
        self.gui.canvas.itemconfig(self.clock, state='hidden')
        self.gui.canvas.itemconfig(self.clock_text_bg, state='hidden')
        self.gui.canvas.itemconfig(self.clock_text, state='hidden')
        self.gui.canvas.itemconfig(self.score, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_bg, state='hidden')
        self.gui.canvas.itemconfig(self.score_text, state='hidden')
        self.gui.canvas.itemconfig(self.moves, state='hidden')
        self.gui.canvas.itemconfig(self.moves_text_bg, state='hidden')
        self.gui.canvas.itemconfig(self.moves_text, state='hidden')
        self.gui.canvas.itemconfig(self.pause_button, state='hidden')
        self.gui.canvas.itemconfig(self.restart_button, state='hidden')
        self.gui.canvas.itemconfig(self.exit_button, state='hidden')

    def destroy_ui(self) -> None:
        self.gui.canvas.delete(self.stats_background)
        self.gui.canvas.delete(self.clock)
        self.gui.canvas.delete(self.clock_text_bg)
        self.gui.canvas.delete(self.clock_text)
        self.gui.canvas.delete(self.score)
        self.gui.canvas.delete(self.score_text_bg)
        self.gui.canvas.delete(self.score_text)
        self.gui.canvas.delete(self.moves)
        self.gui.canvas.delete(self.moves_text_bg)
        self.gui.canvas.delete(self.moves_text)
        self.gui.canvas.delete(self.pause_button)
        self.gui.canvas.delete(self.restart_button)
        self.gui.canvas.delete(self.exit_button)

class Pause_Screen:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.create_ui()

        self.close_ui()

        self.gui.canvas.tag_bind(self.resume_button, '<Button-1>', lambda event: (self.close_ui(), self.gui.maze.timer.resume_timer()))

    def create_ui(self):
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['pause_background'])
        self.resume_button = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*241//382, image=self.gui.images['resume_button'])

    def open_ui(self):
        self.destroy_ui()
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['pause_background'])
        self.resume_button = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*241//382, image=self.gui.images['resume_button'])
        self.gui.canvas.tag_bind(self.resume_button, '<Button-1>', lambda event: (self.close_ui(), self.gui.maze.timer.resume_timer()))
        # self.gui.canvas.itemconfig(self.ui, state='normal')

    def close_ui(self):
        self.gui.canvas.itemconfig(self.ui, state='hidden')
        self.gui.canvas.itemconfig(self.resume_button, state='hidden')

    def destroy_ui(self):
        self.gui.canvas.delete(self.ui)
        self.gui.canvas.delete(self.resume_button)

class Game_over:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.create_ui()

        self.close_ui()

        def play_again(event):
            self.close_ui()
            self.gui.maze.destroy_ui()
            self.gui.maze = Maze(self.gui)

        self.gui.canvas.tag_bind(self.play_again_button, '<Button-1>', play_again)
        self.gui.canvas.tag_bind(self.exit, '<Button-1>', lambda event: (self.close_ui(), self.gui.maze.destroy_ui(), self.gui.start_screen.open_ui()))

    def create_ui(self):
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['game_over_background'])
        self.play_again_button = self.gui.canvas.create_image(self.gui.window_width*779//1358, self.gui.window_height*241//382, image=self.gui.images['play_again_button'])
        self.exit = self.gui.canvas.create_image(self.gui.window_width*579//1358, self.gui.window_height*241//382, image=self.gui.images['exit_button_game_over'])

    def open_ui(self):
        self.destroy_ui()
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['game_over_background'])
        self.play_again_button = self.gui.canvas.create_image(self.gui.window_width*779//1358, self.gui.window_height*241//382, image=self.gui.images['play_again_button'])
        self.exit = self.gui.canvas.create_image(self.gui.window_width*579//1358, self.gui.window_height*241//382, image=self.gui.images['exit_button_game_over'])

        def play_again(event):
            self.close_ui()
            self.gui.maze.destroy_ui()
            self.gui.maze = Maze(self.gui)

        self.gui.canvas.tag_bind(self.play_again_button, '<Button-1>', play_again)
        self.gui.canvas.tag_bind(self.exit, '<Button-1>', lambda event: (self.close_ui(), self.gui.maze.destroy_ui(), self.gui.start_screen.open_ui()))

    def close_ui(self):
        self.gui.canvas.itemconfig(self.ui, state='hidden')
        self.gui.canvas.itemconfig(self.play_again_button, state='hidden')
        self.gui.canvas.itemconfig(self.exit, state='hidden')

    def destroy_ui(self):
        self.gui.canvas.delete(self.ui)
        self.gui.canvas.delete(self.play_again_button)
        self.gui.canvas.delete(self.exit)
    
class Victory:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.create_ui()

        self.close_ui()

        def play_again(event):
            self.close_ui()
            self.gui.maze.destroy_ui()
            self.gui.maze = Maze(self.gui)

        self.gui.canvas.tag_bind(self.play_again_button, '<Button-1>', play_again)
        self.gui.canvas.tag_bind(self.exit, '<Button-1>', lambda event: (self.close_ui(), self.gui.maze.destroy_ui(), self.gui.start_screen.open_ui()))

    def create_ui(self):
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['victory_bg'])
        self.background = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*15//31 ,image=self.gui.images['leaderstats_background'] )
        self.headding = self.gui.canvas.create_text(self.gui.window_width//2, self.gui.window_height*227//620, text='VICTORY!', font='Helvitica 15 bold', fill='white')
        self.time_text_bg = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*14//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.score_text_bg = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*17//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.time_img = self.gui.canvas.create_image(self.gui.window_width*302//679, self.gui.window_height*14//31, image=self.gui.images['clock'])
        self.score_img = self.gui.canvas.create_image(self.gui.window_width*302//679, self.gui.window_height*17//31, image=self.gui.images['score'])
        self.time_text = self.gui.canvas.create_text(self.gui.window_width*699//1358, self.gui.window_height*14//31+5, text='00:00', font='Helvitica 25 bold', fill='white')
        self.score_text = self.gui.canvas.create_text(self.gui.window_width*699//1358, self.gui.window_height*17//31+5, text='0000', font='Helvitica 25 bold', fill='white')
        self.play_again_button = self.gui.canvas.create_image(self.gui.window_width*779//1358, self.gui.window_height*291//382, image=self.gui.images['play_again_button'])
        self.exit = self.gui.canvas.create_image(self.gui.window_width*579//1358, self.gui.window_height*291//382, image=self.gui.images['exit_button_game_over'])

    def open_ui(self):
        self.destroy_ui()
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['victory_bg'])
        self.background = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*15//31 ,image=self.gui.images['leaderstats_background'] )
        self.headding = self.gui.canvas.create_text(self.gui.window_width//2, self.gui.window_height*227//620, text='VICTORY!', font='Helvitica 15 bold', fill='white')
        self.time_text_bg = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*14//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.score_text_bg = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height*17//31+5, image=self.gui.images['scoreboard_text_bg'])
        self.time_img = self.gui.canvas.create_image(self.gui.window_width*302//679, self.gui.window_height*14//31, image=self.gui.images['clock'])
        self.score_img = self.gui.canvas.create_image(self.gui.window_width*302//679, self.gui.window_height*17//31, image=self.gui.images['score'])
        self.time_text = self.gui.canvas.create_text(self.gui.window_width*699//1358, self.gui.window_height*14//31+5, text='00:00', font='Helvitica 25 bold', fill='white')
        self.score_text = self.gui.canvas.create_text(self.gui.window_width*699//1358, self.gui.window_height*17//31+5, text='0000', font='Helvitica 25 bold', fill='white')
        self.play_again_button = self.gui.canvas.create_image(self.gui.window_width*779//1358, self.gui.window_height*291//382, image=self.gui.images['play_again_button'])
        self.exit = self.gui.canvas.create_image(self.gui.window_width*579//1358, self.gui.window_height*291//382, image=self.gui.images['exit_button_game_over'])

        self.gui.canvas.itemconfig(self.time_text, text=f'{Time//60:02}:{Time-(Time//60)*60:02}')
        self.gui.canvas.itemconfig(self.score_text, text=f'{self.gui.maze.score:04}')

        def play_again(event):
            self.close_ui()
            self.gui.maze.destroy_ui()
            self.gui.maze = Maze(self.gui)

        self.gui.canvas.tag_bind(self.play_again_button, '<Button-1>', play_again)
        self.gui.canvas.tag_bind(self.exit, '<Button-1>', lambda event: (self.close_ui(), self.gui.maze.destroy_ui(), self.gui.start_screen.open_ui()))

    def close_ui(self):
        self.gui.canvas.itemconfig(self.ui, state='hidden')
        self.gui.canvas.itemconfig(self.background, state='hidden')
        self.gui.canvas.itemconfig(self.headding, state='hidden')
        self.gui.canvas.itemconfig(self.time_text_bg, state='hidden')
        self.gui.canvas.itemconfig(self.score_text_bg, state='hidden')
        self.gui.canvas.itemconfig(self.time_img, state='hidden')
        self.gui.canvas.itemconfig(self.score_img, state='hidden')
        self.gui.canvas.itemconfig(self.time_text, state='hidden')
        self.gui.canvas.itemconfig(self.score_text, state='hidden')
        self.gui.canvas.itemconfig(self.play_again_button, state='hidden')
        self.gui.canvas.itemconfig(self.exit, state='hidden')

    def destroy_ui(self):
        self.gui.canvas.delete(self.ui)
        self.gui.canvas.delete(self.background)
        self.gui.canvas.delete(self.headding)
        self.gui.canvas.delete(self.time_text_bg)
        self.gui.canvas.delete(self.score_text_bg)
        self.gui.canvas.delete(self.time_img)
        self.gui.canvas.delete(self.score_img)
        self.gui.canvas.delete(self.time_text)
        self.gui.canvas.delete(self.score_text)
        self.gui.canvas.delete(self.play_again_button)
        self.gui.canvas.delete(self.exit)

class Credits:
    def __init__(self, gui) -> None:
        self.gui = gui

        self.create_ui()

        self.close_ui()

        self.gui.canvas.tag_bind(self.ui, '<Button-1>', lambda event: (self.close_ui(), self.gui.start_screen.open_ui()))

    def create_ui(self):
        self.ui = self.gui.canvas.create_image(self.gui.window_width//2, self.gui.window_height//2, image=self.gui.images['credits_background'])

    def open_ui(self):
        self.gui.canvas.itemconfig(self.ui, state='normal')

    def close_ui(self):
        self.gui.canvas.itemconfig(self.ui, state='hidden')

    def destroy_ui(self):
        self.gui.canvas.delete(self.ui)

class Gui:
    def __init__(self, user_data) -> None:
        self.user_data = user_data

        self.create_root_ui()

        self.create_bg()

        self.create_ui()
    
    def create_images(self):
        self.images = dict()
        font1 = ImageFont.truetype("c:\windows\Fonts\ARLRDBD.TTF", self.window_width*30//679)
        font2 = ImageFont.truetype("c:\windows\Fonts\ARLRDBD.TTF", self.window_width*15//679)

        self.images['background_img'] = ImageTk.PhotoImage(Image.open('app_data/Background.png').resize((self.window_width, self.window_height)))

        self.images['home_screen_button1'] = Image.open('app_data/Home Screen Button.png').resize((self.window_width//5, self.window_height//5))
        ImageDraw.Draw(self.images['home_screen_button1']).text((self.window_width//10, self.window_height//10), 'Play', font=font1, fill='white', anchor='mm')
        self.images['home_screen_button1'] = ImageTk.PhotoImage(self.images['home_screen_button1'])

        self.images['home_screen_button2'] = Image.open('app_data/Home Screen Button.png').resize((self.window_width//5, self.window_height//5))
        ImageDraw.Draw(self.images['home_screen_button2']).text((self.window_width//10, self.window_height//10), 'Score', font=font1, fill='white', anchor='mm')
        self.images['home_screen_button2'] = ImageTk.PhotoImage(self.images['home_screen_button2'])

        self.images['home_screen_button3'] = Image.open('app_data/Home Screen Button.png').resize((self.window_width//5, self.window_height//5))
        ImageDraw.Draw(self.images['home_screen_button3']).text((self.window_width//10, self.window_height//10), 'Settings', font=font1, fill='white', anchor='mm')
        self.images['home_screen_button3'] = ImageTk.PhotoImage(self.images['home_screen_button3'])

        self.images['home_screen_button4'] = Image.open('app_data/Home Screen Button.png').resize((self.window_width//5, self.window_height//5))
        ImageDraw.Draw(self.images['home_screen_button4']).text((self.window_width//10, self.window_height//10), 'Credits', font=font1, fill='white', anchor='mm')
        self.images['home_screen_button4'] = ImageTk.PhotoImage(self.images['home_screen_button4'])
        
        self.images['settings_img'] = Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 128))
        ImageDraw.Draw(self.images['settings_img']).rounded_rectangle((self.window_width*7//18, self.window_height*5//14, self.window_width*11//18, self.window_height*9//14), fill=(0, 0, 0, 200), width=0, radius=20)
        self.images['settings_img'] = ImageTk.PhotoImage(self.images['settings_img'])

        self.images['sound_image'] = ImageTk.PhotoImage(Image.open('app_data/Sound Image.png').resize((self.window_height//11, self.window_height//11)))

        self.images['music_image'] = ImageTk.PhotoImage(Image.open('app_data/Music Image.png').resize((int(self.window_height//(12*1400/1102)), self.window_height//12)))

        self.images['save_button'] = Image.new('RGBA', ((self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['save_button'])
        img.rounded_rectangle((0, 0, (self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text(((self.window_width//2 - self.window_width//14)//8 - 2, self.window_height//22), 'Save', font=font2, fill='white', anchor='mm')
        self.images['save_button'] = ImageTk.PhotoImage(self.images['save_button'])

        self.images['cancel_button'] = Image.new('RGBA', ((self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['cancel_button'])
        img.rounded_rectangle((0, 0, (self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text(((self.window_width//2 - self.window_width//14)//8 - 2, self.window_height//22), 'cancel', font=font2, fill='white', anchor='mm')
        self.images['cancel_button'] = ImageTk.PhotoImage(self.images['cancel_button'])

        self.images['stats_background'] = Image.new('RGBA', (self.window_width//5, self.window_height//2), (0, 0, 0, 0))
        ImageDraw.Draw(self.images['stats_background']).rounded_rectangle((0, 0, self.window_width//5, self.window_height//2), fill=(9, 88, 172, 128), width=0, radius=20)
        self.images['stats_background'] = ImageTk.PhotoImage(self.images['stats_background'])

        self.images['clock'] = ImageTk.PhotoImage(Image.open('app_data/Clock.png').resize((self.window_height//12, self.window_height*1559//(12*1400))))

        self.images['score'] = ImageTk.PhotoImage(Image.open('app_data/Score.png').resize((self.window_height//12, self.window_height*1341//(12*1400))))
        
        self.images['moves'] = ImageTk.PhotoImage(Image.open('app_data/Moves.png').resize((self.window_height//12, self.window_height*1135//(12*1400))))

        self.images['scoreboard_text_bg'] = ImageTk.PhotoImage(Image.open('app_data/Gradient Two.png').resize((self.window_height//4, self.window_height*1341//(12*1400))))

        self.images['pause_button'] = ImageTk.PhotoImage(Image.open('app_data/Pause Button.png').resize((self.window_height//12, self.window_height//12)))

        self.images['restart_button'] = ImageTk.PhotoImage(Image.open('app_data/Restart Button.png').resize((self.window_height*1400//(12*1251), self.window_height//12)))

        self.images['exit_button'] = ImageTk.PhotoImage(Image.open('app_data/Exit Button.png').resize((self.window_height*1400//(12*1633), self.window_height//12)))
        
        self.images['choose_mode_img'] = Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 128))
        img = ImageDraw.Draw(self.images['choose_mode_img'])
        img.rounded_rectangle((self.window_width*7//18, self.window_height*5//14, self.window_width*11//18, self.window_height*9//14), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text((self.window_width//2, self.window_height*4//14 + 10), 'Choose Mode', font=font2, fill='white', anchor='mm')
        self.images['choose_mode_img'] = ImageTk.PhotoImage(self.images['choose_mode_img'])

        self.images['start_button'] = Image.new('RGBA', ((self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['start_button'])
        img.rounded_rectangle((0, 0, (self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text(((self.window_width//2 - self.window_width//14)//8 - 2, self.window_height//22), 'Start', font=font2, fill='white', anchor='mm')
        self.images['start_button'] = ImageTk.PhotoImage(self.images['start_button'])

        self.images['back_button'] = Image.new('RGBA', ((self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['back_button'])
        img.rounded_rectangle((0, 0, (self.window_width//2 - self.window_width//14)//4 - 10, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text(((self.window_width//2 - self.window_width//14)//8 - 2, self.window_height//22), 'Back', font=font2, fill='white', anchor='mm')
        self.images['back_button'] = ImageTk.PhotoImage(self.images['back_button'])

        self.images['easy_button_white'] = Image.new('RGBA', (self.window_width*2//9, 80), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['easy_button_white'])
        img.rounded_rectangle((0, 0, self.window_width*2//9 - 80, 40), fill=(255, 255, 255, 128), width=0, radius=20)
        img.text((self.window_width//9 - 40, 20), 'Easy', font=font2, fill='white', anchor='mm')
        self.images['easy_button_white'] = ImageTk.PhotoImage(self.images['easy_button_white'])

        self.images['medium_button_white'] = Image.new('RGBA', (self.window_width*2//9, 80), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['medium_button_white'])
        img.rounded_rectangle((0, 0, self.window_width*2//9 - 80, 40), fill=(255, 255, 255, 128), width=0, radius=20)
        img.text((self.window_width//9 - 40, 20), 'Medium', font=font2, fill='white', anchor='mm')
        self.images['medium_button_white'] = ImageTk.PhotoImage(self.images['medium_button_white'])

        self.images['hard_button_white'] = Image.new('RGBA', (self.window_width*2//9, 80), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['hard_button_white'])
        img.rounded_rectangle((0, 0, self.window_width*2//9 - 80, 40), fill=(255, 255, 255, 128), width=0, radius=20)
        img.text((self.window_width//9 - 40, 20), 'Hard', font=font2, fill='white', anchor='mm')
        self.images['hard_button_white'] = ImageTk.PhotoImage(self.images['hard_button_white'])

        self.images['easy_button_blue'] = Image.new('RGBA', (self.window_width*2//9, 80), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['easy_button_blue'])
        img.rounded_rectangle((0, 0, self.window_width*2//9 - 80, 40), fill=(9, 88, 172, 128), width=0, radius=20)
        img.text((self.window_width//9 - 40, 20), 'Easy', font=font2, fill='white', anchor='mm')
        self.images['easy_button_blue'] = ImageTk.PhotoImage(self.images['easy_button_blue'])

        self.images['medium_button_blue'] = Image.new('RGBA', (self.window_width*2//9, 80), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['medium_button_blue'])
        img.rounded_rectangle((0, 0, self.window_width*2//9 - 80, 40), fill=(9, 88, 172, 128), width=0, radius=20)
        img.text((self.window_width//9 - 40, 20), 'Medium', font=font2, fill='white', anchor='mm')
        self.images['medium_button_blue'] = ImageTk.PhotoImage(self.images['medium_button_blue'])

        self.images['hard_button_blue'] = Image.new('RGBA', (self.window_width*2//9, 80), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['hard_button_blue'])
        img.rounded_rectangle((0, 0, self.window_width*2//9 - 80, 40), fill=(9, 88, 172, 128), width=0, radius=20)
        img.text((self.window_width//9 - 40, 20), 'Hard', font=font2, fill='white', anchor='mm')
        self.images['hard_button_blue'] = ImageTk.PhotoImage(self.images['hard_button_blue'])

        self.images['clock_maze_e'] = ImageTk.PhotoImage(Image.open('app_data/Clock.png').resize(((self.window_height - 200)*1400//(10*1559), (self.window_height - 200)//10)))
        self.images['clock_maze_m'] = ImageTk.PhotoImage(Image.open('app_data/Clock.png').resize(((self.window_height - 200)*1400//(15*1559), (self.window_height - 200)//15)))
        self.images['clock_maze_h'] = ImageTk.PhotoImage(Image.open('app_data/Clock.png').resize(((self.window_height - 200)*1400//(20*1559), (self.window_height - 200)//20)))
        
        self.images['coin_maze_e'] = ImageTk.PhotoImage(Image.open('app_data/Coin.png').resize(((self.window_height - 200)*1920//(10*1642), (self.window_height - 200)//10)))
        self.images['coin_maze_m'] = ImageTk.PhotoImage(Image.open('app_data/Coin.png').resize(((self.window_height - 200)*1920//(15*1642), (self.window_height - 200)//15)))
        self.images['coin_maze_h'] = ImageTk.PhotoImage(Image.open('app_data/Coin.png').resize(((self.window_height - 200)*1920//(20*1642), (self.window_height - 200)//20)))
        
        self.images['crown_maze_e'] = ImageTk.PhotoImage(Image.open('app_data/Crown.png').resize(((self.window_height - 200)*1400//(10*981), (self.window_height - 200)//10)))
        self.images['crown_maze_m'] = ImageTk.PhotoImage(Image.open('app_data/Crown.png').resize(((self.window_height - 200)*1400//(15*981), (self.window_height - 200)//15)))
        self.images['crown_maze_h'] = ImageTk.PhotoImage(Image.open('app_data/Crown.png').resize(((self.window_height - 200)*1400//(20*981), (self.window_height - 200)//20)))

        self.images['leaderstats_background'] = Image.new('RGBA', (self.window_width//5, self.window_height//3), (0, 0, 0, 0))
        ImageDraw.Draw(self.images['leaderstats_background']).rounded_rectangle((0, 0, self.window_width//5, self.window_height//3), fill=(9, 88, 172, 128), width=0, radius=20)
        self.images['leaderstats_background'] = ImageTk.PhotoImage(self.images['leaderstats_background'])
        
        self.images['stats_background_bg'] = ImageTk.PhotoImage(Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 128)))

        self.images['maze_bg'] = Image.new('RGBA', (self.window_height - 20, self.window_height - 20), (0, 0, 0, 0))
        ImageDraw.Draw(self.images['maze_bg']).rounded_rectangle((0, 0, self.window_height - 20, self.window_height - 20), fill=(9, 88, 172, 200), outline='white', width=2, radius=20)
        self.images['maze_bg'] = ImageTk.PhotoImage(self.images['maze_bg'])

        self.images['credits_background'] = Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 128))
        img = ImageDraw.Draw(self.images['credits_background'])
        img.rounded_rectangle((self.window_width*279//1358, self.window_height*41//382, self.window_width*1079//1358, self.window_height*341//382),fill=(255, 255, 255, 128), width=0, radius=20)
        img.text((self.window_width//2, self.window_height*28//191), 'Credits', font=font2, fill='black', anchor='mm')
        img.text((self.window_width*47//194, self.window_height*38//191), 'Pushkar\n   Maze generation\n   Maze visualization\n   rewards\n   Start Menu\n   Settings', font=font2, fill='black')
        img.text((self.window_width//2, self.window_height*38//191), 'Preetham\n   Save and load\n   Scoreboard\n   Sound effects and music', font=font2, fill='black')
        img.text((self.window_width*47//194, self.window_height*113//191), 'Sukesh\n   Leaderboard\n   Credits page', font=font2, fill='black')
        img.text((self.window_width//2 , self.window_height*113//191), 'Prajwal\n   Timer\n   Pause / resume\n   restart', font=font2, fill='black')
        self.images['credits_background'] = ImageTk.PhotoImage(self.images['credits_background'])
        
        self.images['pause_background'] = Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 200))
        ImageDraw.Draw(self.images['pause_background']).text((self.window_width//2, self.window_height//2), 'Game Paused', font=font1, fill='white', anchor='mm')
        self.images['pause_background'] = ImageTk.PhotoImage(self.images['pause_background'])

        self.images['resume_button'] = Image.new('RGBA', ((self.window_width//2 - self.window_width//14)//4, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['resume_button'])
        img.rounded_rectangle((0, 0, (self.window_width//2 - self.window_width//14)//4, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text(((self.window_width//2 - self.window_width//14)//8, self.window_height//22), 'Resume', font=font2, fill='white', anchor='mm')
        self.images['resume_button'] = ImageTk.PhotoImage(self.images['resume_button'])
        
        self.images['game_over_background'] = Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 200))
        ImageDraw.Draw(self.images['game_over_background']).text((self.window_width//2, self.window_height//2), 'Game Over!', font=font1, fill='white', anchor='mm')
        self.images['game_over_background'] = ImageTk.PhotoImage(self.images['game_over_background'])

        self.images['exit_button_game_over'] = Image.new('RGBA', (self.window_width//8, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['exit_button_game_over'])
        img.rounded_rectangle((0, 0, self.window_width//8, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text((self.window_width//16, self.window_height//22), 'Exit', font=font2, fill='white', anchor='mm')
        self.images['exit_button_game_over'] = ImageTk.PhotoImage(self.images['exit_button_game_over'])

        self.images['play_again_button'] = Image.new('RGBA', (self.window_width//8, self.window_height//11), (0, 0, 0, 0))
        img = ImageDraw.Draw(self.images['play_again_button'])
        img.rounded_rectangle((0, 0, self.window_width//8, self.window_height//11), fill=(0, 0, 0, 200), width=0, radius=20)
        img.text((self.window_width//16, self.window_height//22), 'Play Again', font=font2, fill='white', anchor='mm')
        self.images['play_again_button'] = ImageTk.PhotoImage(self.images['play_again_button'])

        self.images['victory_bg'] = ImageTk.PhotoImage(Image.new('RGBA', (self.window_width, self.window_height), (0, 0, 0, 200)))

    def create_root_ui(self) -> None:
        self.root = tkinter.Tk()
        self.root.title('Rat in Maze')
        self.root.iconbitmap('app_data/Logo.ico')

        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        self.window_height = int(self.screen_height - 100)
        self.window_width = int(self.window_height*1920/1080)

        self.create_images()

        self.root.geometry(f'{self.window_width}x{self.window_height}+{(self.screen_width - self.window_width)//2}+{(self.screen_height - self.window_height)//2 - 40}')
        self.root.resizable(False, False)

        self.canvas = tkinter.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack()
    
    def create_bg(self) -> None:
        self.background_img = self.canvas.create_image(self.window_width//2, self.window_height//2, image=self.images['background_img'])

    def create_ui(self) -> None:
        self.start_screen = Start_screen(self)
        self.settings = Settings(self)
        self.choose_mode = Choose_mode(self)
        self.leaderboard = Leaderboard(self)
        self.credits = Credits(self)
        self.pause_screen = Pause_Screen(self)
        self.game_over = Game_over(self)
        self.victory = Victory(self)
        self.sounds = Sounds(self)

class Main:
    def __init__(self) -> None:
        self.user_data = User_data()
        self.gui = Gui(self.user_data)

        def move(direction):
            try:
                self.gui.maze.button_clicked(direction=direction)
            except:
                pass

        keyboard.on_press_key("left arrow", lambda _: move('left'))
        keyboard.on_press_key("right arrow", lambda _: move('right'))
        keyboard.on_press_key("up arrow", lambda _: move('top'))
        keyboard.on_press_key("down arrow", lambda _: move('bot'))
        keyboard.on_press_key("a", lambda _: move('left'))
        keyboard.on_press_key("d", lambda _: move('right'))
        keyboard.on_press_key("w", lambda _: move('top'))
        keyboard.on_press_key("s", lambda _: move('bot'))

        self.gui.root.mainloop()
        self.user_data.save_user_data()
        try:
            self.gui.maze.timer.stop_timer()
        except:
            pass

    def initilize_data(self) -> None:
        pass

    def create_root_ui(self) -> None:
        pass

Main()