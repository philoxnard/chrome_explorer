class Attack:
    """
    A class to model an attack
    """

    def __init__(self):
        self.name = ""
        self.family = ""
        self.style = ""
        self.damage = 0
        self.cost = 0
        self.effect = ""

    def serialize(self):
        return {
            "name": self.name.title(),
            "family": self.family.title(),
            "style": self.style.title(),
            "damage": self.damage,
            "cost": self.cost,
            "effect": self.plain_text_effect}