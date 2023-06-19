from Card import Card
from Player import Player

class ModifierCard(Card):
    def __init__(self, name, description, modifier, mod_type, times_picked):
        super().__init__(name, description, mod_type, times_picked)
        self.modifier = modifier

    def apply_effect(self, player : Player):
        player.modify_state(self.modifier)
