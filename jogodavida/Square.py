from tkinter import Label
from PIL import ImageTk, Image
from Player import Player
from constants import LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates


class Square:
    def __init__(self, position):
        self.position = get_board_house_coordinates(position)
        self.position_index = position
        self.fees = 0
        self.owner: Player = None
        self.property_icon = None
        self.label = Label() 

    def to_dict(self) -> tuple:
        sqdict = {
            "position": self.position_index,
            "fees": self.fees,
            "owner": self.owner.get_player_id()
        }
        return sqdict 

    def get_position_index(self) -> int:
        return self.position_index

    def add_property_icon(self) -> ImageTk:
        img = None
        if self.owner.get_colour() == "red":
            img = Image.open(r"media/property_icons/property_red.png")
        elif self.owner.get_colour() == "yellow":
            img = Image.open(r"media/property_icons/property_yellow.png")
        else:
            img = Image.open(r"media/property_icons/property_blue.png")
        new_width = LARGURA_CASA // 3
        new_height = LARGURA_CASA // 3
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        self.property_icon = ImageTk.PhotoImage(img)
        return self.property_icon
    
    def get_position(self):
        return self.position

    def has_owner(self) -> bool:
        return self.owner is not None

    def set_owner(self, owner):
        self.owner = owner

    def set_fees(self, fees):
        self.fees = fees

    def get_owner(self) -> Player:
        return self.owner
    
    def get_property_icon(self):
        return self.property_icon

    def get_property_fees(self) -> int:
        return self.fees
