from tkinter import *
from Player import Player
from typing import List
from collections import namedtuple
from gui.FlashcardCreator import FlashcardCreator
from gui.ShadowCreator import ShadowCreator
from gui.TextCreator import TextCreator

Flashcard = namedtuple("Card", ["field", "value"])


class FlashcardFactory:
    def __init__(self, frame, board_height, players: list[Player]):
        self.frame = frame
        self.card_width = int(0.8 * 300)
        self.card_height = int(board_height / 4)
        self.card_space = int((board_height - 3 * self.card_height) / 4)
        self.x1 = (300 - self.card_width) // 2
        self.card_attributes = ['#ebf8ff', '#70cdf6', '#aadef5', '#043c50']
        self.cards_nodes = self.create_flashcards(players)

    def refresh_flashcards(self, players: list[Player]):
        self.delete_flashcards()
        self.cards_nodes = self.create_flashcards(players)

    def create_flashcard(self, player: Player, i: int) -> dict:
        y1 = self.card_space * (i + 1) + self.card_height * i
        x2 = self.x1 + self.card_width
        y2 = y1 + self.card_height

        shadow = ShadowCreator(self.frame, self.card_attributes).create_shadow(self.x1, y1, x2, y2, radius=20)

        card = FlashcardCreator(self.frame, self.card_width, self.card_attributes).create_flashcard(self.x1, y1, x2, y2, radius=20)

        id_text = self.frame.create_text(self.x1 + 10, y1 + 10, text=f'#{player.get_player_name()}', anchor="nw", font=("Arial", 14, "bold"), fill=self.card_attributes[3])

        y_start = self.card_space * (i + 1) + self.card_height * i + 40
        card_content = player.get_card_content()
        card_texts = TextCreator(self.frame, self.x1, y_start, self.card_width).create_text(card_content)

        return {"shadow": shadow, "card": card, "id_text": id_text, "texts": card_texts}

    def create_flashcards(self, players: List[Player]):
        card_texts = []
        for i, player in enumerate(players):
            card_texts.append(self.create_flashcard(player, i))
        return card_texts
    
    def delete_flashcards(self):
        for card in self.cards_nodes:
            ShadowCreator.delete_shadow(self.frame, card['shadow'])
            FlashcardCreator.delete_flashcard(self.frame, card['card'])
            self.frame.delete(card['id_text'])
            TextCreator.delete_text(self.frame, card['texts'])

