from tkinter import *
import tkinter as tk
from gui.Board import Board
from gui.Dice import Dice
from gui.RightFrame import RightFrame
from constants import LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA

class GameInterface:    
    def __init__(self, master, player_name, players, game):
        self.master = master
        self.master.geometry(f"{LARGURA_TABULEIRO+300}x{ALTURA_TABULEIRO}")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.__game = game

        self.__create_canvas()
        self.__board = Board(self.__canvas, self.__game)
        self.__game.set_board(self.__board)
        self.player_name = player_name
        
        self.__dice = Dice(self.__canvas, self.frame, command=lambda: self.__game.handle_dice_roll())
        self.__game.set_players(players)
        self.__game.set_dice(self.__dice)
        self.__players = self.__game.get_players() # FIXME: desacoplar players daqui?

        self.__create_player_text()
        self.__create_current_player_text()
        self.__create_game_title()

        self.__board.draw_players(self.__players)
        self.right_frame = RightFrame(self.frame, 300, ALTURA_TABULEIRO, self.__game.get_players())
        self.__dice.draw(1) # Só para ter algo ali
        self.__dice.show_roll_btn()

    def __create_canvas(self):
        self.__canvas = tk.Canvas(self.frame, width=LARGURA_TABULEIRO, height=ALTURA_TABULEIRO, bg='white')
        self.__canvas.pack(side="left")

    def __create_right_frame(self):
        self.right_frame = tk.Canvas(self.frame, width=300, height=ALTURA_TABULEIRO, bg='white')
        self.right_frame.pack(side="right")

    def __create_player_text(self):
        self.player_text = self.__canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 10, 
                                                    text=f"#{self.player_name}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")
        
    def update_current_player_text(self):
        self.__canvas.delete(self.current_player_text)
        current_player = self.__game.get_player_turn()
        self.current_player_text = self.__canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 30,
                                                    text=f"Current player: {current_player.get_player_name()}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")

    def __create_current_player_text(self):
        current_player = self.__game.get_player_turn()
        self.current_player_text = self.__canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 30,
                                                        text=f"Current player: {current_player.get_player_name()}", anchor="nw",
                                                        font=("Arial", 16, "bold"), fill="#172934") 

    def __create_game_title(self):
        self.__canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

    def refresh_ui(self):
        self.right_frame.update_cards(self.__game.get_players())
        # self.toggle_dice_visibility() # TODO: wtf?
        self.__dice.draw(self.__game.get_dice().get_number())

        for player in self.__game.get_players():
            self.__board.update_player_position(player)
    