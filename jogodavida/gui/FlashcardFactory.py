from tkinter import *
from Player import Player
from collections import namedtuple
from gui.FlashcardCreator import FlashcardCreator
from gui.ShadowCreator import ShadowCreator
from gui.TextCreator import TextCreator

Flashcard = namedtuple("Card", ["field", "value"])


class FlashcardFactory:
    def __init__(self, frame, board_height, players):
        self.__frame = frame
        self.__card_width = int(0.8 * 300)
        self.__card_height = int(board_height / 4)
        self.__card_space = int((board_height - 3 * self.__card_height) / 4)
        self.__x1 = (300 - self.__card_width) // 2
        self.__card_attributes = ['#ebf8ff', '#70cdf6', '#aadef5', '#043c50']
        self.__cards_nodes = self.create_flashcards(players)

    def refresh_flashcards(self, players):
        self.delete_flashcards()
        self.__cards_nodes = self.create_flashcards(players)

    def __create_flashcard(self, player: Player, i: int) -> dict:
        y1 = self.__card_space * (i + 1) + self.__card_height * i
        x2 = self.__x1 + self.__card_width
        y2 = y1 + self.__card_height

        shadow = ShadowCreator(self.__frame, self.__card_attributes).create_shadow(self.__x1, y1, x2, y2, radius=20)

        card = FlashcardCreator(self.__frame, self.__card_width, self.__card_attributes).create_flashcard(self.__x1, y1, x2, y2, radius=20)

        id_text = self.__frame.create_text(self.__x1 + 10, y1 + 10, text=f'#{player.get_player_name()}', anchor="nw", font=("Arial", 14, "bold"), fill=self.__card_attributes[3])

        y_start = self.__card_space * (i + 1) + self.__card_height * i + 40
        card_content = player.get_card_content()
        card_texts = TextCreator(self.__frame, self.__x1, y_start, self.__card_width).create_text(card_content)

        return {"shadow": shadow, "card": card, "id_text": id_text, "texts": card_texts}

    def create_flashcards(self, players):
        card_texts = []
        for i, player in enumerate(players):
            card_texts.append(self.__create_flashcard(player, i))
        return card_texts
    
    def delete_flashcards(self):
        for card in self.__cards_nodes:
            ShadowCreator.delete_shadow(self.__frame, card['shadow'])
            FlashcardCreator.delete_flashcard(self.__frame, card['card'])
            self.__frame.delete(card['id_text'])
            TextCreator.delete_text(self.__frame, card['texts'])

