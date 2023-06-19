from tkinter import *
from Game import Game
from PropertyCard import PropertyCard
from constants import LARGURA_TABULEIRO, PROPERTY_FEE
from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from gui.GameInterface import GameInterface
from gui.InitInterface import InitInterface
from CareerType import CareerType
import tkinter as tk


class PlayerInterface(DogPlayerInterface):
    def __init__(self, master):
        self.master = master
        self.player_name = ''
        self.init_interface = None
        self.game_interface = None
        self.local_actor = None

        self.__game = Game(self)
        self.render_init_interface()
        self.master.mainloop()

    def get_master(self) -> Tk:
        return self.master

    def show_messagebox_info(self, title, text):
        tk.messagebox.showinfo(title, text)

    def show_card_options(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Pick a card")

        player = self.__game.get_player_turn()
        current_position = player.get_position()
        cards = self.__game.get_cards_for_position(current_position)

        for card in cards:
            button_text = self.__create_flashcard_button_text(card)
            button = tk.Button(dialog, text=button_text, command=lambda c=card: self.__game.select_card(c, dialog))
            button.pack(fill='both', expand=True, padx=5, pady=5)
        
        return dialog

    def refresh_ui(self):
        self.game_interface.refresh_ui()

    def render_win_screen(self, winner):       
        if self.game_interface:
            self.game_interface.frame.destroy()
            self.game_interface = None

        self.master.configure(background='dark green') 
        label = Label(self.master, text=f'You won! You had the most money, {winner.get_total_money()} and a salary of {winner.get_salary()}!',
                    bg='dark green', fg='white', justify=CENTER, wraplength=LARGURA_TABULEIRO)
        label.config(font=("Courier", 15))  
        label.pack(expand=True, pady=20, padx=20)  

    def render_loss_screen(self, winner):
        if self.game_interface:
            self.game_interface.frame.destroy()
            self.game_interface = None

        self.master.configure(background='dark red')  
        label = Label(self.master, text=f'You lost and {winner.get_player_name()} won! He had the most money, {winner.get_total_money()} and a salary of {winner.get_salary()}!',
                    bg='dark red', fg='white', justify=CENTER, wraplength=LARGURA_TABULEIRO)
        label.config(font=("Courier", 15))  
        label.pack(expand=True, pady=20, padx=20)  

    def show_career_options(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Select a career")

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        label = tk.Label(dialog, text="Select a career:")
        label.pack(pady=10)

        financial_button_info = "Financial Career:\nProperty Discount: 15%\nBonus Rent: 0%\nBonus Salary: 20%"
        financial_button = tk.Button(dialog, text=financial_button_info, command=lambda: self.__set_career_and_clear_options(CareerType.FINANTIAL, dialog))
        financial_button.pack(pady=5)

        normal_button_info = "Normal Career:\nProperty Discount: 5%\nBonus Rent: 30%\nBonus Salary: 0%"
        normal_button = tk.Button(dialog, text=normal_button_info, command=lambda: self.__set_career_and_clear_options(CareerType.NORMAL, dialog))
        normal_button.pack(pady=5)

        self.master.wait_window(dialog)
        
    def __set_career_and_clear_options(self, career, dialog):
        player = self.__game.get_player_turn()
        if not player.get_can_pick_career():
            return
        # aqui dentro nós checamos o tipo de carreira e adicionamos aos atributos do jogador de acordo
        # somente após isso, nós fazemos a atualização da carreira do jogador no atributo
        # por favor, não se engane com o nome do método, não achamos nada melhor :(
        player.set_career(career) 
        dialog.destroy()

    def render_init_interface(self):
        game_interface = self.get_game_interface()
        if game_interface:
            self.game_interface.frame.destroy()
            self.game_interface = None

        self.init_interface = InitInterface(self.master)
        self.player_name = self.init_interface.get_player_name()  

        self.local_actor = DogActor()
        message = self.local_actor.initialize(self.player_name, self)
        self.show_messagebox_info("Connection message", message) 

        self.init_interface.button.configure(command=self.__game.start_game)

    def get_game_interface(self) -> GameInterface:
        return self.game_interface
    
    def get_local_actor(self) -> DogActor:
        return self.local_actor

    def render_game_interface(self, players):
        init_interface = self.init_interface
        if init_interface:
            self.init_interface.frame.destroy()
            self.init_interface = None

        self.game_interface = GameInterface(self.master, self.player_name, players, self.__game)

    def receive_move(self, move : dict):
        self.__game.handle_move(move)
        self.refresh_ui()

    def update_current_player_text(self):
        self.game_interface.update_current_player_text()

    def receive_start(self, start_status):
        message = start_status.get_message()
        players = start_status.get_players()
        self.__game.set_local_player_id(players[0][1])
        self.show_messagebox_info("Start status", message)
        self.render_game_interface(players)

    def receive_withdrawal_notification(self):
        if self.game_interface:
            self.game_interface.frame.destroy()
            self.game_interface = None
        if self.init_interface:
            self.init_interface.frame.destroy()
            self.init_interface = None

        self.master.configure(background='light gray') 
        label = Label(self.master, text=f"A user has left the game. The game has ended and there are no winners.",
                    bg='light gray', fg='black', justify=CENTER)
        label.config(font=("Courier", 15))  
        label.pack(pady=20, padx=20) 

    def __create_flashcard_button_text(self, card) -> str:
        return f"Name: {card.name}\nDescription: {card.description}\nModifier Type: {card.mod_type}"
