from gui.ShapeCreator import ShapeCreator

class FlashcardCreator(ShapeCreator):
    def __init__(self, frame, card_width, card_attributes):
        super().__init__(frame)
        self.card_width = card_width
        self.card_attributes = card_attributes

    def create_flashcard(self, x1, y1, x2, y2, radius):
        return self.create_rounded_rect(x1, y1, x2, y2, radius=radius, fill=self.card_attributes[1], outline=self.card_attributes[2])

    @staticmethod
    def delete_flashcard(frame, card):
        frame.delete(card)