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
            "name": self.name,
            "family": self.family,
            "style": self.style,
            "damage": self.damage,
            "cost": self.cost,
            "effect": self.effect}