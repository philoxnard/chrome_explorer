class Player:
    """
    A class to model a player
    """

    def __init__(self):
        # Attributes imported from database
        self.username = ""
        self.party = []
        self.collection = []

        # Attributes changed during play
        self.url = "https://www.youtube.com/philoxnard/chrome_explorer"
