from enums.NormalModifier import NormalModifier

class PropertyModifier(NormalModifier):
    def __init__(self, type, value, new_family_member=False):
        super().__init__(type, value, new_family_member)
        # TODO: self.sprite = somethingidk
