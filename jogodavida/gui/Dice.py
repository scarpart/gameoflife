from tkinter import *
from tkinter import ttk
from random import randint
from constants import LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA

class Dice:
    def __init__(self, canvas, frame, command):
        self.__canvas = canvas
        self.__frame = frame
        self.__command = command
        self.__create_roll_btn()
        self.__number = 6

    def get_number(self) -> int:
        return self.__number

    def __create_roll_btn(self):
        style = ttk.Style()
        style.configure("Dice.TButton", bordercolor="black", borderwidth=4, relief="groove",
                        font=("Arial", 10, "bold"), background="white")
        style.layout("Dice.TButton",
                     [('Button.border', {'sticky': 'nswe', 'border': '1', 'children':
                         [('Button.padding', {'sticky': 'nswe', 'border': '1', 'children':
                             [('Button.label', {'sticky': 'nswe'})]})]})])

        self.roll_btn = ttk.Button(self.__frame, text="Roll Dice",
                                    command=self.__command, style="Dice.TButton", cursor="hand2")

    def roll(self):
        return randint(1, 6)

    def draw(self, number):
        self.__number = number
        centro_x, centro_y = LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2
        lado = LARGURA_CASA
        meio_lado = lado // 2
        raio = LARGURA_CASA // 8
        dist_multiplier = 2

        self.erase()

        self.dado_rectangle = self.__canvas.create_rectangle(centro_x - meio_lado, centro_y - meio_lado, centro_x + meio_lado, centro_y + meio_lado, fill="white", outline="black")

        pontos = {
            1: [(0, 0)],
            2: [(-1, -1), (1, 1)],
            3: [(-1, -1), (0, 0), (1, 1)],
            4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
            6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        }

        self.dado_ovals = []
        for dx, dy in pontos[number]:
            x = centro_x + dx * raio * dist_multiplier
            y = centro_y + dy * raio * dist_multiplier
            oval = self.__canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="black")
            self.dado_ovals.append(oval)

    def erase(self):
        if hasattr(self, 'dado_rectangle'):
            self.__canvas.delete(self.dado_rectangle)
        if hasattr(self, 'dado_ovals'):
            for oval in self.dado_ovals:
                self.__canvas.delete(oval)
            self.dado_ovals = []

    def hide_roll_btn(self):
        self.roll_btn.place_forget()

    def show_roll_btn(self):
        self.roll_btn.place(x=LARGURA_TABULEIRO // 2 - self.roll_btn.winfo_reqwidth() // 2,
                            y=ALTURA_TABULEIRO // 2 + LARGURA_CASA)