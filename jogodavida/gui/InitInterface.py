from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

from PIL import Image, ImageTk
from constants import INIT_HEIGHT, INIT_WIDTH

class InitInterface:
    def __init__(self, master):
        self.__master = master

        self.image = Image.open("media/initpage.jpg")  

        self.image = self.image.resize((INIT_WIDTH, INIT_HEIGHT), Image.ANTIALIAS) 
        self.photo_image = ImageTk.PhotoImage(self.image)

        self.__master.geometry(f"{INIT_WIDTH}x{INIT_HEIGHT}") 

        self.frame = Frame(self.__master)
        self.frame.pack(fill="both", expand=True)

        self.__canvas = Canvas(self.frame, width=INIT_WIDTH, height=INIT_HEIGHT)
        self.__canvas.pack(fill="both", expand=True)
        self.__canvas.create_image(0, 0, image=self.photo_image, anchor="nw")

        self.button = Button(self.frame, text="Play", font=("Arial", 20, "bold"), fg="#FFFFFF", bg="#198754", activebackground="#4cae4c", activeforeground="#FFFFFF", cursor="hand2", padx=10, pady=10)
        self.button.pack(side="bottom", pady=20)
        self.button.place(relx=0.5, rely=0.55, anchor="center")

    def get_player_name(self) -> str:
        player_name = "" 
        while True:
            player_name = simpledialog.askstring("Input", "Enter your name.", parent=self.__master)
            # Check if the name is not null
            if player_name: 
                break
            messagebox.showerror("Invalid input", "Your username cannot be null. Please enter a valid username.")
        # self.__player_name = player_name
        return player_name