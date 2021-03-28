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

        # NOTE: The game will NOT save things like phox health, phox status, and
        #       whether ro not a phox is disconnected. These things are all meant
        #       to serve as obstacles in Pokemon when traversing world zones, such
        #       as Mt. Moon, the cycling path, or even Indigo Plateau. Instead,
        #       progress through analagous zones will be tracked in the Player class.
        #       For example, in order to get through the Phoxtrot version of Mt. Moon,
        #       the player will need to win 10 successive fights in a specific region
        #       without returning to the Phoxtrot website to heal. When a player goes
        #       to Phoxtrot.com or quits the game, their progress is lost. This way,
        #       every time a player logs on, she will be able to have her entire team
        #       alive and healthy, and it will not change the difficulty of the game.
