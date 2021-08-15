# Importing Required Modules & libraries
from tkinter import *
import pygame
from mutagen.mp3 import MP3
from tkinter import ttk
from PIL import ImageTk, Image, ImageSequence
import os
import time
# Defining MusicPlayer Class
class Player(Frame):

  # Defining Constructor
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()
        
        self.current = 0
        self.vol=0
        self.paused = True
        self.played = False
        
        # Creating Track Frame for Song label & status label
        self.trackframe = LabelFrame(self, text='Song Track', 
                        font=("times new roman",15,"bold"),
                        bg="grey",fg="white",bd=5,relief=GROOVE)
        self.trackframe.config(width=400,height=400)
        self.trackframe.grid(row=0, column=0, padx=10)
        self.songtrack = Label(self.trackframe,textvariable=self.track,font=("times new roman",18,"bold"),fg="black")
        self.songtrack.config(width=30, height=1)
        self.songtrack.grid(row=1,column=0)
       
        
        
        # Inserting Status Label
        self.trackstatus = Label(self.trackframe,textvariable=self.status,font=("times new roman",18,"bold"),fg="black")
        self.trackstatus.config(width=10, height=1)
        self.trackstatus.grid(row=1,column=1)
        
      

        # Creating Button Frame
        self.buttonframe = LabelFrame(self,
                                font=("times new roman",15,"bold"),
                                bg="white",fg="white",bd=2,relief=GROOVE)
        self.buttonframe.config(width=400,height=80)
        self.buttonframe.grid(row=1, column=0, pady=5, padx=10)
        
        
        self.my_slider = ttk.Scale(self,from_=0,to=100,orient=HORIZONTAL,value=0,length=360)
        self.my_slider['command']=self.slide
        self.my_slider.grid(row=3,column=0)
        
        self.status_bar = Label(self, text='', bd=1, relief=GROOVE, anchor=E)
        self.status_bar.grid(row=3,column=1)
        # Inserting Pause Button
        self.pause = Button(self.buttonframe, image=pause,borderwidth=0)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)
        
        
        
        self.prev = Button(self.buttonframe, image=prev,borderwidth=0)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)
        
        self.next = Button(self.buttonframe, image=nextt,borderwidth=0)
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)
        # Creating Playlist Frame
        self.songsframe = LabelFrame(self, text='PlayList -',
                                font=("times new roman",15,"bold"),
                                bg="grey",fg="white",bd=5,relief=GROOVE)
        self.songsframe.config(width=200,height=400)
        self.songsframe.grid(row=0, column=1, rowspan=3, pady=5)
        # Inserting scrollbar
        scrol_y = Scrollbar(self.songsframe,orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(self.songsframe,yscrollcommand=scrol_y.set,selectbackground="gold",selectmode=SINGLE,font=("times new roman",12,"bold"),bd=5,relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        os.chdir("C:/Users/lenovo/Desktop/EMOPlayer/songs")
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
          self.playlist.insert(END,track)

        self.canvas = Canvas(self.trackframe)
        
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0,column=0,columnspan=3)
        self.sequence = [ImageTk.PhotoImage(img)
                            for img in ImageSequence.Iterator(
                                    Image.open(
                                    r'C:/Users/lenovo/Desktop/EMOPlayer/Buttons/equaliser.gif'))]
        self.image = self.canvas.create_image(200,200, image=self.sequence[0])
        self.animate(1)
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        self.after(60, lambda: self.animate((counter+1) % len(self.sequence)))
        # Inserting Song Track Label
    
    def slide(self,x):
        song = self.playlist.get(ACTIVE)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0,start=int(self.my_slider.get()))
    def play_time(self):
        
        current_time = pygame.mixer.music.get_pos() / 1000

       
        converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

        song = self.playlist.get(ACTIVE)
        
        song_mut = MP3(song)
        # Get song Length
        global song_length
        song_length = song_mut.info.length
        # Convert to Time Format
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

       
        current_time +=1
        pygame.mixer.music.set_volume(0.4)
        if int(self.my_slider.get()) == int(song_length):
            self.status_bar.config(text=f'Time Elapsed: {converted_song_length}  ')
            
        elif self.paused==True:
            
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(self.my_slider.get())))
            
            
              
            # Output time to status bar
            self.status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')
            
            pygame.mixer.music.set_volume(0)
            pygame.mixer.music.pause()
        
            
            
            
          
                
        
        elif int(self.my_slider.get()) == int(current_time):
            # Update Slider To position
            
                
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(current_time))
            
               

        else:
           
            
            slider_position = int(song_length)
            self.my_slider.config(to=slider_position, value=int(self.my_slider.get()))
            
            
            converted_current_time = time.strftime('%M:%S', time.gmtime(int(self.my_slider.get())))

           
            self.status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

           
            next_time = int(self.my_slider.get()) + 1
            self.my_slider.config(value=next_time)
           
        self.status_bar.after(1000, self.play_time)       
            
        
        
        
        
        
  # Defining Play Song Function
    def play_song(self):
    # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        self.pause['image'] = play
        self.paused = False
        self.played = True
        # Playing Selected Song
        pygame.mixer.music.play()
        self.play_time()
        #
        
       
    

      
        
    def next_song(self):
        self.status_bar.config(text='')
        self.my_slider.config(value=0)
        
        next_song = self.playlist.curselection()
        
        next_song = next_song[0]+1
        
        song = self.playlist.get(next_song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.track.set(song)
        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.status.set('-Playing')
        self.playlist.selection_clear(0,END) 
        self.playlist.activate(next_song)
        #self.playlist.selection_set(next_song) 
        self.playlist.selection_set(next_song, last=None)
        
        
    def prev_song(self):
        self.status_bar.config(text='')
        self.my_slider.config(value=0)
        next_song = self.playlist.curselection()
        next_song = next_song[0]-1
        song = self.playlist.get(next_song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.track.set(song)
        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.status.set('-Playing')
        self.playlist.selection_clear(0,END) 
        self.playlist.activate(next_song)
        #self.playlist.selection_set(next_song)
        self.playlist.selection_set(next_song, last=None)
        
        
    def pause_song(self):
        if not self.paused:
            self.paused = True
            pygame.mixer.music.pause()
            self.pause['image'] = pause
            self.status.set("-Paused")
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            pygame.mixer.music.unpause()
            self.pause['image'] = play
            self.status.set('-Playing')
# Creating TK Container
root = Tk()

root.geometry('800x400')
root.wm_title('Music Player')

nextt_img = Image.open('C:/Users/lenovo/Desktop/EMOPlayer/Buttons/forward.png')
nextt_img = nextt_img.resize((50,50),Image.ANTIALIAS)
nextt = ImageTk.PhotoImage(nextt_img)

prev_img = Image.open('C:/Users/lenovo/Desktop/EMOPlayer/Buttons/back.png')
prev_img = prev_img.resize((50,50),Image.ANTIALIAS)
prev = ImageTk.PhotoImage(prev_img)

pause_img  =Image.open('C:/Users/lenovo/Desktop/EMOPlayer/Buttons/pause.png')
pause_img = pause_img.resize((50,50),Image.ANTIALIAS)
pause = ImageTk.PhotoImage(pause_img)

play_img =Image.open('C:/Users/lenovo/Desktop/EMOPlayer/Buttons/play.png')
play_img = play_img.resize((50,50),Image.ANTIALIAS)
play = ImageTk.PhotoImage(play_img)


app = Player(master=root)
app.mainloop()
