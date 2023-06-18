from tkinter import *
import tkinter as tk
from constants import ALTURA_TABULEIRO
from gui.FlashcardFactory import FlashcardFactory

class RightFrame:
    def __init__(self, master, width, height, players):
        self.right_frame = tk.Canvas(master, width=width, height=height, bg='white')
        self.right_frame.pack(side="right")
        self.cards = FlashcardFactory(self.right_frame, ALTURA_TABULEIRO, players)

    def update_cards(self, players):
        self.cards.refresh_flashcards(players)