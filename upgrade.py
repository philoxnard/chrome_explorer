class Upgrade:
    """
    A class to model an upgrade
    """

    def __init__(self):
        self.name = ""
        self.plain_text_effect = ""

    def serialize(self):
        return {
            "name": self.name.title(),
            "effect": self.plain_text_effect}