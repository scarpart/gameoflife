from collections import namedtuple

Card = namedtuple("Card", ["field", "value"])

class TextCreator:
    def __init__(self, frame, x1, y_start, card_width):
        self.frame = frame
        self.x1 = x1
        self.y_start = y_start
        self.card_width = card_width

    def create_text(self, card_content):
        card_texts = []
        for line in card_content:
            field_text = self.frame.create_text(self.x1 + 10, self.y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#22471a')
            value_text = self.frame.create_text(self.x1 + self.card_width - 10, self.y_start, text=line['value'], anchor="ne", font=("Arial", 12), fill='#22471a')
            card_texts.append(Card(field_text, value_text))
            self.y_start += 22
        return card_texts
    
    @staticmethod
    def delete_text(frame, texts):
        for card_text in texts:
            frame.delete(card_text.field)
            frame.delete(card_text.value)
