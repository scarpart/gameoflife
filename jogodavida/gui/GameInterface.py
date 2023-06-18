from tkinter import *
import tkinter as tk
from components.CustomDialog import CustomDialog
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

        self.game = game

        # self._create_menu()
        self._create_canvas()

        self.board = Board(self.canvas, self.game)
        self.game.set_board(self.board)

        self.player_name = player_name
        
        self.dice = Dice(self.canvas, self.frame, command=lambda: self.game.handle_dice_roll())
        self.game.set_players(players)
        self.game.set_dice(self.dice)
        self.players = self.game.get_players() # FIXME: desacoplar players daqui?

        self._create_player_text()
        self._create_current_player_text()
        self._create_game_title()

        self.board.draw_players(self.players)
        self.right_frame = RightFrame(self.frame, 300, ALTURA_TABULEIRO, self.game.players)
        self.dice.draw(1) # Só para ter algo ali
        self.dice.show_roll_btn()
        # self.toggle_dice_visibility()
        
    def toggle_dice_visibility(self):
        # TODO: find_player? wtf? what game is this?
        on_hold_player = self.game.find_player(self.player_name)
        
        if on_hold_player == self.game.player_turn:
            self.dice.show_roll_btn()
        else:
            self.dice.hide_roll_btn()

    # def _create_menu(self):
    #     self.menubar = Menu(self.master)
    #     self.menubar.option_add('*tearOff', FALSE)
    #     self.master['menu'] = self.menubar

    #     self.menu_file = Menu(self.menubar)
    #     self.menubar.add_cascade(menu=self.menu_file, label='File')

    #     self.menu_file.add_command(label='Restaurar estado inicial', command=self.start_game)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.frame, width=LARGURA_TABULEIRO, height=ALTURA_TABULEIRO, bg='white')
        self.canvas.pack(side="left")

    def _create_right_frame(self):
        self.right_frame = tk.Canvas(self.frame, width=300, height=ALTURA_TABULEIRO, bg='white')
        self.right_frame.pack(side="right")

    def _create_player_text(self):
        self.player_text = self.canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 10, 
                                                    text=f"#{self.player_name}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")
        
    def update_current_player_text(self):
        self.canvas.delete(self.current_player_text)
        current_player = self.game.get_player_turn()
        self.current_player_text = self.canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 30,
                                                    text=f"Current player: {current_player.get_player_name()}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")

    def _create_current_player_text(self):
        current_player = self.game.get_player_turn()
        self.current_player_text = self.canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 30,
                                                        text=f"Current player: {current_player.get_player_name()}", anchor="nw",
                                                        font=("Arial", 16, "bold"), fill="#172934") 

    def _create_game_title(self):
        self.canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

    def refresh_ui(self):
        self.right_frame.update_cards(self.game.players)
        # self.toggle_dice_visibility() # TODO: wtf?
        self.dice.draw(self.game.get_dice().number)

        for player in self.game.get_players():
            self.board.update_player_position(player)
    
    # TODO: put this somewhere else man wtf
    def handle_move(self, move):
        self.game.update_game_state(move['game'])
        self.refresh_ui()
