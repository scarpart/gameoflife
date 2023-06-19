from tkinter import *
from PIL import Image, ImageTk
from Square import Square
from constants import LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates

CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]

class Board:
    def __init__(self, canvas, game):
        self.__canvas = canvas
        self.__game = game
        self.__squares = []
        self.__draw_board_spaces()

    def get_canvas(self):
        return self.__canvas

    def __draw_board_spaces(self):
        for i in list(range(0, 10)) + list(range(10, 20)) + list(range(20, 30)) + list(range(30, 36)):
            x, y = get_board_house_coordinates(i)
            cor = CORES[i % len(CORES)]
            subcor = LIGHT_CORES[i % len(LIGHT_CORES)]

            center_x = x + LARGURA_CASA / 2
            center_y = y + LARGURA_CASA / 2
            self.__squares.append(Square(i-1))

            if i == 0:
                self.__canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#53c7f8", outline="black")
                self.arrow_image = ImageTk.PhotoImage(Image.open("media/right-arrow-resized.png"))
                self.__canvas.create_image(center_x, center_y, image=self.arrow_image)

            else:
                self.__canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=cor, outline="black")
                self.__canvas.create_text(center_x, center_y, text=str(i+1), fill=subcor, font=("Arial", 12, "bold"))
    
    def draw_players(self, players):
        raio = LARGURA_CASA // 6

        for i, player in enumerate(players):
            x, y = get_board_house_coordinates(player.get_position())

            x += (LARGURA_CASA / 2) - raio
            if i == 0:
                y += ((LARGURA_CASA) / 10)
            elif i == 1:
                y += (LARGURA_CASA / 2) - raio
            elif i == 2:
               y += ((9 * LARGURA_CASA) / 10) - (2 * raio)
            char = self.draw_player(x, y, player.get_colour(), raio)
            player.set_char(char)

    def draw_player(self, x, y, cor, raio):
        centro_x, centro_y = x + raio, y + raio
        pino = self.__canvas.create_oval(centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio, fill=cor)
        return pino

    def update_player_position(self, player):
        raio = LARGURA_CASA // 6
        x, y = get_board_house_coordinates(player.get_position())
        i = self.__game.get_players().index(player)
        
        x += (LARGURA_CASA / 2) - raio
        if i == 0:
            y += ((LARGURA_CASA) / 10)
        elif i == 1:
            y += (LARGURA_CASA / 2) - raio
        elif i == 2:
           y += ((9 * LARGURA_CASA) / 10) - (2 * raio) 
       
        centro_x, centro_y = x + raio, y + raio
        self.__canvas.coords(player.get_char(), centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio)

    def get_canvas(self):
        return self.__canvas

    def get_active_squares(self) -> list:
        # "active squares" = do segundo ao penúltimo (somente aqueles nos quais podemos colocar propriedade)
        return self.__squares[2:]
    
    def get_squares(self) -> list:
        return self.__squares
    
    def get_square_by_position(self, position : int) -> Square:
        return self.__squares[position]