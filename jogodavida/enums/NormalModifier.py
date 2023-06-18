
class NormalModifier:
    def __init__(self, type, value, is_wife=False):
        self.type = type
        self.value = value
        # This next one is only relevant for NormalModfiers of type FAMILY and will be used in add_family_member
        # which is a method of the Player class.
        self.is_wife = is_wife

