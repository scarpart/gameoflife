from Card import Card
from Player import Player

class PropertyCard(Card):
    def __init__(self, name, description, property, mod_type, times_picked):
        super().__init__(name, description, mod_type, times_picked=times_picked)
        self.property = property
