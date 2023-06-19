from gui.ShapeCreator import ShapeCreator

class ShadowCreator(ShapeCreator):
    def __init__(self, frame, card_attributes):
        super().__init__(frame)
        self.card_attributes = card_attributes

    def create_shadow(self, x1, y1, x2, y2, radius):
        return self.create_rounded_rect(x1 + 5, y1 + 5, x2 + 5, y2 + 5, radius=radius, fill=self.card_attributes[0])

    @staticmethod
    def delete_shadow(frame, shadow):
        frame.delete(shadow)